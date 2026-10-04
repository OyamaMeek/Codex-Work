import configparser
from pathlib import Path
import sys


def read_profile(path):
    parser = configparser.ConfigParser(
        interpolation=None, allow_no_value=True, delimiters=("=",),
        comment_prefixes=("#", ";", "//"),
    )
    parser.optionxform = str
    parser.read_string(Path(path).read_text())
    return parser


current = read_profile(sys.argv[1])
before = read_profile(sys.argv[2])
rules = list(current["Rule"])
expected_direct = [
    "USER-AGENT,MicroMessenger%20Client,DIRECT",
    "USER-AGENT,WeChat*,DIRECT",
    "USER-AGENT,%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1*,DIRECT",
    "DOMAIN-SUFFIX,gtimg.com,DIRECT",
    "DOMAIN-SUFFIX,idqqimg.com,DIRECT",
    "DOMAIN-SUFFIX,igamecj.com,DIRECT",
    "DOMAIN-SUFFIX,myapp.com,DIRECT",
    "DOMAIN-SUFFIX,myqcloud.com,DIRECT",
    "DOMAIN-SUFFIX,qq.com,DIRECT",
    "DOMAIN-SUFFIX,qqmail.com,DIRECT",
    "DOMAIN-SUFFIX,servicewechat.com,DIRECT",
    "DOMAIN-SUFFIX,tencent.com,DIRECT",
    "DOMAIN-SUFFIX,tencent-cloud.net,DIRECT",
    "DOMAIN-SUFFIX,tenpay.com,DIRECT",
    "DOMAIN-SUFFIX,wechat.com,DIRECT",
    "DOMAIN,file-igamecj.akamaized.net,DIRECT",
]
assert rules[:16] == expected_direct, "腾讯 User-Agent / 域名直连没有在 IP 判断前生效"
assert rules[16] == "AND,((OR,((PROCESS-NAME,WeChat),(DOMAIN-SUFFIX,qpic.cn),(DOMAIN-SUFFIX,qlogo.cn))),(GEOIP,CN)),DIRECT", "微信图片缺少优先中国 IP 直连判断"
assert rules[17] == "OR,((PROCESS-NAME,WeChat),(DOMAIN-SUFFIX,qpic.cn),(DOMAIN-SUFFIX,qlogo.cn)),Final", "微信非中国 IP 图片未在其他服务规则前进入 Final"
before_rules = list(before["Rule"])
assert len(before_rules) == 58, "原转换结果不符合已确认的58条规则"
assert rules[18:] == before_rules[10:], "范围外规则内容或顺序改变"
assert len(rules) == 66
for section in ("General", "Proxy", "Proxy Group", "Host", "MITM", "Script"):
    assert dict(current[section]) == dict(before[section]), f"{section} 的原参数、节点或分组改变"
assert list(current["Proxy Group"]) == list(before["Proxy Group"]), "分组展示顺序改变"
assert "{{" not in Path(sys.argv[1]).read_text(), "实际转换没有展开模板变量"
assert not any("HOSTNAME-TYPE,IPv6" in rule or "WeChat.list" in rule or "43.156.222.0/24" in rule for rule in rules), "旧微信特殊规则仍在生效"
print("PASS：66条规则按腾讯直连、中国 IP 直连及 Final 顺序生成；范围外规则、节点与分组保留")
