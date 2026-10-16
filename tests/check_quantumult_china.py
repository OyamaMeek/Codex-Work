from collections import Counter
from pathlib import Path
import ipaddress
import subprocess

root = Path(__file__).resolve().parents[1]
source = root / 'quantumult_20261016155506.conf'
cache = root / '.agent/china-rules'
policies = {'NetEaseMusic', '大陆流媒体', '大陆网站', '国内流媒体', 'Speedtest', 'direct'}
types = {'host': 'DOMAIN', 'host-suffix': 'DOMAIN-SUFFIX',
         'host-keyword': 'DOMAIN-KEYWORD', 'host-wildcard': 'DOMAIN-WILDCARD',
         'ip-cidr': 'IP-CIDR', 'ip6-cidr': 'IP-CIDR6', 'ip-asn': 'IP-ASN',
         'geoip': 'GEOIP', 'user-agent': 'USER-AGENT'}


def convert(line):
    fields = [part.strip() for part in line.split('//', 1)[0].split(',')]
    kind = types[fields[0].lower()]
    value = fields[1]
    assert value, line
    if kind.startswith('DOMAIN'):
        value = value.lower()
        if kind == 'DOMAIN' and '*' in value:
            kind = 'DOMAIN-WILDCARD'
    if kind in {'IP-CIDR', 'IP-CIDR6'}:
        ipaddress.ip_network(value)
    if kind == 'IP-ASN':
        assert value.isdigit(), line
    if kind == 'GEOIP':
        value = value.upper()
    return f'{kind},{value}'


expected = set()
counts = Counter()
urls = []
section = ''
for line in source.read_text().splitlines():
    line = line.strip()
    if line.startswith('['):
        section = line
    elif section == '[filter_remote]' and line.startswith('https://'):
        fields = [part.strip() for part in line.split(',')]
        options = dict(part.split('=', 1) for part in fields[1:] if '=' in part)
        if options.get('force-policy') not in policies or options.get('enabled') != 'true':
            continue
        name = options['force-policy']
        urls.append(fields[0])
        for row in (cache / f'{name}.list').read_text().splitlines():
            if row.strip() and not row.startswith(('#', ';', '//')):
                expected.add(convert(row))
                counts[name] += 1
    elif section == '[filter_local]' and line and not line.startswith(('#', ';', '//')):
        if line.split(',')[-1].strip() in policies:
            expected.add(convert(line))
            counts['本地'] += 1

assert len(urls) == 4, urls
baseline_text = subprocess.check_output(['git', 'show', 'd18312e:China.list'], cwd=root, text=True)
baseline = {line for line in baseline_text.splitlines() if line and not line.startswith('#')}
actual_text = (root / 'China.list').read_text()
actual = [line for line in actual_text.splitlines() if line and not line.startswith('#')]
assert len(actual) == len(set(actual)), '重复规则'
assert actual == sorted(actual), '规则未排序'
assert set(actual) == baseline | expected, f'缺少 {len((baseline | expected) - set(actual))} 条规则'
assert 'FINAL' not in {line.split(',')[0] for line in actual}
print(f'通过：4个远程集合、本地{counts["本地"]}条，提取{len(expected)}条唯一规则，输出{len(actual)}条')
print(dict(counts))
