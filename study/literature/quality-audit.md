# Auditoria de qualidade do corpus bibliográfico

Atualizada em 5 de outubro de 2026 (UTC), após enriquecimento editorial, inclusão de SU09, exclusão histórica de eng09, correção dos venues e regeneração do corpus. Auditoria local; não houve nova consulta externa, leitura integral ou avaliação sistemática de risco de viés. Política: docs/editorial/politica-latex.md.

## Corpus atual e seleção

| Grupo selecionado | Quantidade | journal ausente | DOI ausente |
|---|---:|---:|---:|
| education | 20 | 0 | 0 |
| accessibility | 20 | 0 | 10 |
| offline-security | 13 | 0 | 0 |
| engineering | 18 | 0 | 0 |
| supplemental | 9 | 0 | 0 |
| Total | 80 | 0 | 10 |

O corpus bruto tem 89 registros, selected.json tem 80 e excluded.json tem nove. Excluídos: OS04, OS05 (preprints); OS11 (tipo editorial inconsistente); OS12 (subtipo indefinido); OS16 (capítulo); OS19 e OS20 (publicação não confirmada); eng19 (revisão dos anais não inspecionada); eng09 (registro histórico com publicação pendente). As razões completas permanecem nas auditorias dos lotes. As exclusões são escolhas locais de elegibilidade, não evidência de inexistência ou baixa qualidade dessas fontes.

education.json registra journal e rastreio raw_fetch. Os nove venues antes pendentes foram preenchidos com metadados primários; nenhum selecionado permanece sem journal/venue. SU08 tem seis autores confirmados no programa oficial, evento datado de 16–19 agosto de 2021 e URL do programa; o DOI continua metadado do índice, sem alegar confirmação IEEE nesta sessão. O link do software do autor não foi recuperado nem demonstra licença ou código conferidos.

SU09, Miller (2007), substitui eng09. Sua inclusão fora da janela 2016–2026 tem justificativa explícita como fundamento editorial de comunicação de pôsteres, e não estudo de eficácia educacional. Há metadados institucionais/editoriais, mas acesso direto ao PMC foi bloqueado por CAPTCHA. O campo source_service “Primary PMC full text” conflita com access_level, que declara consulta de resumo/metadados; interpretar pelo limite de acesso e corrigir esse rótulo antes de alegar leitura integral. Não alterei o JSON nesta revisão.

Resumos completos foram retirados das cinco listas públicas e de selected/excluded; permanecem paráfrases, nível de acesso, metadados de consulta e links. build_literature.py exige autoria, claim_pt e limitation_pt, sem exigir reprodução de abstract. Essa remoção evita publicar resumos extensos, mas impede revalidar todas as afirmações apenas pelos JSON públicos: a confirmação exige os registros de consulta ou nova recuperação autorizada.

As listas originais não apresentaram duplicatas exatas por DOI normalizado ou título normalizado; essa triagem não exclui estudos com títulos diferentes, versões ou amostras sobrepostas. SU01 e SU02 são publicações distintas sobre a mesma diretriz PRISMA: podem constituir referências distintas, mas não estudos independentes de eficácia. Recontagem de selected/excluded confirma 80/9; o mínimo numérico atingido pelo gerador não equivale a 80 fontes metodologicamente validadas.

## Correções concretas de afirmações

Foram modificados cinco claim_pt em accessibility.json e regenerados os derivados. O problema não era uma promessa explícita de eficácia do MVP, mas recomendações apresentadas como se fossem resultados diretos dos resumos abreviados.

| Chave | Problema anterior | Correção aplicada |
|---|---|---|
| bong2021 | Apoio institucional atribuído como necessidade sem constar no suporte curto. | Separar revisão de formação docente de apoio institucional como proposta de projeto. |
| farhan2020 | “Precisam ser avaliadas” derivado de estudo que relata avaliação de recursos. | Relatar avaliação efetiva e identificar avaliação participativa do MVP como inferência. |
| kumiyeboah2023 | Estratégias complementares formuladas como recomendação geral a partir de entrevistas. | Atribuir relatos aos entrevistados e identificar combinação no projeto como proposta. |
| cob2023 | Necessidade de considerar tela/interface inferida de organização de critérios. | Relatar conteúdo da revisão e marcar aplicação ao MVP como inferência. |
| punchoojit2017 | Suporte editorial não demonstrava a recomendação sobre contexto de interação. | Descrever revisão de padrões e marcar aplicação escolar como inferência. |

