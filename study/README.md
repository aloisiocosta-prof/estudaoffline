# Estudo técnico reproduzível — dados sintéticos

Artefatos desta pasta são exemplos de teste, sem identificação de estudantes. O produto implementado é um organizador local de tarefas de estudo: não confundir tarefas com armazenamento de livros ou PDFs didáticos. Consulte também ../docs/research-protocol.md e o relatório técnico final; o roteiro abaixo não é prova de execução.

## Fixtures e contrato
fixtures/backup-valid.json tem versão 1 e duas tarefas distintas, uma pendente e uma concluída. fixtures/backup-invalid-date.json contém data inexistente; fixtures/backup-invalid-duplicate.json repete identificador. Conforme lib/model.dart, backup exige objeto com version inteiro 1 e tasks lista; cada tarefa contém id/title/subject não vazios até 200 caracteres, deadline válido YYYY-MM-DD entre 1900 e 2200, minutes inteiro de 1 a 1440 e done booleano. Máximo 5.000 tarefas e 2.000.000 caracteres de texto. Limite em caracteres não equivale a tamanho exato do arquivo em bytes. Campos adicionais não têm rejeição garantida. Fixtures inválidas são JSON sintaticamente válidos e semanticamente inválidos.

## Roteiro manual
Registrar URL, commit/release, data/hora, navegador/versão, sistema, estado da rede e armazenamento. Usar perfil dedicado de teste; exportar qualquer dado prévio antes de substituir tarefas.

| ID | Procedimento | Resultado esperado | Evidência a preservar |
|---|---|---|---|
| M01 | Em Segurança e backup, Importar backup, colar backup-valid.json e confirmar | Duas tarefas; títulos, duração e conclusão correspondem ao fixture | Captura antes/depois e versão |
| M02 | Alternar conclusão da primeira tarefa e recarregar | Alteração confirmada permanece e segunda tarefa não muda | Capturas e eventual erro |
| M03 | Exportar backup e comparar conteúdo após parse JSON | Mesmos identificadores e campos atuais; formatação pode diferir | Arquivo exportado sintético |
| M04 | Importar backup-invalid-date.json | Mensagem de erro; lista anterior preservada | Captura de erro e lista |
| M05 | Importar backup-invalid-duplicate.json | Mensagem de erro; lista anterior preservada | Captura de erro e lista |
| M06 | Carregar build release online até app abrir; esperar service worker controlar a página; desabilitar rede e recarregar a mesma URL | Interface e tarefas locais permanecem utilizáveis se preparação do cache terminou | Estado do controlador, captura offline e requests |
| M07 | Em perfil limpo, primeira visita sem rede | Sem garantia de carregar; comportamento registrado sem declarar cache preparado | Captura e estado limpo |
| M08 | Exportar fixture, limpar armazenamento da origem e reabrir | Dados locais não garantidos; importar backup recupera tarefas | Evidências de perda e recuperação |

Service worker e cache são condições explícitas do M06; build compilado ou ícone de conexão não bastam. Cache depende de versão/navegador e pode ser removido. Teste de quota/erro controlado deve ser documentado separadamente; não fingir esgotamento real a partir de mock. Só execute limpeza em perfil de teste: no Pages, outras aplicações podem compartilhar a origem.

## Afirmações permitidas e proibidas
Pode afirmar: critérios técnicos observados passaram naquela combinação registrada; dados sintéticos foram importados/exportados; recarga offline funcionou após preparação no navegador testado — somente quando há evidência real correspondente.

Não pode afirmar: melhoria de aprendizagem, aprovação escolar, validação psicométrica, eficácia educacional, representatividade de usuários, ausência absoluta de vulnerabilidades, armazenamento permanente, suporte offline de primeira visita, funcionamento em todos os aparelhos ou teste completo de segurança. Não houve participantes humanos nem coleta de desempenho escolar. Estudos externos não demonstram eficácia deste app.

## Registro de execução
Para cada ID preencher: estado (passou/falhou/pendente), resultado observado, referência de evidência, versão e desvio do procedimento. Etapas inaplicáveis precisam justificativa. Este arquivo define expectativas; nenhum resultado fica aprovado apenas por existir um fixture.
