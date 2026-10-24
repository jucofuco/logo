"""Exports every pictogram set as PNG for the iOS app: Pictograms/<set>/<word id>.png in the repo root.

Usage:  python3 pictograms/export_png.py       (run build.py first so the svg folders are current)
The iOS app bundles the Pictograms/ folder (project.yml) and shows the set picked in Settings.
320 px is enough for 3x screens (a card picture is about 100 pt), the palette compression (pngquant)
makes the files about 6 KB each with no visible difference. Needs the Docker image:
        docker build -t logo-pictogram-render pictograms/docker
"""
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
# iOS folder -> svg folder in pictograms/
SETS = {'v1': 'svg', 'v2': 'svg-v2', 'mulberry': 'svg-mulberry'}

commands = []
for name, svg_dir in SETS.items():
    out = ROOT / 'Pictograms' / name
    out.mkdir(parents=True, exist_ok=True)
    ids = {p.stem for p in (ROOT / 'pictograms' / svg_dir).glob('*.svg')}
    for old in out.glob('*.png'):
        if old.stem not in ids:
            old.unlink()   # a pictogram that no longer exists
    commands.append(
        f'for f in pictograms/{svg_dir}/*.svg; do b=$(basename $f .svg); '
        f'rsvg-convert -a -w 320 -h 320 $f -o /tmp/$b.png && '
        f'pngquant --quality=85-100 --speed 1 --strip --force /tmp/$b.png -o Pictograms/{name}/$b.png; done')

subprocess.run(['docker', 'run', '--rm', '-u', f'{os.getuid()}:{os.getgid()}', '-e', 'XDG_CACHE_HOME=/tmp',
                '-v', f'{ROOT}:/w', 'logo-pictogram-render', 'sh', '-c', ' && '.join(commands)], check=True)
for name in SETS:
    files = list((ROOT / 'Pictograms' / name).glob('*.png'))
    print(f'Pictograms/{name}: {len(files)} files, {sum(f.stat().st_size for f in files) // 1024} KB')
