"""Confirma o commit, o conteúdo inicial e HTTP 200 dos arquivos publicados."""

import json
import os
import time
from urllib.request import Request, urlopen

base = os.environ['SITE_URL'].rstrip('/') + '/'
commit = os.environ['SITE_COMMIT']


def fetch(path):
    request = Request(base + path + '?ci=' + commit,
                      headers={'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=15) as response:
        return response.read().decode('utf-8')


for attempt in range(1, 13):
    try:
        info = json.loads(fetch('build-info.json'))
        if info['commit'] != commit:
            raise ValueError('A publicação ainda não corresponde ao commit esperado')
        if 'Bem-vindo ao Projeto de Pull Request' not in fetch('index.html'):
            raise ValueError('Conteúdo esperado não encontrado')
        for file in info['files']:
            fetch(file)
        print(f"OK: commit {commit}; HTTP 200 em {len(info['files'])} arquivos; {base}")
        break
    except Exception as error:
        print(f'Tentativa {attempt}/12: {error}')
        if attempt == 12:
            raise SystemExit('Falha ao confirmar a publicação') from error
        time.sleep(10)
