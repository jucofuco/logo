"""Renders pictograms to PNG (in Docker, with rsvg-convert) so they can be looked at as images.

Usage:  python3 pictograms/render.py ball doll          -> png/ball.png, png/doll.png (256 px)
        python3 pictograms/render.py --sheet toys ball doll ...   -> also png/sheet-toys.png, all in one grid
Run build.py first so svg/ is up to date. The Docker image is built once with:
        docker build -t logo-pictogram-render pictograms/docker
"""
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
IMAGE = 'logo-pictogram-render'
args = sys.argv[1:]
sheet = None
if args[:1] == ['--sheet']:
    sheet, args = args[1], args[2:]
if not args:
    sys.exit(__doc__)

(HERE / 'png').mkdir(exist_ok=True)
missing = [i for i in args if not (HERE / 'svg' / f'{i}.svg').exists()]
if missing:
    sys.exit(f'no svg for: {", ".join(missing)} (run build.py first)')

commands = [f'rsvg-convert -w 256 -h 256 -b white svg/{i}.svg -o png/{i}.png' for i in args]

if sheet:
    # One grid of all given pictograms with their ids, to judge them side by side.
    cols, cell, label = 6, 180, 22
    rows = (len(args) + cols - 1) // cols
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols * cell}" height="{rows * (cell + label)}">'
             f'<rect width="100%" height="100%" fill="white"/>']
    for n, i in enumerate(args):
        x, y = (n % cols) * cell, (n // cols) * (cell + label)
        body = (HERE / 'svg' / f'{i}.svg').read_text(encoding='utf-8')
        body = re.sub(r'width="\d+" height="\d+"', f'x="{x + 10}" y="{y + 10}" width="{cell - 20}" height="{cell - 20}"', body, count=1)
        parts.append(f'<rect x="{x + 9}" y="{y + 9}" width="{cell - 18}" height="{cell - 18}" fill="none" stroke="#ccc"/>{body}'
                     f'<text x="{x + cell / 2}" y="{y + cell + 12}" font-family="sans-serif" font-size="14" text-anchor="middle">{i}</text>')
    parts.append('</svg>')
    (HERE / 'png' / f'sheet-{sheet}.svg').write_text(''.join(parts), encoding='utf-8')
    commands.append(f'rsvg-convert png/sheet-{sheet}.svg -o png/sheet-{sheet}.png && rm png/sheet-{sheet}.svg')

subprocess.run(['docker', 'run', '--rm', '-u', f'{os.getuid()}:{os.getgid()}', '-e', 'XDG_CACHE_HOME=/tmp', '-v', f'{HERE}:/w', IMAGE,
                'sh', '-c', ' && '.join(commands)], check=True)
print('\n'.join(str(HERE / 'png' / f'{i}.png') for i in args))
if sheet:
    print(HERE / 'png' / f'sheet-{sheet}.png')
