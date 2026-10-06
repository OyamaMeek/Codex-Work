import configparser
from pathlib import Path
import sys
from urllib.parse import urlsplit


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
general = current["General"]
servers = [urlsplit(value.strip()) for value in general["encrypted-dns-server"].split(",")]
assert servers and all(server.scheme == "tls" for server in servers), "DNS 未全部使用 DoT"
assert {server.hostname for server in servers} == {"1.1.1.1", "1.0.0.1"}, "DoT 应使用 Cloudflare IP 端点，避免引导域名查询"
assert general["dns-server"].replace(" ", "") == "1.1.1.1,1.0.0.1", "传统 DNS 包含系统或大陆服务器"
assert general["encrypted-dns-follow-outbound-mode"] == "true", "DoT 未跟随代理规则"
assert general["encrypted-dns-skip-cert-verification"] == "false", "DoT 证书验证未开启"
assert general["hijack-dns"] == "*:53", "硬编码53端口 DNS 未被接管"
assert not any("server:" in value for value in current["Host"].values()), "Host 中仍有绕过统一 DNS 的服务器映射"
assert dict(current["Host"]) == {"mtalk.google.com": "108.177.125.188"}, "固定 IP 映射改变"
assert list(current["Rule"])[0] == "PROTOCOL,DOT,All Proxies", "DoT 未优先交给 All Proxies"
assert list(current["Rule"])[1:] == list(before["Rule"]), "其他分流规则或顺序改变"
changed = {"dns-server", "encrypted-dns-server", "encrypted-dns-follow-outbound-mode", "encrypted-dns-skip-cert-verification", "hijack-dns"}
assert {key: value for key, value in general.items() if key not in changed} == {key: value for key, value in before["General"].items() if key not in changed}, "范围外 General 参数改变"
for section in ("Proxy", "Proxy Group", "MITM", "Script"):
    assert list(current[section].items()) == list(before[section].items()), f"{section} 内容或顺序改变"
assert "{{" not in Path(sys.argv[1]).read_text(), "转换结果残留模板变量"
print("PASS：DoT 使用 Cloudflare IP 端点、优先代理、校验证书，未配置大陆或系统 DNS；其他分流和节点保持一致")
