> Registro histórico da revisão anterior. A versão ABCD usa seis fontes científicas no manuscrito conciso, conserva as 80 no caderno e substitui o mínimo de três páginas pelo máximo de duas; ver docs/editorial/revisao-abcd.md.

# Correções de fundamentação e evidências — 5 outubro 2026

A revisão trata a fundamentação como seleção narrativa focal, orientada à pergunta técnica e sujeita a limites de cobertura; a escolha de uma modalidade de revisão não dispensa transparência de seleção e análise (Snyder,2019, DOI10.1016/j.jbusres.2019.07.039).

## Erros corrigidos e consequências

| Problema | Correção | Evidência e consequência |
|---|---|---|
| Grande quantidade de fontes sugerindo validade | Separar corpus ampliado em apêndice e referencial integrado | 80 publicações no corpus; 18 fontes no núcleo argumentativo, não 80 estudos independentes ou instrumentos validados |
| Modelo teórico genérico | Escolher a descrição do ciclo de Zimmerman por Panadero 2017 | Antecipação, execução e autorreflexão; implementação cobre apenas recursos organizacionais, não todos os processos |
| Seleção predominantemente favorável | Incluir contrapontos de Palalas/Wark e limites de relato | Dispositivos podem apresentar resultados neutros/desfavoráveis; nenhuma nova estimativa de efeito |
| Contar revisões sobrepostas como reforço independente | Registrar relação explícita Prasse→Araka | Araka é ID2 nas referências incluídas por Prasse; não somar suas amostras |
| Ambiguidade de “offline” | Distinguir posição temporal da mensuração e rede indisponível | Araka usa antes/depois da aprendizagem; o contrato do MVP trata ausência de rede |
| Referência antiga admitida como exceção silenciosa | Excluir Miller 2007; excluir FEDS online 2014/fascículo 2016 | Incluir Panadero 2017 e Snyder 2019, com motivo documentado; nenhum enunciado depende de consulta de original não realizada |
| Critérios de acessibilidade sem vínculo normativo específico | Identificar seis critérios WCAG2.2 | Matriz de procedimentos em accessibility-inspection.csv; todos pendentes, sem certificação |
| Duração e conclusão confundidas com estudo real | Declarar minutos como planejamento e done como estado informado | lib/model.dart não registra cronômetro nem compreensão; nenhuma medida de aprendizagem |
| Armazenamento de teste confundido com navegador | Identificar store_stub em memória no teste de widget | Reconstrução do widget não é recarga offline real ou prova de localStorage |
| Teste de modelo interpretado como transação completa | Limitar conclusões ao parsing e validação | O teste que mantém lista independente não executa a importação pela interface; atomicidade real e download precisam de cenários próprios |
| “Sem dados pessoais” como promessa geral | Restringir a afirmação ao dataset sintético do estudo | Texto livre pode receber dados pessoais; mesma origem/perfil não isola usuários |
| Borda da linha incluindo espaços considerada ocupação por caracteres | Usar união de caixas de caracteres não brancos e preservar ambas as medidas | Avanço tipográfico não é cobertura de tinta; regra universal continua não atendida se alguma linha ficar abaixo de50% |
| Documento vazio aprovado por falta de violações | Rejeitar zero páginas e ausência de texto extraível | Três regressões verificam PDF vazio, página branca e espaços artificiais |
| Inventários e níveis de acesso desatualizados | Recontar corpus e registrar acesso por fonte | 91 registros,80 selecionados,11 excluídos; ficha central com18 fontes e localizações; sem avaliação uniforme de viés |

A leitura de trechos adicionais pode corrigir a interpretação, mas não equivale à leitura crítica integral de todas as fontes, e a conferência foi realizada por agente de IA sem segunda avaliação humana independente (registro: study/literature/core-source-appraisal.json).

## Regras de interpretação

Os cenários sintéticos testam operações e requisitos em uma configuração registrada; o uso de referências sobre aprendizagem não transforma esses resultados em evidência de efeito educacional (Araka et al.,2020, DOI10.1186/s41039-020-00129-5; protocolo do projeto).
A inspeção dos critérios selecionados é parcial e não autoriza declaração de conformidade integral, pois a WCAG2.2 estabelece requisitos para páginas e processos completos (W3 C,2024, https://www.w3.org/TR/2024/REC-WCAG22-20241212/).
As fontes de aprendizagem móvel e engenharia móvel são aplicadas como motivação ou diferenciação conceitual, sem transferir medidas, intervenções ou ferramentas de Android para Flutter web sem novos testes (Palalas;Wark,2020, DOI10.14742/ajet.5650; Júnior et al.,2022, DOI10.1145/3507903).

## Limitações que não podem ser eliminadas pela redação

| Limite | Tratamento verificável | Estado |
|---|---|---|
| Sem participantes e sem medida de aprendizagem | Retirar qualquer inferência de eficácia; futuro estudo exige desenho e autorizações próprios | Delimitado; não há validação educacional |
| Texto integral indisponível para parte das fontes | Limitar enunciados ao suporte recuperado; marcar método não avaliável | Parcial; sem julgamento formal uniforme |
| Retrações e contexto de citações | Scite read_fulltext retornou exigência de plano; não alegar verificação | Não concluído |
| Segunda avaliação independente | Permitir revisão humana da ficha de18 fontes e resolver discordâncias | Não realizada |
| Recarga offline, quota, exportação, usuários assistivos e pen-test | Manter cenários não executados como pendentes | Não comprovados nesta revisão |
| Regra de50% em toda linha | Reportar caracteres, espaços, títulos, referências e paginação separadamente | A conferir em cada PDF; sem exceção presumida |
| Formatação escolar e aceitação | Manter substituição Liberation Sans declarada e revisão institucional pendente | Sem promessa de aprovação |

Registro metodológico e consultas: study/literature/referencial-busca.json; ligação fonte–afirmação–limite: study/literature/core-source-appraisal.md; resultados editoriais: study/editorial-audit.json e study/referencial-audit.json.
