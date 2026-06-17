from pathlib import Path
import re

path = Path("src/app/home/home.html")
html = path.read_text(encoding="utf-8")

section_pattern = re.compile(
    r"<section\b[^>]*>[\s\S]*?(?=\n\s*<section\b|\n\s*</main>)",
    re.IGNORECASE
)

def set_section_id(opening_tag: str, new_id: str) -> str:
    if re.search(r'\sid="[^"]*"', opening_tag):
        return re.sub(r'\sid="[^"]*"', f' id="{new_id}"', opening_tag, count=1)
    return opening_tag.replace("<section", f'<section id="{new_id}"', 1)

new_html_parts = []
last = 0
changed = []

for match in section_pattern.finditer(html):
    block = match.group(0)
    opening_match = re.match(r"<section\b[^>]*>", block, re.IGNORECASE)

    if not opening_match:
        continue

    opening_tag = opening_match.group(0)
    new_opening_tag = opening_tag

    # A seção que tem o título "Diferenciais" precisa ter id="diferenciais"
    if re.search(r"<h[1-6][^>]*>\s*Diferenciais\s*</h[1-6]>", block, re.IGNORECASE):
        new_opening_tag = set_section_id(opening_tag, "diferenciais")
        changed.append("Diferenciais -> id=diferenciais")

    # A seção que tem o título "Cafeteria" precisa ter id="cafeteria"
    elif re.search(r"<h[1-6][^>]*>\s*Cafeteria\s*</h[1-6]>", block, re.IGNORECASE):
        new_opening_tag = set_section_id(opening_tag, "cafeteria")
        changed.append("Cafeteria -> id=cafeteria")

    new_block = block.replace(opening_tag, new_opening_tag, 1)

    new_html_parts.append(html[last:match.start()])
    new_html_parts.append(new_block)
    last = match.end()

new_html_parts.append(html[last:])
new_html = "".join(new_html_parts)

path.write_text(new_html, encoding="utf-8")

print("OK: IDs corrigidos.")
for item in changed:
    print("-", item)
