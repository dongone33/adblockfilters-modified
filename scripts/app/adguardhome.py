import ipaddress
import os
import re
from typing import List, Set, Dict

from loguru import logger

from app.base import APPBase

class AdGuardHome(APPBase):
    # AdGuardHome(dnsfilter) 除了 ||domain^ / @@||domain^ 这类纯域名规则外，
    # 还支持 /regex/ 形式的正则规则（可带 @@ 前缀表示放行，也可带 $modifier 后缀）。
    # 上游 filterList/filterList_var 中混杂着正则、通配符、$修饰符等复杂规则，
    # 这里只挑出真正的 /regex/ 规则，其余（元素隐藏、脚本变量等）DNS 层用不上，继续丢弃。
    _REGEX_RULE_PATTERN = re.compile(r'^(@@)?/.+/(\$\S*)?$')

    # ---- 以下为"输出前最后一道合规校验"，依据 AdGuard DNS 过滤规则语法文档 ----
    # 1) DNS 规则只支持这些修饰符；含其它修饰符（$script/$third-party/$domain=/$3p/$xhr/$network 等）
    #    的规则文档要求整条忽略，写进去只会成为无效规则。
    _SUPPORTED_MODIFIERS = {'important', 'badfilter', 'dnstype', 'dnsrewrite', 'denyallow', 'client', 'ctag'}
    # 2) 主机名：每段 1~63 字符，不以 - 开头/结尾；允许下划线（实践中广泛存在）；TLD 为字母或 punycode。
    _HOSTNAME_LABEL = r'(?!-)[a-z0-9_-]{1,63}(?<!-)'
    _HOSTNAME_PATTERN = re.compile(r'^(?:%s\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]{1,59})$' % _HOSTNAME_LABEL)
    # 3) AdGuard Home 使用 Go(RE2) 正则：不支持前瞻/后顾/反向引用，重复次数上限 1000。
    _RE2_UNSUPPORTED = re.compile(r'\(\?(?:=|!|<=|<!)|\\[1-9]')
    _REPEAT_COUNT = re.compile(r'\{(\d+)(?:,(\d*))?\}')

    def __init__(self, blockList:List[str], unblockList:List[str], filterDict:Dict[str,str], filterList:List[str], filterList_var:List[str], ChinaSet:Set[str], fileName:str, sourceRule:str):
        super(AdGuardHome, self).__init__(blockList, unblockList, filterDict, filterList, filterList_var, ChinaSet, fileName, sourceRule)
        # 放行(白名单)规则单独生成一份文件，命名规则与 xxxlite.txt 的方式保持一致：
        # 在扩展名前插入 "allow"，例如 adblockdns.txt -> adblockdnsallow.txt
        self.fileNameAllow:str = self.__insertSuffix(self.fileName, "allow")
        self.fileNameAllowLite:str = self.__insertSuffix(self.fileNameLite, "allow")

        # 从 filterList 中拆出可用于 AdGuardHome 的正则规则，按拦截/放行归类
        self.blockRegexList, self.unblockRegexList = self.__splitRegexRules(self.filterList)
        self.blockRegexListLite, self.unblockRegexListLite = self.__splitRegexRules(self.filterListLite)

    @staticmethod
    def __insertSuffix(fileName:str, suffix:str) -> str:
        idx = fileName.rfind(".")
        if idx == -1:
            return fileName + suffix
        return fileName[:idx] + suffix + fileName[idx:]

    @classmethod
    def _isValidHost(cls, host:str) -> bool:
        """host 必须是合法主机名或 IP 字面量；含空格（如 '0.0.0.0 example.com'）等一律无效。"""
        if not host or len(host) > 253:
            return False
        try:
            ipaddress.ip_address(host)
            return True
        except ValueError:
            pass
        return cls._HOSTNAME_PATTERN.match(host) is not None

    @classmethod
    def _isCompatibleRegexRule(cls, rule:str) -> bool:
        """判断一条 /regex/ 规则能否在 AdGuard Home 中生效。"""
        text = rule[2:] if rule.startswith('@@') else rule
        if len(text) < 3 or not text.startswith('/'):
            return False
        if text.endswith('/'):
            pattern, opts = text, ''
        else:
            # 与 urlfilter 一致：以最后一个未转义的 $ 作为修饰符分隔符
            idx = -1
            for i in range(len(text) - 1, -1, -1):
                if text[i] == '$' and (i == 0 or text[i - 1] != '\\'):
                    idx = i
                    break
            if idx < 0:
                return False
            pattern, opts = text[:idx], text[idx + 1:]
            if len(pattern) < 3 or not pattern.endswith('/'):
                return False
        body = pattern[1:-1]
        for opt in re.split(r'(?<!\\),', opts):
            if opt and opt.split('=', 1)[0] not in cls._SUPPORTED_MODIFIERS:
                return False
        # DNS 只匹配主机名，含 URL 路径特征的正则永远不会命中
        if '\\/' in body or '://' in body:
            return False
        if cls._RE2_UNSUPPORTED.search(body):
            return False
        for m in cls._REPEAT_COUNT.finditer(body):
            if int(m.group(1)) > 1000 or (m.group(2) and int(m.group(2)) > 1000):
                return False
        return True

    @classmethod
    def __splitRegexRules(cls, filterList:List[str]):
        blockRegex, unblockRegex = [], []
        skipped = 0
        for rule in filterList:
            if not cls._REGEX_RULE_PATTERN.match(rule):
                continue
            if not cls._isCompatibleRegexRule(rule):
                skipped += 1
                continue
            if rule.startswith('@@'):
                unblockRegex.append(rule)
            else:
                blockRegex.append(rule)
        if skipped:
            logger.info("AdGuardHome: skip %d regex rules incompatible with AdGuard Home (modifiers/RE2/URL-path)"%(skipped))
        return blockRegex, unblockRegex

    def __writeRuleFile(self, fileName:str, domainList:List[str], regexList:List[str], isLite:bool, isAllow:bool):
        if os.path.exists(fileName):
            os.remove(fileName)

        # 输出前过滤掉非法主机名，避免上游解析缺陷产生 "||0.0.0.0 example.com^" 之类的无效规则
        validDomains = [d for d in domainList if self._isValidHost(d)]
        if len(validDomains) != len(domainList):
            logger.warning("AdGuardHome %s: drop %d invalid host entries, e.g. %s"%(os.path.basename(fileName), len(domainList) - len(validDomains), [d for d in domainList if not self._isValidHost(d)][:3]))
        domainList = validDomains

        if isAllow:
            title = "AdBlock DNS Allowlist" + (" Lite" if isLite else "")
            desc = "适用于 AdGuard、AdGuardHome 的放行（白名单/误杀修复）规则，每 12 小时更新一次。规则源：%s。" % (self.sourceRule)
            if isLite:
                desc += " Lite 版仅针对国内域名放行。"
            countLabel = "Unblocked domains"
            prefix = "@@||"
        else:
            title = "AdBlock DNS" + (" Lite" if isLite else "")
            desc = "适用于 AdGuard、AdGuardHome 的去广告合并规则，每 12 小时更新一次。规则源：%s。" % (self.sourceRule)
            if isLite:
                desc += " Lite 版仅针对国内域名拦截。"
            countLabel = "Blocked domains"
            prefix = "||"

        with open(fileName, 'a') as f:
            f.write("!\n")
            f.write("! Title: %s\n" % (title))
            f.write("! Description: %s\n" % (desc))
            f.write("! Homepage: %s\n" % (self.homepage))
            f.write("! Source: %s/%s\n" % (self.source, os.path.basename(fileName)))
            f.write("! Version: %s\n" % (self.version))
            f.write("! Last modified: %s\n" % (self.time))
            f.write("! %s: %s\n" % (countLabel, len(domainList)))
            f.write("! Regex rules: %s\n" % (len(regexList)))
            f.write("!\n")
            for domain in domainList:
                f.write("%s%s^\n" % (prefix, domain))
            for regex in regexList:
                f.write("%s\n" % (regex))

    def generate(self, isLite=False):
        try:
            if isLite:
                logger.info("generate adblock AdGuardHome Lite...")
                fileName = self.fileNameLite
                fileNameAllow = self.fileNameAllowLite
                blockList = self.blockListLite
                unblockList = self.unblockListLite
                blockRegexList = self.blockRegexListLite
                unblockRegexList = self.unblockRegexListLite
            else:
                logger.info("generate adblock AdGuardHome...")
                fileName = self.fileName
                fileNameAllow = self.fileNameAllow
                blockList = self.blockList
                unblockList = self.unblockList
                blockRegexList = self.blockRegexList
                unblockRegexList = self.unblockRegexList

            # 拦截规则（域名 + 正则）：单独生成
            self.__writeRuleFile(fileName, blockList, blockRegexList, isLite, isAllow=False)
            # 放行规则（域名 + 正则）：单独生成一份独立的放行名单
            self.__writeRuleFile(fileNameAllow, unblockList, unblockRegexList, isLite, isAllow=True)

            if isLite:
                logger.info("adblock AdGuardHome Lite: block=%d(+%d regex), unblock=%d(+%d regex)"%(len(blockList), len(blockRegexList), len(unblockList), len(unblockRegexList)))
            else:
                logger.info("adblock AdGuardHome: block=%d(+%d regex), unblock=%d(+%d regex)"%(len(blockList), len(blockRegexList), len(unblockList), len(unblockRegexList)))
        except Exception as e:
            logger.error("%s"%(e))
        except Exception as e:
            logger.error("%s"%(e))
