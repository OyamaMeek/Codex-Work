import configparser
from pathlib import Path
import sys

expected = dict.fromkeys([
    "Emby", "Global Media", "Netflix", "TikTok", "Disney", "Social Media",
    "Spotify", "OpenAI", "Apple", "Global", "Google Voice", "SpeedTest", "China", "Final",
], "All Proxies")
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
        assert groups[name].split(",")[2:] == baseline["Proxy Group"][name].split(",")[1:], f"{name} 未保留其余候选成员与顺序"
assert list(config["Rule"]) == list(baseline["Rule"]), "原规则或顺序改变"
print(f"PASS：14个用途组均新增并默认选择 All Proxies，原候选与{len(nodes)}个真实节点的顺序保留")
