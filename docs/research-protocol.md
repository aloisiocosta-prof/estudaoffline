# Protocolo de estudo técnico — EstudaOffline

## Pergunta
O MVP permite consultar recursos previamente preparados e conservar progresso sintético no navegador quando a conexão é interrompida?

## Desenho e unidade
Estudo técnico descritivo de um artefato de software, sem participantes humanos. Unidade: execução de cenário em combinação registrada de build, navegador e estado do armazenamento. Não é experimento educacional, avaliação de alunos ou ensaio de aprendizagem.

## Hipóteses operacionais
H1: recursos preparados continuam disponíveis após recarga offline. H2: conclusão gravada reaparece após recarga. H3: ausência de cache ou falha de armazenamento produz aviso e não falsa confirmação. Hipóteses pendentes até execução.

## Procedimento reproduzível
1. Registrar commit, release, versões de ferramentas, navegador, plataforma, URL/base path e condições de armazenamento.
2. Usar perfil limpo e catálogo sintético versionado. Online: abrir app, preparar conteúdo, marcar um item e registrar sucesso confirmado.
3. Desabilitar rede no navegador; recarregar app; abrir material preparado; conferir progresso. Capturar estado e requisições falhas relevantes.
4. Repetir com recurso não preparado. Limpar dados locais e repetir: registrar perda esperada e mensagem. Simular erro/quota em teste controlado; distinguir simulação de esgotamento real.
5. Executar análise estática, testes unitários/funcionais e build; preservar saídas. Verificar a URL pública e abrir PDFs reais.
6. Para cada requisito: observado, falhou, pendente ou não aplicável com justificativa; anexar comando/saída/captura. Revisão independente confirma achados antes de fechar.

## Medidas e análise
Contagens de cenários executados e aprovados; disponibilidade do conteúdo, estado do progresso e mensagens observadas. Se medir tempo, registrar ferramenta e condições, sem comparar dispositivos não equivalentes. A aprovação técnica exige critérios explícitos de requirements.csv; não usar pontuação de aprendizagem nem inferir eficácia.

## Limitações
Navegador automatizado não representa todos os dispositivos reais; armazenamento pode ser removido; primeira visita exige conectividade; versões e atualizações podem alterar comportamento [S1–S3]. Dados sintéticos não demonstram aceitação de usuários, adequação curricular ou aprendizagem. Estudos educacionais externos têm intervenções e populações distintas [S4].

## Relato e integridade
Este é protocolo prospectivo; ainda não contém resultados. Relatório final deve separar método planejado, desvios, resultados efetivamente observados e limitações. Não reivindicar PRISMA: a busca de fontes foi direcionada para decisões técnicas, sem revisão sistemática. Futuro estudo com alunos demanda desenho, instrumentos e autorizações próprios.
