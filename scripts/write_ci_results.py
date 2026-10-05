from pathlib import Path
import os
commit=os.environ.get('GITHUB_SHA','unknown');run=os.environ.get('GITHUB_RUN_ID','unknown')
parts=['A execução automatizada documentada verificou componentes técnicos do MVP',
       'O GitHub Actions concluiu análise estática, testes Flutter, quatro testes de versionamento e compilação web; commit '+commit[:7]+', execução '+run,
       'Esses resultados se restringem à execução registrada, e o teste de widget com armazenamento simulado não comprova recarga real do navegador sem conexão',
       'Por isso, os resultados automatizados precisam ser lidos junto às observações disponíveis no navegador']
Path('paper/results.tex').write_text(' '.join(s+r' \citep{projeto}.' for s in parts)+'\n')

import json
ledger=Path('study/literature/argumento-abcd.json')
x=json.loads(ledger.read_text())
for section in x['sections']:
    for p in section['paragraphs']:
        if p['id']=='R1':
            for key,value in zip(['A','B','C','D'],parts):p[key]=value
ledger.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
