# Decisão provisória — salvamento e importação

## Pergunta
Uma falha ao salvar ou uma importação inválida preserva o estudo anterior e informa o erro sem declarar sucesso?

## Decisão proposta
Separar estudo em uso, última cópia salva e alteração pendente. Preparar uma alteração ou uma importação válida não substitui o estudo em uso. Somente um resultado explícito de salvamento concluído promove a alteração pendente para o estudo em uso e para a cópia salva. A falha mantém esses três valores anteriores e informa que é necessário tentar novamente. Importação ilegível ou estruturalmente inválida também preserva a alteração pendente existente.

O protótipo aceita título não vazio de até 120 caracteres e duração inteira de 0 a 1.440 minutos. Esses limites são decisões exploratórias, não requisitos institucionais confirmados. Campos extras são rejeitados nesta exploração.

## Artefato exploratório
`/workspace/scratch/91c6ab881ce7/estudaoffline-prototype.html`: página autônoma, dados em memória, reducer puro e percursos normal, falha e arquivo inválido. Não integra armazenamento real e não deve entrar na aplicação de produção. Não foram adicionados testes ao protótipo.

## Evidência e estado da decisão
Estado: provisório; implementação da exploração preparada, execução observada ainda não registrada. O código descreve o comportamento pretendido; não constitui evidência de funcionamento no navegador ou de segurança da persistência real.

Após executar os percursos, registrar separadamente data, ambiente, ações, estado antes/depois, mensagem observada e capturas. Só então confirmar ou revisar a decisão. Na aplicação final, verificar falhas reais de escrita, leitura e importação e a conservação do estado anterior; uma simulação em memória não comprova essas propriedades.
