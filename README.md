# Atividade Pull Request

Projeto colaborativo de páginas HTML/CSS para praticar branches, commits e pull requests.

- **Site:** https://gabpgarcia.github.io/atividade-pull-request/
- **Pipeline:** [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)
- **Registro da atividade:** [docs/atividade-ci-cd.md](docs/atividade-ci-cd.md)

## CI/CD

A CI executa em todo `push` na `main` e em `pull_request` destinado à `main`.
Configura Python 3.12, executa sete testes do validador, verifica as cinco páginas
HTML e suas referências locais e prepara um artefato com os HTML/CSS públicos.
Todos os scripts usam a biblioteca padrão: não há pacotes a instalar.

O job de CD tem `needs: ci` e só executa em pushes na `main`. Publica o mesmo
artefato aprovado pela CI no GitHub Pages com autenticação OIDC e permissões
`pages: write` e `id-token: write`. Em PRs, o CD é ignorado. Depois do deployment,
o teste HTTP confirma o SHA publicado em `build-info.json`, o conteúdo da página
inicial e o acesso aos sete arquivos HTML/CSS.

A configuração inicial de Settings > Pages > Source é **GitHub Actions**.
O site não precisa de backend, compilação ou servidor próprio, por isso o Pages
é adequado. Os formulários de login e contato são demonstrativos; a hospedagem
estática não implementa autenticação ou envio de mensagens.

## Execução local

Na raiz do repositório, com Python 3.12 ou posterior:

```sh
python -m unittest discover -s tests -v
python scripts/validate_site.py
python scripts/build_site.py
python -m http.server 8000 --directory _site
```

Abra http://localhost:8000. O artefato `_site/` e o cache Python são ignorados pelo Git.
O validador verifica metadados e referências locais; não é um validador completo
da sintaxe HTML e não depende da disponibilidade de links externos.
