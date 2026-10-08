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
assert rules[0] == "PROTOCOL,STUN,REJECT", "首条规则未拦截 STUN"
assert rules.count("PROTOCOL,STUN,REJECT") == 1, "STUN 拦截规则重复"
assert rules[1:] == list(before["Rule"]), "其他规则内容或顺序改变"
assert current.sections() == before.sections(), "配置节改变"
for section in current.sections():
    if section != "Rule":
        assert list(current[section].items()) == list(before[section].items()), f"{section} 内容或顺序改变"
assert "{{" not in Path(sys.argv[1]).read_text(), "生成结果残留模板变量"

root = Path(__file__).resolve().parents[1]
external = configparser.ConfigParser(interpolation=None, strict=False)
external.read(root / "HappaConfig.ini")
assert external["template"]["stun_rule"] == rules[0], "INI 缺少完整 STUN 规则"
base = read_profile(root / "HappaConfig.conf")
assert list(base["Rule"])[0] == "{{ local.stun_rule }}", "CONF 未在首位引用 INI 规则"
print("PASS：INI 定义 STUN 拒绝规则，实际转换首位展开；其余规则、节点、分组与参数保持一致")
