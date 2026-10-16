import json
import re
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

root = Path("HDU/大一上数学分析备考/分节练习")
pdf_path = root / "分节课后练习-iPad横屏草稿版.pdf"
knowledge_path = root / "分节知识点.tex"
source = (root / "分节课后练习.tex").read_text()
assert pdf_path.is_file(), "缺少iPad横屏PDF"
assert knowledge_path.is_file(), "缺少分节知识清单"
knowledge = knowledge_path.read_text()
for name, content in [("题目", source), ("知识点", knowledge)]:
    assert not any("/" in formula for formula in re.findall(r"\$([^$]*)\$", content)), (name, "数学比值仍使用斜杠")
entries = re.findall(r"\\knowledge\{([\d.]+)\}", knowledge)
assert len(entries) == len(set(entries)) == 85

reader = PdfReader(pdf_path)
expected_ids = []
expected_titles = []
expected_prompts = []
chapter = section = subsection = 0
for line in source.splitlines():
    if line.startswith(r"\chapter{"):
        chapter += 1
        section = 0
    elif line.startswith(r"\section{"):
        section += 1
        subsection = 0
    elif line.startswith(r"\subsection{"):
        subsection += 1
        key = f"{chapter}.{section}.{subsection}"
        expected_titles.append((key, line[len(r"\subsection{"):-1]))
        expected_ids.extend(f"题号 {key}-{i}" for i in range(1, 6))
    elif line.startswith(r"\item "):
        expected_prompts.append(re.findall(r"[\u4e00-\u9fff]{2,}", line))
assert entries == [key for key, _ in expected_titles]
assert len(expected_prompts) == 425

question_pages = []
knowledge_pages = []
minimum_blank = 1000
with pdfplumber.open(pdf_path) as document:
    for page_number, page in enumerate(document.pages, 1):
        assert abs(page.width / page.height - 4 / 3) < 5e-5
        assert abs(page.width - 240 * 72 / 25.4) < 0.1
        assert abs(page.height - 180 * 72 / 25.4) < 0.1
        text = page.extract_text() or ""
        compact = re.sub(r"\s+", "", text)
        assert "iPad横屏练习" not in compact, (page_number, "右上角页眉尚未删除")
        ids = re.findall(r"题号\s*(\d+\.\d+\.\d+-[1-5])", text)
        assert len(ids) <= 1, (page_number, ids)
        if ids:
            assert "重要知识点" not in compact
            if ids == ["1.2.1-3"]:
                assert "/" not in text
                assert any(line["width"] > 20 and 95 < line["top"] < 180 for line in page.lines), "示例题未生成横向分数线"
            chinese = "".join(re.findall(r"[\u4e00-\u9fff]", text))
            assert all(fragment in chinese for fragment in expected_prompts[len(question_pages)]), (page_number, ids)
            body = [c for c in page.chars if 28 < c["top"] < page.height - 25]
            assert body, page_number
            blank = page.height - 25 - max(c["bottom"] for c in body)
            assert blank >= 90 * 72 / 25.4, (page_number, blank * 25.4 / 72)
            minimum_blank = min(minimum_blank, blank * 25.4 / 72)
            assert not page.images and not page.rects and not page.curves
            assert all(line["top"] < page.height - 25 - blank or line["top"] >= page.height - 25 for line in page.lines)
            question_pages.append((page_number, f"题号 {ids[0]}"))
        if "重要知识点" in compact and "需要掌握" in compact:
            knowledge_pages.append((page_number, compact))
assert [key for _, key in question_pages] == expected_ids
assert len(knowledge_pages) == 85
def normalized_title(value):
    return value.replace("--", "–").replace("'", "’")

for (page_number, text), (key, title) in zip(knowledge_pages, expected_titles):
    assert key in text and normalized_title(title) in text, (page_number, key, title)
    assert [n for n, _ in question_pages if page_number < n < page_number + 6] == list(range(page_number + 1, page_number + 6))

destinations = []
destination_pages = {}
def read_outline(items):
    for item in items:
        if isinstance(item, list):
            read_outline(item)
        else:
            destinations.append(str(item["/Title"]))
            destination_pages[normalized_title(str(item["/Title"]))] = reader.get_destination_page_number(item) + 1
read_outline(reader.outline)
assert len(destinations) == 4 + 20 + 85 + 425, len(destinations)
for page_number, key in question_pages:
    question_id = key.removeprefix("题号 ")
    matching = [title for title in destinations if title.startswith(question_id + " ")]
    assert len(matching) == 1 and destination_pages[matching[0]] == page_number
for (page_number, _), (key, title) in zip(knowledge_pages, expected_titles):
    assert destination_pages[normalized_title(f"{key} {title}")] == page_number
first_pages = {key: page_number for (page_number, _), (key, _) in zip(knowledge_pages, expected_titles)}
for title in destinations:
    chapter_match = re.match(r"第(\d+)章", title)
    section_match = re.match(r"(\d+\.\d+) ", title)
    if chapter_match:
        assert destination_pages[normalized_title(title)] == first_pages[f"{chapter_match[1]}.1.1"]
    elif section_match:
        assert destination_pages[normalized_title(title)] == first_pages[f"{section_match[1]}.1"]
assert len(reader.pages) == 1 + 85 + 425
result = {"status": "passed", "pages": len(reader.pages), "questions": 425,
          "knowledge_pages": 85, "bookmarks": len(destinations),
          "size_mm": [240, 180], "minimum_blank_mm": round(minimum_blank, 1),
          "bytes": pdf_path.stat().st_size,
          "scope": "PDF文字、页面坐标、页数及书签；未做截图或图像检查"}
print(json.dumps(result, ensure_ascii=False))
