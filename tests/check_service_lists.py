from pathlib import Path
import sys


def expected_rules(source):
    types = {'HOST': 'DOMAIN', 'HOST-SUFFIX': 'DOMAIN-SUFFIX',
             'HOST-KEYWORD': 'DOMAIN-KEYWORD', 'HOST-WILDCARD': 'DOMAIN-WILDCARD',
             'USER-AGENT': 'USER-AGENT'}
    result = set()
    for line in source.read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        kind, value, policy = [field.strip() for field in line.split(',')]
        assert policy == source.stem, line
        kind = types[kind]
        result.add(kind + ',' + (value if kind == 'USER-AGENT' else value.lower()))
    return result


if __name__ == '__main__':
    source_dir = Path(sys.argv[1])
    root = Path(__file__).resolve().parents[1]
    for name in ('Microsoft', 'PayPal'):
        expected = expected_rules(source_dir / f'{name}.list')
        text = (root / f'{name}.list').read_text()
        actual = [line for line in text.splitlines() if line and not line.startswith('#')]
        assert len(actual) == len(set(actual)), f'{name} 重复规则'
        assert actual == sorted(expected), f'{name} 来源覆盖、类型或顺序不一致'
        assert all(len(line.split(',')) == 2 for line in actual), f'{name} 包含策略字段'
        assert any(line.startswith('USER-AGENT,') for line in actual)
        print(f'{name}：通过，{len(actual)} 条唯一规则，完整覆盖来源、格式和排序正确')
