"""Builds every pictogram into svg/<word id>.svg and writes preview.html.

Usage:  python3 pictograms/build.py               all sets, deletes stale SVGs, writes preview.html,
                                                  then builds style 2 into svg-v2/ the same way
        python3 pictograms/build.py toys clothes  only these sets (sets/toys.py ...), nothing else touched
        PICTO_STYLE=2 python3 pictograms/build.py ...   style 2 only (see kit.STYLE)
The preview shows all pictograms and lists the app's words that still have no pictogram.
"""
import importlib
import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
VOCABULARY = HERE.parent / 'logo' / 'Vocabulary'
sys.path.insert(0, str(HERE))

import kit  # noqa: E402

only = sys.argv[1:]
modules = only or sorted(m.stem for m in (HERE / 'sets').glob('*.py') if m.stem != '__init__')
for name in modules:
    importlib.import_module(f'sets.{name}')
if kit.STYLE == 2:
    # sets_v2/ may redraw single pictograms for style 2; those replace the shared drawing
    for m in sorted((HERE / 'sets_v2').glob('*.py')):
        if m.stem != '__init__':
            importlib.import_module(f'sets_v2.{m.stem}')
    kit.PICTOS.update(kit.PICTOS_V2)

out = HERE / ('svg' if kit.STYLE == 1 else 'svg-v2')
out.mkdir(exist_ok=True)
if only:
    for word_id, (label, draw) in kit.PICTOS.items():
        (out / f'{word_id}.svg').write_text(kit.svg(label, draw()), encoding='utf-8')
    print(f'{len(kit.PICTOS)} pictograms from {", ".join(only)} written to {out}')
    sys.exit()

for old in out.glob('*.svg'):
    if old.stem not in kit.PICTOS:
        old.unlink()  # a pictogram that was renamed or removed
for word_id, (label, draw) in kit.PICTOS.items():
    (out / f'{word_id}.svg').write_text(kit.svg(label, draw()), encoding='utf-8')
# The web app reads this to know which words have a pictogram (the others show their emoji).
(out / 'index.json').write_text(json.dumps(sorted(kit.PICTOS)), encoding='utf-8')
if kit.STYLE == 2:
    print(f'{len(kit.PICTOS)} style 2 pictograms written to {out}')
    sys.exit()

# Which app words and folder icons have a pictogram.
structure = json.loads((VOCABULARY / 'structure.json').read_text(encoding='utf-8'))
words = json.loads((VOCABULARY / 'words.sk.json').read_text(encoding='utf-8'))
app_ids = list(dict.fromkeys(structure['core'] + [w for f in structure['folders'] for w in f['words']]
                             + [f['icon'] for f in structure['folders'] if 'icon' in f]))
missing = [i for i in app_ids if i not in kit.PICTOS]
extra = [i for i in kit.PICTOS if i not in app_ids]


def card(word_id, label, body):
    return (f'<figure>{kit.svg(label, body, 160)}<figcaption><b>{label}</b><br>{word_id}</figcaption></figure>')


html = ['<!doctype html><meta charset="utf-8"><title>Pictograms</title><style>'
        'body{font:14px system-ui;margin:16px}.grid{display:flex;flex-wrap:wrap;gap:12px}'
        'figure{margin:0;width:160px;text-align:center}figure svg{border:1px solid #ccc;border-radius:12px}'
        'figcaption{color:#555;margin-top:4px}li{margin:2px 0}</style>',
        f'<h1>Pictograms ({len(kit.PICTOS)})</h1><div class="grid">',
        ''.join(card(i, label, draw()) for i, (label, draw) in kit.PICTOS.items()),
        '</div>',
        f'<h2>App words without a pictogram ({len(missing)} of {len(app_ids)})</h2><ul>',
        ''.join(f'<li>{words[i]["base"] if i in words else i} <small>({i})</small></li>' for i in missing),
        '</ul>',
        f'<h2>Pictograms not used by the app yet ({len(extra)})</h2><p>{", ".join(extra) or "none"}</p>']
(HERE / 'preview.html').write_text(''.join(html), encoding='utf-8')

print(f'{len(kit.PICTOS)} pictograms written to {out}')
print(f'{len(app_ids) - len(missing)} of {len(app_ids)} app words have a pictogram, {len(extra)} pictograms are not used yet')


# The same drawings again in style 2.
subprocess.run([sys.executable, __file__], env={**os.environ, 'PICTO_STYLE': '2'}, check=True)