Não foram modificados resultados quantitativos de estudos. Não se afirmou eficácia causal de organizador de tarefas, acessibilidade universal, vulnerabilidade atual do MVP ou garantias CRDT para localStorage. Outros enunciados devem continuar vinculados aos resumos originais e seus limites; essas correções não substituem avaliação de método e texto integral.

## Citações e geração compartilhada

Executado: python scripts/build_literature.py. Saída observada: selected=80, excluded=9, minimum_met=true. O último campo significa apenas comparação numérica.

Verificação estática de paper/bibliography.tex: 85 chaves bibliográficas, sendo 80 selecionadas e cinco técnicas/projeto fora da contagem científica. Todas as 80 chaves selecionadas aparecem em paper/literature.tex; nenhuma citação nesse arquivo está indefinida. artigo.tex, entrega-escolar.tex e poster.tex carregam natbib e os arquivos compartilhados literature.tex/bibliography.tex. Expandindo essas inclusões na análise estática, cada documento referencia as 80 chaves selecionadas e não apresenta chave citada sem bibitem.

Esta é verificação de fontes LaTeX, não de PDFs compilados: não confirma estabilização de referências, ausência de warnings natbib, layout, ocupação de linhas ou 80 publicações elegíveis confirmadas independentemente. Na revisão anterior, o gerador foi executado sem Flutter; nesta revisão final, seus derivados foram inspecionados sem executar nova geração. Nesta revisão final, somente quality-audit.md foi modificado; JSON e paper foram preservados.

## Datas e pendências

Nenhum ano das listas supera 2026; triagem local de datas ISO nos JSON não encontrou data posterior a 2026-10-05. Ano isolado não permite excluir publicação futura dentro de 2026. Selecionados de 2026 a conferir com data editorial completa: education_wong2026, linhalis2026 e eng20. OS20 e eng09 permanecem excluídos.

Preservar convenção consistente online/fascículo: education_taghavi2024 (2024/2026), education_xu2022 (2022/2023), education_zheng2016 (2016/2018), kumar2017 (2017/2018), eng03 (2018/2019), eng15 (2021/2022), eng16 (2021/2022), eng17 (2014/2016). martin2024 menciona volume posterior sem ano explícito. Ano do DOI não substitui data editorial.

Pendentes: resolver o rótulo de acesso contraditório de SU09; confirmar datas completas; conferir metadados primários e abstracts rastreados; avaliar risco de viés por desenho se for reivindicada síntese científica; compilar documentos e examinar warnings e ocupação das linhas. Não houve busca nova, scite, leitura integral nem investigação de retratações nesta auditoria. Conclusão permitida: corpus selecionado e citações estáticas alcançam 80; conclusão não permitida: “80 fontes científicas validadas” ou conformidade editorial universal.


## Parecer final desta revisão

A conferência estática atual confirma 89 entradas nas listas de origem, 80 selecionadas e nove excluídas. As 80 fontes selecionadas têm venue registrado; não há abstract_or_support nas listas públicas. No material científico sobre o aplicativo não foi identificada alegação explícita de ganho de aprendizagem, segurança ou acessibilidade demonstrados pelo MVP. As cinco correções concretas de propostas/inferências permanecem nas paráfrases geradas. O código de lib não contém exposição científica que atribua esses efeitos; docs/SPEC.md, research-protocol.md e sources.md mantêm os limites. A ausência de abstracts públicos limita a confirmação semântica independente de todos os resultados externos.

As bibliografias geradas têm labels autor–ano distintos: Page et al. (2021a/2021b) para as duas publicações e MDN (2026a/2026b/2026c) para documentação técnica. Nenhum label opcional é duplicado. Os três documentos continuam citando 80 chaves científicas pelo arquivo compartilhado e nenhuma chave citada fica sem bibitem na expansão estática. Isso resolve a ambiguidade autor–ano observável nas fontes, sem substituir compilação e leitura do PDF.

Ressalva documental localizada: supplemental-audit.md ainda abre com “Oito publicações”, embora supplemental.json agora tenha nove. Atualizar esse inventário e registrar a exceção Miller2007 nesse log; não foi editado por estar fora do escopo autorizado desta revisão.


Conferência adicional pré-entrega: SU06 corrigido de Dental science reports para Scientific Reports13art14045, conforme Nature DOI10.1038/s41598-023-41032-5 (7set2023); OS13 título completo conforme ACMdoi10.1145/3596267; eng02 venueComputers conforme MDPI12(5)97. A presença de metadados no indexador não garante exatidão editorial. Não se afirma validação integral dos 80estudos.
