# Controle documental dos fichamentos

A cadeia de rastreamento é publicação → localizador consultado → afirmação → parágrafo ABCD → citação → referência. O controle distingue completude do registro, sustentação da paráfrase e decisão editorial; DOI e URL não validam qualidade metodológica nem aprovam a pesquisa (Gao et al., 2023, DOI 10.18653/v1/2023.emnlp-main.398; Snyder, 2019, DOI 10.1016/j.jbusres.2019.07.039).

`python scripts/track_sources.py` gera JSON, CSV e relatório de admissibilidade, além de `evidence-graph.json`. `python scripts/query_evidence.py --key SU10` recupera a ficha, páginas, DOI, URL e destinos. Os hashes SHA256 dos arquivos de entrada permitem detectar alterações. Este é um controle documental próprio, sem alegação de instrumento científico validado (Gao et al., 2023).

## Critérios e decisão

Identificação, DOI registrado, URL registrada, página conferida, conferência dirigida e limites são critérios observáveis desta triagem. DOI registrado é checagem sintática, não consulta automática ao registro editorial. Cinco fontes satisfazem esses critérios para revisão; 75 têm pendências. Nenhuma decisão final do orientador foi registrada. Mesmo uma ficha apta só pode sustentar a afirmação e o alcance efetivamente conferidos; não autoriza extrapolação para aprendizagem, causalidade ou validade de instrumentos (Gao et al., 2023; Snyder, 2019).

Para decisão final, o orientador deve confrontar cada paráfrase com o original, conferir autores, ano, veículo, volume, fascículo, páginas ou identificador de artigo, DOI, URL e eventuais avisos editoriais; extrair desenho, população, resultados e limitações pertinentes. Registrar em `admission-decisions.json` revisor, data, decisão, justificativa, afirmações conferidas e `input_fingerprint` atual; decisões com fonte ou parágrafo alterado são rejeitadas. Executar `python scripts/track_sources.py --strict` antes de rotular a entrega como final: o controle bloqueia o estado atual porque não há 80 decisões documentadas. Registrar a revisão por afirmação antes de chamar o corpus de aceito. O relatório atual não trata a contagem de 80 fontes como 80 publicações já aprovadas nem declara rastreamento integral de retratações (Snyder, 2019).

## Modelo escolar e normas

Os arquivos DOCX 01 e 02 são idênticos pelo SHA256 registrado em `docs/school-model-requirements.json`. A entrega escolar tem Introdução com Objetivos e Metodologia, Referencial teórico, Considerações finais, Referências, Apêndices e Anexos. Os objetivos são um geral e dois específicos, em infinitivo. Dados e síntese ampliada são preservados em apêndices próprios. Nenhum documento de terceiros foi inventado para preencher Anexos (modelo fornecido, páginas 3–5).

O arquivo exige A4, margens de 2 cm, Arial ou Times New Roman 12 pt, entrelinhas 1,5 e texto justificado. A entrega aplica as margens literais; a divergência com a orientação genérica 3/2 cm usada anteriormente fica registrada. Liberation Sans continua substituindo Arial, portanto a fonte exata não está cumprida. Aprovação da escola, autoria estudantil e conferência normativa integral seguem pendentes (modelo fornecido, parágrafo 97 e configuração de seção).

ABCD organiza o parágrafo por decisão do orientador; ABNT organiza a apresentação da citação e referência. A citação indireta usa autor-data; página é acrescentada apenas quando conferida. Referências estão ordenadas alfabeticamente e com espaçamento simples na entrega escolar; completude de metadados e conformidade integral ainda requerem revisão, usando NBR 10520:2023 e NBR 6023:2025 (ABNT, 2023; UNICAMP, 2025, https://www3.eco.unicamp.br/biblioteca/images/arquivos/NBR60232025Referencias.pdf).

## codebase memory mcp

A versão 0.11.0 foi obtida da release oficial e o arquivo Linux amd64 conferido com SHA256 `032b33c1833919a2d1de67ff6367fa6ea46aee8689c86ef223c88fae3b6e4536`. A tentativa local de indexação falhou com `secure CLI coordination could not be created (process-fingerprint)`; não houve grafo local retornado. O CI tem execução isolada com versão e hash fixados e artefato de resultado, inclusive em falha. Não se modifica configuração global de agentes e não se desativa a coordenação de segurança (DeusData, documentação técnica, https://github.com/DeusData/codebase-memory-mcp).

O grafo da ferramenta rastreia código, geradores e testes. O grafo bibliográfico é produzido separadamente por `track_sources.py`; arestas de citação não são provas automáticas de sustentação. O job técnico é opcional e sua falha não se converte em sucesso científico ou em bloqueio artificial da compilação documental (DeusData, documentação técnica; Gao et al., 2023).

A primeira execução do CI retornou índice com 2207 nós e 2315 arestas, mas o modo moderate excluiu scripts e a consulta assess retornou zero linhas. Esse resultado não foi aceito como cobertura útil do rastreamento. A integração foi corrigida para modo full e exige retorno não vazio da função assess; dados bibliográficos são excluídos do índice AST por .cbmignore e continuam no grafo documental próprio (registro técnico initial-ci-coverage.json; DeusData, documentação técnica).

O CI registra os resultados antes de gerar narrativa e rastreamento; `track_sources.py --verify-fresh` compara os hashes depois dos geradores para rejeitar relatórios feitos antes de uma alteração das entradas. O teste reproduz uma entrada alterada e exige bloqueio do grafo desatualizado (controle técnico local; Gao et al., 2023, sobre verificabilidade de citações).
