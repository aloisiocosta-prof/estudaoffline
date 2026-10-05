# EstudaOffline — especificação do MVP 0.1.0

## Resultado e contexto
Entregar aplicativo Flutter Web estático, publicado no GitHub Pages e acompanhado de PDFs técnicos, que permita organizar tarefas sintéticas de estudo, marcar conclusão e recuperar registros locais após preparação online. Contexto informado pelo professor Aloisio: CETI Lucas Meireles Alves, curso técnico ADS, Chapadinha Sul, Teresina–PI. Essa contextualização não constitui aprovação institucional; nomes de estudantes foram omitidos.

## Escopo
Lista de tarefas sintéticas, criação e exclusão de tarefas, filtros, marcação de conclusão, recuperação após recarga e exportação/importação de backup JSON. Sem cadastro, autenticação, sincronização, telemetria, dados pessoais ou notas de estudantes. O conteúdo e qualquer progresso de teste são sintéticos. O produto não demonstra eficácia pedagógica.

## Contrato offline
Primeiro acesso exige rede para obter aplicativo e recursos de execução. A disponibilidade offline só pode ser comprovada quando o service worker controla a página e os recursos necessários estiverem armazenados com sucesso. Depois, recarga sem rede deve abrir aplicativo e tarefas locais. Dados locais podem ser removidos pelo navegador ou usuário: avisar esse limite e tratar erro de armazenamento. Primeira visita sem cache não tem garantia de carregar; esse limite precisa ser explicitado. Não prometer funcionamento offline ilimitado [S1–S3].

## Decisões técnicas
Flutter Web para interface; service worker próprio para recursos do aplicativo, com escopo restrito à rota do projeto Pages; persistência local para progresso com erros tratados. IndexedDB é opção para dados estruturados; escolha final e eventual alternativa devem ser documentadas na implementação, sem fingir que uma API planejada já foi usada [S1–S3]. Não depender de CDN para recursos necessários à execução offline. Versão do cache acompanha release para evitar mistura de ativos.

## Pronto
Cada requisito em requirements.csv deve apontar evidência real. Executar análise estática, testes unitários e funcionais pertinentes; build release; navegador online e offline após preparação, incluindo recarga, persistência e caminho de falha. Publicação deve servir sob a subrota Pages correta. PDFs devem abrir e distinguir objetivos, método e resultados observados. Registrar versões de Flutter, navegador, commit, comandos e saídas. Etapa não executada permanece pendente; não preencher resultados por expectativa.

## Marcos
M1: organizador local de tarefas com dados sintéticos, filtros, persistência e backup validado. M2: build e contrato offline comprovados no navegador. M3: documentação/PDFs consistentes, release semântica e publicação Pages verificada. Segurança: revisão do escopo do service worker, dependências, dados publicados e recursos externos; não declarar pen-test completo sem execução e relatório próprio.

## Limites e questões abertas
Acesso real à rede, aparelhos da escola, usabilidade, acessibilidade em dispositivos assistivos e aprendizagem não foram medidos. Estudo com participantes requer protocolo e autorizações aplicáveis próprios. Fontes e justificativas estão em sources.md; estudo técnico em research-protocol.md.
