import configparser
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
source = (root / "HappaConfig.ini").read_text()
groups = [line.split("=", 1)[1].split("`") for line in source.splitlines() if line.startswith("custom_proxy_group=")]
names = [group[0] for group in groups]
assert names[names.index("Apple") + 1] == "SiriAI", "SiriAI 分组未紧接 Apple"
assert groups[names.index("SiriAI")][1:] == ["select", "[]US", "[]All Proxies", "[]Manual"], "SiriAI 候选或默认项错误"
assert len(names) == len(set(names)), "策略组重名"
assert all(member[2:] in set(names) | {"DIRECT", "REJECT"} for group in groups for member in group[2:] if member.startswith("[]")), "引用未定义策略"
external = configparser.ConfigParser(interpolation=None, strict=False)
external.read_string(source)
rule = "RULE-SET,https://document.happanetwork.com/HappaConfig/SiriAI.list,SiriAI"
assert external["template"]["siriai_rule"] == rule, "INI 缺少 SiriAI 完整规则"
base = (root / "HappaConfig.conf").read_text()
references = re.findall(r"{{ local\.(\w+) }}", base)
assert references.count("siriai_rule") == 1, "CONF 缺少唯一 SiriAI 引用"
assert references.index("siriai_rule") < references.index("appstore_rule"), "SiriAI 被 Apple 通用规则覆盖"
rendered = re.sub(r"{{ local\.(\w+) }}", lambda match: external["template"][match[1]], base)
profile = configparser.ConfigParser(interpolation=None, allow_no_value=True, delimiters=("=",), comment_prefixes=("#", ";", "//"))
profile.optionxform = str
profile.read_string(rendered)
assert len(profile["Rule"]) == 70, "规则总数错误"
assert list(profile["Rule"]).count(rule) == 1
print("PASS：SiriAI 紧接 Apple、默认 US，完整规则与模板引用有效，共70条规则")
