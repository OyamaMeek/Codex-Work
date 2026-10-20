import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from pylatexenc.latexwalker import LatexEnvironmentNode, LatexMacroNode, LatexMathNode, LatexWalker, get_default_latex_context_db
from pylatexenc.macrospec import EnvironmentSpec

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'output/大一数学分析期末复习-上册'
CONTEXT = get_default_latex_context_db()
CONTEXT.add_context_category('exercise', environments=[EnvironmentSpec('exercise', '{{')], prepend=True)
manifest = json.loads((FOLDER / '题目清单.json').read_text())
questions = []
sections = 0
limits = 0
fractions = 0


def inspect(nodes):
    global limits, fractions
    for node in nodes or []:
        if isinstance(node, LatexMathNode):
            assert '/' not in node.latex_verbatim(), node.latex_verbatim()
        if isinstance(node, LatexMacroNode):
            limits += node.macroname == 'lim'
            fractions += node.macroname in ('frac', 'dfrac', 'tfrac')
        inspect(getattr(node, 'nodelist', None))
        arguments = getattr(node, 'nodeargd', None)
        if arguments:
            inspect([arg for arg in arguments.argnlist if arg is not None])


for chapter, expected in enumerate((150, 138, 135, 133, 104, 60, 110), 1):
    relative = f'chapters/ch{chapter:02}.tex'
    source = (FOLDER / relative).read_text()
    nodes, position, length = LatexWalker(source, latex_context=CONTEXT, tolerant_parsing=False).get_latex_nodes()
    assert position == 0 and length == len(source), relative
    inspect(nodes)
    chapter_questions = 0
    for node in nodes:
        if isinstance(node, LatexMacroNode) and node.macroname == 'subsection':
            sections += 1
        if isinstance(node, LatexEnvironmentNode) and node.environmentname == 'exercise':
            number, direction = [arg.latex_verbatim()[1:-1] for arg in node.nodeargd.argnlist]
            body = ''.join(child.latex_verbatim() for child in node.nodelist).strip()
            row = manifest['questions'][len(questions)]
            assert (int(number), direction, relative, source.count('\n', 0, node.pos) + 1) == (
                row['number'], row['direction'], row['file'], row['line'])
            assert hashlib.sha256(body.encode()).hexdigest() == row['body_sha256'], number
            questions.append(int(number))
            chapter_questions += 1
    assert chapter_questions == expected, (relative, chapter_questions)

assert questions == list(range(1, 831))
assert sections == manifest['sections'] == 40
assert manifest['level_counts'] == {'基础': 412, '常规': 418}
inputs = [f'\\input{{chapters/ch{chapter:02}.tex}}' for chapter in range(1, 8)]
for entry in ('main.tex', 'ipad.tex'):
    source = (FOLDER / entry).read_text()
    assert '\\everymath{\\displaystyle}' in source, entry
    assert [line for line in source.splitlines() if line.startswith('\\input{')] == inputs
    _, position, length = LatexWalker(source, tolerant_parsing=False).get_latex_nodes()
    assert position == 0 and length == len(source), entry

with ZipFile(FOLDER / '大一数学分析期末复习-上册-LaTeX源码.zip') as archive:
    assert archive.testzip() is None
    assert len(archive.infolist()) == 12
    for item in archive.infolist():
        relative = Path(item.filename).relative_to(FOLDER.name)
        assert item.flag_bits & 0x800, item.filename
        assert archive.read(item.filename) == (FOLDER / relative).read_bytes(), item.filename

print(json.dumps({'status': 'passed', 'questions': len(questions), 'sections': sections,
                  'fractions': fractions, 'limits': limits, 'zip_members': 12}, ensure_ascii=False))
