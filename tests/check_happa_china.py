import configparser
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
external = configparser.ConfigParser(interpolation=None, strict=False)
external.read(root / "HappaConfig.ini")
rule = "RULE-SET,https://document.happanetwork.com/HappaConfig/China.list,China"
assert external["template"].get("china_happa_rule") == rule, "INI 缺少 China 远程规则"
base = (root / "HappaConfig.conf").read_text()
references = re.findall(r"{{ local\.(\w+) }}", base)
assert references.count("china_happa_rule") == 1, "CONF 缺少唯一 China 远程规则引用"
assert references.index("china_domain_rule") + 1 == references.index("china_happa_rule"), "China 远程规则未紧接国内域名集合"
assert references.index("china_happa_rule") + 1 == references.index("china_asn_rule"), "China 远程规则未位于国内 ASN 规则之前"
rendered = re.sub(r"{{ local\.(\w+) }}", lambda match: external["template"][match[1]], base)
profile = configparser.ConfigParser(interpolation=None, allow_no_value=True, delimiters=("=",), comment_prefixes=("#", ";", "//"))
profile.optionxform = str
profile.read_string(rendered)
assert len(profile["Rule"]) == 71, "规则总数错误"
assert list(profile["Rule"]).count(rule) == 1, "生成模板缺少唯一 China 远程规则"
print("PASS：China 远程规则唯一引用，策略为 China，模板展开为71条规则且顺序有效")
