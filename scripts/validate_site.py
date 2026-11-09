"""Validação de metadados e referências locais do site estático."""

from html.parser import HTMLParser
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.ids = set()
        self.language = False
        self.charset = False
        self.title = False
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.language = bool(attrs.get('lang'))
        if tag == 'meta':
            self.charset |= attrs.get('charset', '').lower() == 'utf-8'
        if tag == 'title':
            self.in_title = True
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.refs.append(attrs[key])

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.title = True


def validate(root):
    root = Path(root).resolve()
    errors = []
    pages = {}
    files = {p.name for p in root.iterdir() if p.is_file()}
    if 'index.html' not in files:
        errors.append('index.html: página inicial ausente')
    for file in sorted(root.glob('*.html')):
        page = Page()
        page.feed(file.read_text(encoding='utf-8'))
        pages[file.name] = page
        for present, label in ((page.language, 'idioma'),
                               (page.charset, 'charset UTF-8'), (page.title, 'título')):
            if not present:
                errors.append(f'{file.name}: falta {label}')
    refs = [(name, ref) for name, page in pages.items() for ref in page.refs]
    for file in sorted(root.glob('*.css')):
        css = re.sub(r'/\*.*?\*/', '', file.read_text(encoding='utf-8'), flags=re.S)
        refs.extend((file.name, ref.strip().strip('\"\''))
                    for ref in re.findall(r'url\(\s*(.*?)\s*\)', css))
    for source, reference in refs:
        url = urlsplit(reference)
        if url.hostname in ('localhost', '127.0.0.1', '0.0.0.0', '::1'):
            errors.append(f'{source}: link local de desenvolvimento: {reference}')
            continue
        if url.scheme or url.netloc:
            continue  # Não depende da disponibilidade de sites externos.
        if url.path.startswith('/'):
            errors.append(f'{source}: caminho absoluto incompatível com Pages: {reference}')
            continue
        path = unquote(url.path) or source
        name = posixpath.normpath(path)
        target = (root / path).resolve()
        # Os arquivos públicos deste projeto ficam todos na raiz.
        if target.parent != root or name not in files:
            errors.append(f'{source}: destino ausente ou capitalização incorreta: {reference}')
        elif url.fragment and name in pages:
            if unquote(url.fragment) not in pages[name].ids:
                errors.append(f'{source}: âncora ausente: {reference}')
    return errors, len(pages), len(refs)


if __name__ == '__main__':
    errors, pages, refs = validate(ROOT)
    if errors:
        print('\n'.join('ERRO: ' + error for error in errors))
        sys.exit(1)
    print(f'OK: {pages} páginas e {refs} referências locais verificadas.')
