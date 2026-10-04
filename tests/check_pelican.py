from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.external_resources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("src", "href"):
            value = attrs.get(key, "")
            if value and not value.startswith("#"):
                self.external_resources.append((tag, value))


root = Path(__file__).resolve().parents[1]
source = (root / "pelican-ride.html").read_text()
document = Document()
document.feed(source)
assert not document.external_resources, document.external_resources
svg_source = re.search(r"<svg\b[\s\S]*</svg>", source).group()
svg = ET.fromstring(svg_source)
ids = [node.attrib["id"] for node in svg.iter() if "id" in node.attrib]
assert len(ids) == len(set(ids)), "SVG ID 必须唯一"
for reference in re.findall(r'(?:href="#|url\(#)([\w-]+)', svg_source):
    assert reference in ids, f"无效 SVG 引用：{reference}"
assert svg.attrib["viewBox"] == "0 0 1200 760"
assert svg.attrib.get("role") == "img"
for required in ("rear-spokes", "front-spokes", "leg-near", "leg-far", "crank", "rider"):
    assert required in ids, required
assert "prefers-reduced-motion" in source
assert "requestAnimationFrame" in source
assert not re.search(r"@import|https?://", source.replace('xmlns="http://www.w3.org/2000/svg"', ""))
script = re.search(r"<script>([\s\S]*?)</script>", source).group(1)
result = subprocess.run(
    ["node", "--check"], input=script, text=True, capture_output=True
)
assert result.returncode == 0, result.stderr
print("PASS：离线资源、SVG XML、唯一 ID、图形引用、可访问描述与脚本语法")
