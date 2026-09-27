# AdBlock DNS Filters Modified
[217heidai/adblockfilters](https://github.com/217heidai/adblockfilters) 去广告合并规则增强版，每天更新一次。  

| 指标 | 数值 |
| :- | :- |
| 上次更新（北京时间） | 2026/09/27 14:44:02 (UTC+08:00) |
| 上游规则总数（去重前） | 663361 |
| 上游规则总数（去重后） | 405891 |
| 上游规则去重率 | 38.81% |
| 有效规则数量（可解析） | 258741 |
| 有效规则占比（检测域名） | 78.11% |
| 中国规则数（Lite） | 10912 |
| 中国规则占比（Lite/成品） | 9.66% |

## 说明
1. 定时从上游各规则源获取更新，合并去重。
2. 工作流程：拉取上游规则 → 解析提取域名/规则 → 使用本地 SmartDNS 验证连通性并剔除失效域名（上游规则中存在大量无法解析的域名）→ 生成各类成品规则与统计。
3. 上游规则源增删方法：维护 README 中“上游规则源”表格的规则名/类型/链接，工作流会按表格自动拉取并参与生成。
4. 本地新增拦截/白名单：在 `sources/local/myblock.txt` 添加自定义拦截域名/规则；在 `sources/local/white2.txt` 添加放行域名或 `@@||domain^` 形式白名单规则，支持 `+.example.com`（主域+子域）/`*.example.com`（仅子域）语法，工作流会自动合并生效。
5. 本项目仅对上游规则进行合并、去重、去除无效域名，不做任何修改。如发现误拦截情况，可在 `sources/local/white2.txt` 中自行添加白名单（支持 `+.example.com`/`*.example.com` 语法），或临时添加放行规则（如 `@@||www.example.com^$important`），并向上游规则反馈。

性能说明：实测在 J4125 或同级别性能的 x86 主机上，百万级规则规模对 dnsmasq/AdGuard Home 的解析耗时影响不超过 1ms，可放心使用。

## 相比原版 adblockfilters 的改进与新增
1. 改进了处理逻辑，缩短工作流运行时间。
2. 改进了中国规则和无效规则的处理流程，现在每次生成规则前均会对这两类规则进行验证，不再使用历史数据。
3. 白名单自动同步上游仓库，并支持 `sources/local/white2.txt` 本地补充合并。
4. 域名提取与规则解析更完善，覆盖更多 filter/dns/host 规则格式，减少漏提取。
5. 新增/独有规则源（相对上游仓库，详见下表）：
<details>
<summary>点击展开/收起新增与独有规则源列表</summary>

- 10007_auto混合规则
- DD-AD
- DD-AD允许列表
- DNS-Kuner拦截列表
- DNS-Kuner放行列表
- HG
- HalfLife
- SMAdHosts
- SmartTV
- TTDNS
- anti-AD
- 晴雅广告拦截规则
- 茯苓允许列表
- 茯苓广告规则
- 那个谁520广告白名单
- 那个谁520规则

</details>

## 订阅链接
1. 规则x’为规则x的 Lite 版，仅针对国内域名拦截，体积较小（如添加完整规则报错数量限制，请尝试 Lite 规则）
2. 默认使用 testingcf.jsdelivr.net CDN，加速大文件会自动切换至 github.boki.moe
3. AdGuard 等浏览器插件使用规则1 + 规则2（规则2为规则1的补充，仅适用浏览器插件）

| 规则 | 原始链接 | 加速链接 | 文件体积(MB) | 规则数量 | 适配说明 |
| :- | :- | :- | :- | :- | :- | 
| 规则1 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdns.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdns.txt) | 4.42 | 196014 | AdGuard、AdGuard Home 等 |
| 规则1' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdnslite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdnslite.txt) | 0.24 | 11581 | AdGuard、AdGuard Home 等 |
| 规则2 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockfilters.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockfilters.txt) | 7.22 | 112935 | AdGuard 等 |
| 规则2' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockfilterslite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockfilterslite.txt) | 0.47 | 10912 | AdGuard 等 |
| 规则3 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdomain.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdomain.txt) | 3.85 | 195921 | InviZible Pro、personalDNSfilter |
| 规则3' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdomainlite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdomainlite.txt) | 0.21 | 11581 | InviZible Pro、personalDNSfilter |
| 规则4 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdnsmasq.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdnsmasq.txt) | 5.35 | 195921 | DNSMasq conf |
| 规则4' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdnsmasqlite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdnsmasqlite.txt) | 0.30 | 11581 | DNSMasq conf |
| 规则5 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksmartdns.conf) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksmartdns.conf) | 5.98 | 198471 | SmartDNS |
| 规则5' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksmartdnslite.conf) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksmartdnslite.conf) | 0.39 | 13508 | SmartDNS |
| 规则6 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockclash.list) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockclash.list) | 8.71 | 195922 | Shadowrocket |
| 规则6' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockclashlite.list) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockclashlite.list) | 0.50 | 11582 | Shadowrocket |
| 规则7 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockqx.conf) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockqx.conf) | 7.40 | 195921 | QuantumultX |
| 规则7' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockqxlite.conf) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockqxlite.conf) | 0.42 | 11581 | QuantumultX |
| 规则8 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockmihomo.yaml) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockmihomo.yaml) | 5.35 | 195921 | Clash Meta(Mihomo) yaml |
| 规则8' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockmihomolite.yaml) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockmihomolite.yaml) | 0.30 | 11581 | Clash Meta(Mihomo) yaml |
| 规则9 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockmihomo.mrs) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockmihomo.mrs) | 1.84 | 195921 | Clash Meta(Mihomo) mrs |
| 规则9' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockmihomolite.mrs) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockmihomolite.mrs) | 0.10 | 11581 | Clash Meta(Mihomo) mrs |
| 规则10 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockhosts.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockhosts.txt) | 5.35 | 195935 | Hosts |
| 规则10' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockhostslite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockhostslite.txt) | 0.30 | 11595 | Hosts |
| 规则11 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksingbox.json) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksingbox.json) | 5.91 | 195921 | sing-box 1.12.x json |
| 规则11' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksingboxlite.json) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksingboxlite.json) | 0.33 | 11581 | sing-box 1.12.x json |
| 规则12 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksingbox.srs) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksingbox.srs) | 1.66 | 195921 | sing-box 1.12.x srs |
| 规则12' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksingboxlite.srs) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksingboxlite.srs) | 0.08 | 11581 | sing-box 1.12.x srs |
| 规则13 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockloon.list) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockloon.list) | 6.47 | 195921 | Loon |
| 规则13' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockloonlite.list) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockloonlite.list) | 0.36 | 11581 | Loon |
| 规则14 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksurge.list) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksurge.list) | 4.04 | 195921 | Surge |
| 规则14' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksurgelite.list) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksurgelite.list) | 0.22 | 11581 | Surge |
| 规则15 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockmosdns.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockmosdns.txt) | 4.79 | 195921 | MosDNS v5 |
| 规则15' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockmosdnslite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockmosdnslite.txt) | 0.26 | 11581 | MosDNS v5 |
| 规则16 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksurgeruleset.list) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksurgeruleset.list) | 5.16 | 195921 | Surge RULE-SET |
| 规则16' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblocksurgerulesetlite.list) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblocksurgerulesetlite.list) | 0.29 | 11581 | Surge RULE-SET |
| 规则17 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockclashclassical.yaml) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockclashclassical.yaml) | 5.91 | 195921 | Clash Classical yaml |
| 规则17' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockclashclassicallite.yaml) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockclashclassicallite.yaml) | 0.33 | 11581 | Clash Classical yaml |
| 规则18 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockrouteros.txt) | [加速链接](https://github.boki.moe/https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockrouteros.txt) | 21.72 | 391842 | RouterOS |
| 规则18' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockrouteroslite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockrouteroslite.txt) | 1.24 | 23162 | RouterOS |
| 规则19 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockrouterosadlist.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockrouterosadlist.txt) | 9.76 | 391844 | RouterOS AdList |
| 规则19' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockrouterosadlistlite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockrouterosadlistlite.txt) | 0.54 | 23164 | RouterOS AdList |
| 规则20 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdnsmasqaddnhosts.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdnsmasqaddnhosts.txt) | 5.35 | 195921 | DNSMasq addn-hosts |
| 规则20' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdnsmasqaddnhostslite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdnsmasqaddnhostslite.txt) | 0.30 | 11581 | DNSMasq addn-hosts |
| 规则21 | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdnsmasqservers.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdnsmasqservers.txt) | 5.54 | 195921 | DNSMasq servers |
| 规则21' | [原始链接](https://raw.githubusercontent.com/dongone33/adblockfilters-modified/main/rules/adblockdnsmasqserverslite.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/rules/adblockdnsmasqserverslite.txt) | 0.31 | 11581 | DNSMasq servers |

