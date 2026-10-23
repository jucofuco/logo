"""Generate all pictograms and save each one as its own SVG file.

Usage:  python3 export.py
Output: preview.html (all pictograms on one page) and svg/<word>.svg
"""
import re, subprocess, sys, pathlib, unicodedata

here = pathlib.Path(__file__).parent
out = here / 'svg'
out.mkdir(exist_ok=True)
pages = []
for script in ('emotions_actions.py', 'food.py'):
    html = here / (script.replace('.py', '_preview.html'))
    subprocess.run([sys.executable, str(here / script), str(html)], check=True)
    pages.append(html.read_text(encoding='utf-8'))

def slug(word):
    s = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

count = 0
for page in pages:
    for m in re.finditer(r'<svg[^>]*aria-label="([^"]+)"[^>]*>.*?</svg>', page, re.S):
        word, svg = m.group(1), m.group(0)
        svg = svg.replace(' style="border:1px solid #ccc;overflow:hidden"', '')
        svg = svg.replace('width="240" height="240"', 'width="512" height="512"')
        svg = svg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        (out / f'{slug(word)}.svg').write_text(svg, encoding='utf-8')
        count += 1
(here / 'preview.html').write_text('\n'.join(pages), encoding='utf-8')
print(f'{count} SVG files written to {out}')
