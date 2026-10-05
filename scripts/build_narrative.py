"""Build connected paragraphs from the reviewed ABCD ledger."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    x=json.loads((ROOT/'study/literature/argumento-abcd.json').read_text())
    parts=[]
    for section in x['sections']:
        parts.append(r'\clearpage\section{'+section['title']+'}')
        for p in section['paragraphs']:
            if p['id']=='T4':parts.append(r'\newpage')
            if p['id']=='R1':
                parts.append(r'\input{results.tex}')
                continue
            parts.append(' '.join(p[k]+r' \citep{'+','.join(p['keys'])+'}.' for k in ['A','B','C','D']))
    (ROOT/'paper/argumento.tex').write_text('\n\n'.join(parts)+'\n')
    # Only references actually cited in the shared manuscript; full corpus stays separate.
    full=(ROOT/'paper/bibliography.tex').read_text()
    cited={key for sec in x['sections'] for p in sec['paragraphs'] for key in p['keys']}
    entries=re.findall(r'\\bibitem.*?(?=\\bibitem|\\end\{thebibliography\})',full,re.S)
    kept=[]
    for entry in entries:
        key=re.search(r'\]\{([^}]+)\}',entry)[1]
        if key not in cited:continue
        entry=entry.split(' Consulta:')[0].split(' Acesso em')[0].strip()
        if key=='projeto':
            entry=r'\bibitem[EstudaOffline(2026)]{projeto} ESTUDAOFFLINE. Protocolo e registros técnicos. 2026. \url{https://github.com/aloisiocosta-prof/estudaoffline}. Registro do próprio estudo.'
        if key=='wcag':
            entry=r'\bibitem[W3C(2024)]{wcag} W3C. Web Content Accessibility Guidelines 2.2. Recomendação, 12 dez. 2024. \url{https://www.w3.org/TR/WCAG22/}.'
        kept.append(entry)
    (ROOT/'paper/references-core.tex').write_text(r'\begin{thebibliography}{99}'+'\n'+ '\n\n'.join(kept)+'\n'+r'\end{thebibliography}'+'\n')
    print({'manuscript_sources':len(kept),'scientific_sources':6,'paragraphs':sum(len(s['paragraphs']) for s in x['sections'])})
if __name__=='__main__':main()
