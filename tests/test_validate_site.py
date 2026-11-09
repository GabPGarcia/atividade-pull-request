"""Comprova que erros reais de publicação são rejeitados pela CI."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_site import validate


class SiteValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def page(self, reference='style.css'):
        (self.root / 'index.html').write_text(
            '<html lang="pt-BR"><head><meta charset="UTF-8">'
            '<title>Teste</title></head><body>'
            f'<a href="{reference}">Link</a><h1 id="inicio">Olá</h1></body></html>',
            encoding='utf-8')
        (self.root / 'style.css').write_text('body { color: black; }', encoding='utf-8')

    def test_valid_site(self):
        self.page()
        self.assertEqual(validate(self.root)[0], [])

    def test_missing_file(self):
        self.page('ausente.html')
        self.assertTrue(any('destino ausente' in error for error in validate(self.root)[0]))

    def test_wrong_case_even_on_windows(self):
        self.page('STYLE.css')
        self.assertTrue(validate(self.root)[0])

    def test_localhost_rejected(self):
        self.page('http://127.0.0.1:5500/index.html')
        self.assertTrue(any('desenvolvimento' in error for error in validate(self.root)[0]))

    def test_missing_anchor(self):
        self.page('#ausente')
        self.assertTrue(any('âncora' in error for error in validate(self.root)[0]))

    def test_valid_anchor(self):
        self.page('#inicio')
        self.assertEqual(validate(self.root)[0], [])

    def test_css_missing_image(self):
        self.page()
        (self.root / 'style.css').write_text('body { background: url(missing.png); }')
        self.assertTrue(validate(self.root)[0])


if __name__ == '__main__':
    unittest.main()
