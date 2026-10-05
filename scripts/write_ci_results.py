from pathlib import Path
import os
# Invoked only after analyze, test and release web compilation succeed.
commit=os.environ.get('GITHUB_SHA','unknown')
run=os.environ.get('GITHUB_RUN_ID','unknown')
Path('paper/results.tex').write_text('A execução técnica no GitHub Actions concluiu análise estática, suíte de testes Flutter, quatro testes de versionamento e compilação web sem falha. Commit: '+commit[:7]+'. Execução: '+run+'. Os relatórios estão nos artefatos da execução em study/raw. Esses resultados não demonstram eficácia pedagógica. A reabertura sem rede, a instalação PWA e a falha de quota permanecem pendentes de teste específico no navegador. \\citep{projeto}.\n')

with Path('paper/results.tex').open('a') as output:
    output.write(Path('paper/browser-results.tex').read_text())
