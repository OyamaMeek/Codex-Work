import configparser
from pathlib import Path
import sys

expected = {
    "Proxy": "Manual",
    "Manual": "🇯🇵 JP-GreenCloud-3",
    "All Proxies": "🇯🇵 JP-zgo-2",
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
    "JP": "🇯🇵 JP-GreenCloud-3",
    "US": "🇺🇸 US-DMIT-3",
    "International": "🇬🇧 UK-GreenCloud-3",
}
config = configparser.ConfigParser(interpolation=None, allow_no_value=True, delimiters=("=",), comment_prefixes=("#", ";", "//"))
config.optionxform = str
config.read_string(Path(sys.argv[1]).read_text())
groups = config["Proxy Group"]
assert [name for name in groups if name in expected] == list(expected), "分组展示顺序与截图要求不一致"
nodes = {name for name, value in config["Proxy"].items() if value.strip().upper() != "DIRECT"}
policies = set(groups) | set(config["Proxy"]) | {"DIRECT", "REJECT"}
for name, selected in expected.items():
    members = [member.strip() for member in groups[name].split(",")[1:]]
    assert members[0] == selected, f"{name} 默认选项为 {members[0]}，预期 {selected}"
    assert len(members) == len(set(members)), f"{name} 存在重复成员"
    assert set(members) <= policies, f"{name} 引用未定义策略"
    if name in {"Manual", "All Proxies"}:
        assert set(members) == nodes, f"{name} 未保留全部节点"
print(f"PASS：20组默认选项、展示顺序、成员引用与去重检查通过，Manual / All Proxies 均保留{len(nodes)}个真实节点")
