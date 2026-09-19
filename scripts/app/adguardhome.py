import os
from typing import List, Set, Dict

from loguru import logger

from app.base import APPBase

class AdGuardHome(APPBase):
    def __init__(self, blockList:List[str], unblockList:List[str], filterDict:Dict[str,str], filterList:List[str], filterList_var:List[str], ChinaSet:Set[str], fileName:str, sourceRule:str):
        super(AdGuardHome, self).__init__(blockList, unblockList, filterDict, filterList, filterList_var, ChinaSet, fileName, sourceRule)
        # 放行(白名单)规则单独生成一份文件，命名规则与 xxxlite.txt 的方式保持一致：
        # 在扩展名前插入 "allow"，例如 adblockdns.txt -> adblockdnsallow.txt
        self.fileNameAllow:str = self.__insertSuffix(self.fileName, "allow")
        self.fileNameAllowLite:str = self.__insertSuffix(self.fileNameLite, "allow")

    @staticmethod
    def __insertSuffix(fileName:str, suffix:str) -> str:
        idx = fileName.rfind(".")
        if idx == -1:
            return fileName + suffix
        return fileName[:idx] + suffix + fileName[idx:]

    def __writeRuleFile(self, fileName:str, domainList:List[str], isLite:bool, isAllow:bool):
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
            f.write("!\n")
            for domain in domainList:
                f.write("%s%s^\n" % (prefix, domain))

    def generate(self, isLite=False):
        try:
            if isLite:
                logger.info("generate adblock AdGuardHome Lite...")
                fileName = self.fileNameLite
                fileNameAllow = self.fileNameAllowLite
                blockList = self.blockListLite
                unblockList = self.unblockListLite
            else:
                logger.info("generate adblock AdGuardHome...")
                fileName = self.fileName
                fileNameAllow = self.fileNameAllow
                blockList = self.blockList
                unblockList = self.unblockList

            # 拦截规则：单独生成
            self.__writeRuleFile(fileName, blockList, isLite, isAllow=False)
            # 放行规则：单独生成一份独立的放行名单
            self.__writeRuleFile(fileNameAllow, unblockList, isLite, isAllow=True)

            if isLite:
                logger.info("adblock AdGuardHome Lite: block=%d, unblock=%d"%(len(blockList), len(unblockList)))
            else:
                logger.info("adblock AdGuardHome: block=%d, unblock=%d"%(len(blockList), len(unblockList)))
        except Exception as e:
            logger.error("%s"%(e))
