import json
from pathlib import Path
import re
import sys

source = Path(sys.argv[1])
output = Path(sys.argv[2])
manifest = json.loads((source / 'manifest.json').read_text())
assert re.fullmatch(r'[0-9a-f]{40}', manifest['revision'])
assert {'cn.list', 'geolocation-cn.list', 'tld-cn.list'} <= set(manifest['sources'])
expected = set()
for name in manifest['sources']:
    for line in (source / name).read_text().splitlines():
        value = line.strip()
        if not value or value.startswith('#'):
            continue
        suffix = value.startswith('+.')
        domain = value[2:] if suffix else value
        assert re.fullmatch(r'[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*', domain), (name, value)
        expected.add(('DOMAIN-SUFFIX' if suffix else 'DOMAIN') + ',' + domain)
text = output.read_text()
actual = [line for line in text.splitlines() if line and not line.startswith('#')]
assert len(actual) == len(set(actual)), '重复规则'
assert set(actual) == expected, '规则与完整源集合不一致'
assert actual == sorted(actual), '规则未排序'
assert manifest['revision'] in text, '缺少来源版本'
assert 'DOMAIN-SUFFIX,qq.com' in actual
assert 'DOMAIN-SUFFIX,baidu.com' in actual
assert 'DOMAIN-SUFFIX,cn' in actual
print(f'通过：{len(manifest["sources"])} 个源集合，{len(actual)} 条唯一规则，完整覆盖与匹配类型一致')
