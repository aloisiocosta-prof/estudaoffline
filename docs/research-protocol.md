# Protocolo de estudo técnico — EstudaOffline

## Pergunta
O MVP permite manipular tarefas e conservar progresso sintético no navegador quando a conexão é interrompida?

## Desenho e unidade
Estudo técnico descritivo de um artefato de software, sem participantes humanos. Unidade: execução de cenário em combinação registrada de build, navegador e estado do armazenamento. Não é experimento educacional, avaliação de alunos ou ensaio de aprendizagem.

## Hipóteses operacionais
H1: aplicativo e tarefas locais continuam disponíveis após recarga offline com cache preparado. H2: conclusão gravada reaparece após recarga. H3: backups semanticamente inválidos são rejeitados sem substituir tarefas e falha de armazenamento não gera falsa confirmação. Hipóteses pendentes até execução.

## Procedimento reproduzível
1. Registrar commit, release, versões de ferramentas, navegador, plataforma, URL/base path e condições de armazenamento.
2. Usar perfil limpo e backup sintético versionado. Online: abrir app, aguardar preparação do service worker, importar backup válido e marcar uma tarefa e registrar sucesso confirmado.
3. Desabilitar rede no navegador; recarregar app; manipular tarefas locais; conferir progresso. Capturar estado e requisições falhas relevantes.
4. Repetir primeira visita offline em perfil limpo, sem esperar carregamento. Testar importação com data inválida e identificador duplicado. Limpar dados locais e repetir: registrar perda esperada e mensagem. Simular erro/quota em teste controlado; distinguir simulação de esgotamento real.
5. Executar análise estática, testes unitários/funcionais e build; preservar saídas. Verificar a URL pública e abrir PDFs reais.
6. Para cada requisito: observado, falhou, pendente ou não aplicável com justificativa; anexar comando/saída/captura. Revisão independente confirma achados antes de fechar.

## Medidas e análise
Contagens de cenários executados e aprovados; disponibilidade da interface, estado do progresso e mensagens observadas. Se medir tempo, registrar ferramenta e condições, sem comparar dispositivos não equivalentes. A aprovação técnica exige critérios explícitos de requirements.csv; não usar pontuação de aprendizagem nem inferir eficácia.

## Limitações
Navegador automatizado não representa todos os dispositivos reais; armazenamento pode ser removido; primeira visita exige conectividade; versões e atualizações podem alterar comportamento [S1–S3]. Dados sintéticos não demonstram aceitação de usuários, adequação curricular ou aprendizagem. Estudos educacionais externos têm intervenções e populações distintas [S4].

## Relato e integridade
Este é protocolo prospectivo; ainda não contém resultados. Relatório final deve separar método planejado, desvios, resultados efetivamente observados e limitações. Não reivindicar PRISMA: a busca de fontes foi direcionada para decisões técnicas, sem revisão sistemática. Futuro estudo com alunos demanda desenho, instrumentos e autorizações próprios.
