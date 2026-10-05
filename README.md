# EstudaOffline

MVP Flutter Web para planejar estudos, acompanhar conclusão e exportar/importar backup JSON no próprio navegador. Sem login, servidor de dados ou integração com IA.

## Demonstração e estudo

Deploy: https://aloisiocosta-prof.github.io/estudaoffline/

Após carregar online, aguarde **Acesso offline preparado** antes de testar sem conexão. Dados ficam neste navegador; limpeza do armazenamento pode apagá-los. Faça backups. Não use dados pessoais nos testes.

As evidências deste estudo são testes técnicos com casos sintéticos; não demonstram aprendizagem, aceitação por estudantes nem eficácia pedagógica. Artigo e pôster são versões para revisão do orientador, com autoria a preencher. Veja `docs/research-protocol.md`, `docs/requirements.csv` e `paper/results.tex`.

## Reproduzir

Flutter estável 3.47.6: `flutter pub get`, `flutter analyze`, `flutter test`, `flutter build web --release --base-href /estudaoffline/ --no-web-resources-cdn`, `python3 scripts/prepare_web.py`.

PDFs: instalar XeLaTeX, latexmk e Liberation Sans; executar em `paper`: `latexmk -xelatex -interaction=nonstopmode -halt-on-error artigo.tex entrega-escolar.tex poster.tex`.

GitHub Actions valida, compila PDFs, publica Web no Pages e gera Releases SemVer a partir de Conventional Commits (`feat`, `fix`, `!` ou `BREAKING CHANGE`). Downloads incluem artigo, entrega escolar, pôster e pacote web, com SHA256. Ative Pages com origem **GitHub Actions**.

## Limites

Sem avaliação com participantes. Sem garantia contra perda por quota/limpeza do navegador. Sem sincronização entre dispositivos. Conformidade escolar precisa de conferência do modelo e aprovação do orientador; Liberation Sans é substituta métrica de Arial, não a fonte Arial exata.