## 上游规则源
1. 感谢各位广告过滤规则维护大佬们的辛苦付出。

| 规则 | 类型 | 原始链接 | 加速链接 | 规则数量 | 更新日期 |
| :- | :- | :- | :- | :- | :- | 
| AdGuard Base filter | filter | [原始链接](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/AdGuard_Base_filter.txt) | 168401 | 2026/09/27 |
| AdGuard Chinese filter | filter | [原始链接](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/AdGuard_Chinese_filter.txt) | 23209 | 2026/09/27 |
| AdGuard Mobile Ads filter | filter | [原始链接](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/AdGuard_Mobile_Ads_filter.txt) | 1064 | 2026/09/25 |
| AdGuard DNS filter | dns | [原始链接](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/AdGuard_DNS_filter.txt) | 185038 | 2026/09/27 |
| jiekouAD | filter | [原始链接](https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/jiekouAD.txt) | 5903 | 2026/09/19 |
| AWAvenue Ads Rule | dns | [原始链接](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/AWAvenue_Ads_Rule.txt) | 973 | 2026/09/22 |
| anti-AD | filter | [原始链接](https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/anti-AD.txt) | 95968 | 2026/09/26 |
| HalfLife | filter | [原始链接](https://cdn.jsdelivr.net/gh/sbwml/halflife-list@master/ad.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/HalfLife.txt) | 22052 | 2026/09/22 |
| DD-AD | filter | [原始链接](https://raw.githubusercontent.com/afwfv/DD-AD/refs/heads/release/easylist.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/DD-AD.txt) | 70436 | 2026/09/27 |
| 晴雅广告拦截规则 | filter | [原始链接](https://raw.githubusercontent.com/rssvcn/qy-Ads-Rule/main/black.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/晴雅广告拦截规则.txt) | 574 | 2026/09/19 |
| SMAdHosts | host | [原始链接](https://raw.githubusercontent.com/2Gardon/SM-Ad-FuckU-hosts/master/SMAdHosts) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/SMAdHosts.txt) | 5358 | 2026/09/19 |
| 那个谁520规则 | filter | [原始链接](https://raw.githubusercontent.com/qq5460168/666/refs/heads/master/rules.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/那个谁520规则.txt) | 33526 | 2026/09/27 |
| TTDNS | dns | [原始链接](https://raw.githubusercontent.com/TTDNS/Cat/refs/heads/main/DNS.TXT) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/TTDNS.txt) | 257 | 2026/09/19 |
| 茯苓广告规则 | filter | [原始链接](https://raw.githubusercontent.com/Kuroba-Sayuki/FuLing-AdRules/Master/FuLingRules/FuLingBlockList.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/茯苓广告规则.txt) | 653 | 2026/09/19 |
| HG | filter | [原始链接](https://raw.githubusercontent.com/2771936993/HG/main/hg1.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/HG.txt) | 13030 | 2026/09/27 |
| DNS-Kuner拦截列表 | dns | [原始链接](https://raw.githubusercontent.com/Kuner-mw/DNS-Kuner/main/FilterRules/blacklist.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/DNS-Kuner拦截列表.txt) | 151 | 2026/09/19 |
| SmartTV | filter | [原始链接](https://raw.githubusercontent.com/AdguardTeam/HostlistsRegistry/refs/heads/main/filters/other/filter_7_SmartTVBlocklist/filter.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/SmartTV.txt) | 169 | 2026/09/19 |
| 10007_auto混合规则 | filter | [原始链接](https://raw.githubusercontent.com/lingeringsound/10007_auto/master/adb.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/10007_auto混合规则.txt) | 13345 | 2026/09/27 |
| DNS-Blocklists PRO mini | dns | [原始链接](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.mini.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/DNS-Blocklists_PRO_mini.txt) | 58577 | 2026/09/27 |
| 茯苓允许列表 | filter | [原始链接](https://raw.githubusercontent.com/Kuroba-Sayuki/FuLing-AdRules/Master/FuLingRules/FuLingAllowList.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/茯苓允许列表.txt) | 1313 | 2026/09/19 |
| DD-AD允许列表 | filter | [原始链接](https://raw.githubusercontent.com/afwfv/DD-AD/refs/heads/release/DD-AD.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/DD-AD允许列表.txt) | 1636 | 2026/09/19 |
| 那个谁520广告白名单 | filter | [原始链接](https://raw.githubusercontent.com/qq5460168/666/master/allow.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/那个谁520广告白名单.txt) | 3706 | 2026/09/27 |
| DNS-Kuner放行列表 | dns | [原始链接](https://raw.githubusercontent.com/Kuner-mw/DNS-Kuner/main/FilterRules/allowlist.txt) | [加速链接](https://testingcf.jsdelivr.net/gh/dongone33/adblockfilters-modified@main/sources/upstream/DNS-Kuner放行列表.txt) | 65 | 2026/09/19 |

## Star History
<a href="https://www.star-history.com/#dongone33/adblockfilters-modified&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=dongone33/adblockfilters-modified&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=dongone33/adblockfilters-modified&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=dongone33/adblockfilters-modified&type=Date" />
 </picture>
</a>
