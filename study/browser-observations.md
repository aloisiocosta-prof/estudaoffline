# Evidências observadas — 05/10/2026 UTC

Registro recebido do agente coordenador que executou a inspeção do navegador; não é uma segunda execução independente. Build de referência: commit `5a525bf49bc76e1c60dfa11e66142cb20fa65b54`. URL inspecionada: https://aloisiocosta-prof.github.io/estudaoffline/ . CI: https://github.com/aloisiocosta-prof/estudaoffline/actions/runs/37248230675 . Versão exata do navegador e estado detalhado do armazenamento não foram informados neste registro.

## CI
O coordenador informou conclusão bem-sucedida de flutter analyze, seis testes Flutter, quatro testes SemVer, build Web, geração de três PDFs, release e GitHub Pages no run indicado. Esses resultados de pipeline não demonstram isoladamente sucesso offline ou eficácia educacional. Vincular logs do run para detalhes de comandos e versões.

## Navegador
| Cenário | Procedimento informado | Resultado observado | Alcance |
|---|---|---|---|
| Criação e persistência | Criar “Revisar segurança dispositivos IoT”, assunto IoT, duração 30 min; concluir; recarregar | Título e conclusão preservados | Criação e restauração de uma tarefa nesta execução; exclusão e invariância de outros itens não comprovadas |
| Indicador de preparação | Inspecionar interface após carregamento | Indicador de cache preparado apareceu | Evidência da mensagem; rede não foi desabilitada e controle/ativos do service worker não foram demonstrados neste registro |
| Backup incompatível | Importar objeto com version 99 | Mensagem “Formato ou versão de backup incompatível.” e diálogo permaneceu aberto | Rejeição observada; não equivale aos casos de data inválida/ID duplicado nem prova preservação de todos os dados |
| Exportação | Acionar exportação duas vezes | Interface mostrou “Download solicitado”; nenhum evento ou arquivo de download foi observado | Exportação não verificada; ausência de evento no ambiente não confirma defeito do app |
| Backup válido | Importar study/fixtures/backup-valid.json | Duas tarefas apareceram: “Revisar requisitos do protótipo”, Engenharia de Software, 30 min, 2026-10-10, pendente; “Executar cenário de persistência”, Testes de Software, 45 min, 2026-10-11, concluída | Importação do fixture observada; exportação e comparação round-trip permanecem não verificadas |

## Ainda não executado ou não comprovado
Recarga com rede desabilitada, primeira visita offline, falha de quota, falha real de armazenamento, auditoria de acessibilidade, pen-test, matriz de múltiplos navegadores/dispositivos, exportação com arquivo recuperado e correspondência completa do round-trip. Não afirmar que todas as etapas passaram. Nenhum aluno participou; não houve medida de aprendizagem, aprovação institucional ou avaliação psicométrica.

Estados de requirements.csv são deliberadamente estreitos: “parcial” identifica evidência incompleta para o critério inteiro. Passar testes automatizados gerais não converte automaticamente requisitos de navegador em aprovados.

Filtro Concluídas: observado apenas Executar cenário de persistência, com conclusão marcada; tarefa pendente ausente nessa lista.
