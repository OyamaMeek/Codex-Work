import configparser
from pathlib import Path
import sys

expected = {
    "Emby": "DIRECT",
    "Global Media": "Proxy",
    "Netflix": "Manual",
    "TikTok": "Manual",
    "Disney": "Manual",
    "Social Media": "Manual",
    "Spotify": "HK",
    "OpenAI": "Manual",
    "Apple": "DIRECT",
    "Global": "Manual",
    "Google Voice": "US",
    "SpeedTest": "Manual",
    "China": "DIRECT",
    "Final": "Proxy",
}
config = configparser.ConfigParser(interpolation=None, allow_no_value=True, delimiters=("=",), comment_prefixes=("#", ";", "//"))
config.optionxform = str
config.read_string(Path(sys.argv[1]).read_text())
groups = config["Proxy Group"]
assert list(groups)[:4] == ["Proxy", "Manual", "All Proxies", "Emby"], "All Proxies 未紧接 Manual、位于 Emby 前"
assert [name for name in groups if name in expected] == list(expected), "分组展示顺序与截图要求不一致"
nodes = {name for name, value in config["Proxy"].items() if value.strip().upper() != "DIRECT"}
policies = set(groups) | set(config["Proxy"]) | {"DIRECT", "REJECT"}
for name, selected in expected.items():
    members = [member.strip() for member in groups[name].split(",")[1:]]
    assert members[0] == selected, f"{name} 默认选项为 {members[0]}，预期 {selected}"
    assert len(members) == len(set(members)), f"{name} 存在重复成员"
    assert set(members) <= policies, f"{name} 引用未定义策略"
baseline = configparser.ConfigParser(interpolation=None, allow_no_value=True, delimiters=("=",), comment_prefixes=("#", ";", "//"))
baseline.optionxform = str
baseline.read_string(Path(sys.argv[2]).read_text())
assert dict(config["Proxy"]) == dict(baseline["Proxy"]), "原节点定义改变"
for name in groups:
    if name not in expected:
        assert groups[name] == baseline["Proxy Group"][name], f"{name} 的候选顺序或默认项改变"
    else:
        assert set(groups[name].split(",")) == set(baseline["Proxy Group"][name].split(",")), f"{name} 的候选成员改变"
assert list(config["Rule"]) == list(baseline["Rule"]), "原规则或顺序改变"
print(f"PASS：截图14组默认项与 All Proxies 位置正确，其余组及{len(nodes)}个真实节点的原顺序保留")
