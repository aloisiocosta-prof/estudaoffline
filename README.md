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

## Escrita e auditoria editorial

Artigo e entrega escolar usam parágrafos ABCD, com planejamento explícito em `study/literature/argumento-abcd.json` e prosa compartilhada em `paper/argumento.tex`. ABCD é convenção editorial do orientador, não instrumento validado. Cada parágrafo retoma um conceito anterior e prepara o seguinte; os rótulos A/B/C/D aparecem no planejamento, não na narração final.

Regra atual: máximo duas páginas físicas por seção; Considerações finais, máximo uma página. Referências não têm limite de páginas e contêm80 publicações científicas com DOI+URL, além de documentação técnica complementar. Todas as80 são citadas em bases de parágrafos ABCD com achados e limites, no artigo e na entrega escolar. A bibliografia não inclui o próprio estudo; métodos e resultados locais são descritos diretamente. A regra revoga a bibliografia compacta de seis fontes.

O caderno `paper/fichamentos.tex` preserva80 registros,18 com conferência dirigida anterior e62 preliminares; acesso, localizador, achado, limite e oportunidade proposta ficam separados. Não se declara leitura integral uniforme, rastreio completo de retratações ou validação da rubrica editorial.

Reproduzir: `python3 scripts/build_literature.py`, `python3 scripts/build_narrative.py`, `python3 scripts/build_fichamentos.py`; compilar em `paper` com `latexmk -xelatex -interaction=nonstopmode -halt-on-error artigo.tex entrega-escolar.tex poster.tex fichamentos.tex`. O CI inclui o caderno nos PDFs publicados e audita referências e limites por seção.

Auditorias: `scripts/audit_latex.py`, `scripts/audit_referencial.py`. A regra literal de todas as linhas ocuparem 50% continua não cumprida e é registrada sem preenchimento artificial. O pôster preserva os painéis ampliados anteriores; a revisão ABCD atual abrange artigo, entrega escolar e caderno, não uma revisão do aplicativo ou da eficácia educacional.
