from pathlib import Path

root = Path(__file__).resolve().parents[1]
groups = dict(
    (parts[0], parts[2:])
    for line in (root / "HappaConfig.ini").read_text().splitlines()
    if line.startswith("custom_proxy_group=")
    for parts in [line.split("=", 1)[1].split("`")]
)
expected = dict.fromkeys([
    "Emby", "Global Media", "Netflix", "TikTok", "Disney", "Social Media",
    "Spotify", "OpenAI", "Global", "SpeedTest", "Final",
], "[]Proxy")
expected.update({
    "Proxy": "[]All Proxies", "Google Voice": "[]US",
    "Apple": "[]DIRECT", "China": "[]DIRECT",
    "Claude": "[]US", "SiriAI": "[]US",
})
for name, first in expected.items():
    assert groups[name][0] == first, f"{name} 默认项应为 {first}"
for name, members in groups.items():
    assert len(members) == len(set(members)), f"{name} 存在重复候选"
    for member in members:
        if member.startswith("[]"):
            assert member[2:] in groups or member == "[]DIRECT", f"{name} 引用未定义策略"


def check_cycles(name, ancestors):
    assert name not in ancestors, f"策略组循环引用：{name}"
    for member in groups[name]:
        if member.startswith("[]") and member[2:] in groups:
            check_cycles(member[2:], ancestors | {name})


for name in groups:
    check_cycles(name, set())
print("PASS：17组默认项、候选唯一性、策略引用与无循环检查通过")
