"""Screenshots of the web app at iPhone size, made with headless Chromium in Docker.

Usage:  python3 web/screenshot.py [name=query ...]
        python3 web/screenshot.py main= toys=folder=toys sentence=sentence=me,want,ball
Needs the server running on port 8500 and the image: docker build -t logo-web-screenshot web/docker
Writes web/shots/<name>.png (git-ignored).
"""
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
shots = HERE / 'shots'
shots.mkdir(exist_ok=True)
pages = [a.split('=', 1) for a in sys.argv[1:]] or [['main', '']]
for name, query in pages:
    url = 'http://localhost:8500/' + (f'?{query}' if query else '')
    subprocess.run(['docker', 'run', '--rm', '--network', 'host', '-u', f'{os.getuid()}:{os.getgid()}',
                    '-e', 'HOME=/tmp', '-v', f'{shots}:/out', 'logo-web-screenshot',
                    'chromium', '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                    '--window-size=390,844', '--force-device-scale-factor=2', '--virtual-time-budget=4000',
                    f'--screenshot=/out/{name}.png', url],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(shots / f'{name}.png')
