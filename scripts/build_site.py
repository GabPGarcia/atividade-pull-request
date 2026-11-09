"""Empacota somente os HTML/CSS do projeto, sem scripts nem documentação."""

import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '_site'
OUTPUT.mkdir(exist_ok=True)
files = sorted([*ROOT.glob('*.html'), *ROOT.glob('*.css')])
for file in files:
    shutil.copy2(file, OUTPUT / file.name)
(OUTPUT / '.nojekyll').touch()
(OUTPUT / 'build-info.json').write_text(json.dumps({
    'commit': os.environ.get('SITE_COMMIT', 'local'),
    'files': [file.name for file in files],
}) + '\n', encoding='utf-8')
print(f'OK: {len(files)} arquivos públicos preparados em _site.')
