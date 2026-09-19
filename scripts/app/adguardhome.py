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
    def __splitRegexRules(cls, filterList:List[str]):
        blockRegex, unblockRegex = [], []
        for rule in filterList:
            if not cls._REGEX_RULE_PATTERN.match(rule):
                continue
            if rule.startswith('@@'):
                unblockRegex.append(rule)
            else:
                blockRegex.append(rule)
        return blockRegex, unblockRegex

    def __writeRuleFile(self, fileName:str, domainList:List[str], regexList:List[str], isLite:bool, isAllow:bool):
        if os.path.exists(fileName):
            os.remove(fileName)

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
