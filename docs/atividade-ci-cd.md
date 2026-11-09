# Laboratório - Pipeline CI/CD com IA generativa

## Projeto e diagnóstico inicial

- Repositório: https://github.com/GabPGarcia/atividade-pull-request
- Versão inicial inspecionada: `fdfa53a`.
- Tecnologias: cinco páginas HTML e dois arquivos CSS na raiz.
- A API do GitHub retornou zero workflows e `has_pages: false`.
- Estratégia: GitHub Pages com artefato estático validado antes da publicação.

O projeto não usa backend nem dependências de aplicação. Os formulários já
existentes são demonstrativos. A atividade acrescenta automação de validação e
publicação, mantendo o conteúdo original das páginas.

## Prompts fictícios: simulação com quatro etapas

Estes quatro prompts são uma simulação solicitada para representar a evolução
gradual da solução. Não são transcrições de interações anteriores. Os resultados
e problemas técnicos descritos correspondem ao trabalho realizado nesta atividade.

### 1. Verificar o ponto de partida

**Prompt:** "Confere esse repositório e veja se já tem alguma pipeline. A gente fez
umas páginas em HTML e CSS para praticar pull request. Qual seria um jeito simples
de validar e publicar esse projeto pelo GitHub Actions?"

**Resultado:** identificação de ausência de workflows e de publicação no Pages.
**Problema:** ainda não havia CI/CD para validar e disponibilizar o projeto.
**Alteração:** criação do workflow, com CI em push e PR para `main`, e escolha de Pages.

### 2. Criar e testar a validação

**Prompt:** "Antes de publicar, coloca uma verificação dos arquivos e links das
páginas. Prefiro algo simples, sem instalar várias dependências. Também testa se
essa verificação consegue encontrar um link quebrado."

**Resultado:** validador Python e sete testes para links, arquivos, CSS e âncoras.
**Problema real:** o primeiro teste de capitalização falhou no Windows porque
`Path.resolve()` normalizou o nome do arquivo e ocultou a diferença de maiúsculas.
**Alteração:** comparação com `posixpath.normpath()` preservando a capitalização
do caminho escrito no HTML. O teste passou após a correção.

### 3. Controlar a publicação

**Prompt:** "Agora separa a CI do deploy. No pull request só deve validar. Quando a
mudança entrar na main, publique apenas se a CI passar e envie só os arquivos do
site, sem scripts nem documentos."

**Resultado:** jobs `ci` e `deploy`, condição de push na `main` e `needs: ci`.
**Problema:** o repositório ainda não tinha Pages habilitado.
**Alteração:** configuração inicial do Pages para GitHub Actions; geração de `_site`
com os sete arquivos públicos, `.nojekyll` e identificação do commit.

### 4. Demonstrar o resultado

**Prompt:** "Depois do deploy, confere se o site está acessível e se é a mesma versão
que passou na pipeline. Quero guardar as evidências do pull request, do push e da
publicação para colocar tudo no relatório."

**Resultado:** verificação HTTP do SHA, do conteúdo inicial e dos arquivos publicados.
**Problema previsto:** a distribuição pode levar alguns segundos para atualizar.
**Alteração:** até 12 tentativas, com intervalos de 10 segundos, antes de falhar.
As evidências devem ser extraídas das execuções reais, sem simular resultados.

## Registro de alterações

- `.github/workflows/ci-cd.yml`: checkout, ambiente Python, testes, validação,
  preparação do artefato e CD condicionado ao sucesso da CI.
- `scripts/validate_site.py`: metadados e referências locais com capitalização exata.
- `scripts/build_site.py`: pacote público e `build-info.json` com SHA do commit.
- `scripts/check_deployment.py`: confirmação HTTP da publicação.
- `tests/test_validate_site.py`: sete cenários válidos e inválidos.
- `.gitignore`: artefato e cache Python.
- `README.md` e este registro: justificativa, comandos e processo de uso de IA.

Não houve edição manual do usuário nesta implementação. A geração e a correção do
código foram realizadas com apoio de IA; a configuração administrativa do Pages
foi aplicada via API. Não foram alteradas as páginas originais nem os demais branches.

## Análise e verificação

Foram organizados **quatro prompts fictícios** para o relato; esse número não é uma
contagem de mensagens reais. O uso real de IA ocorreu na implementação, revisão,
correção e execução desta atividade pelo assistente Codex.

A principal correção técnica foi a detecção de diferenças de capitalização no
Windows. A ausência de dependências foi tratada com a biblioteca padrão do Python.
O Pages foi escolhido por corresponder à aplicação estática e integrar hospedagem,
artefatos e autenticação com o GitHub Actions.

A verificação inclui testes locais, CI de pull request com CD ignorado, CI/CD após
push na `main` e confirmação HTTP do commit e dos sete arquivos publicados. O PDF
final apresenta os resultados reais, os links das execuções e o código completo.
