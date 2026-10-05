"""Build ABCD prose and an external bibliography; never cite own study as evidence."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    x=json.loads((ROOT/'study/literature/argumento-abcd.json').read_text());parts=[]
    for section in x['sections']:
        parts.append(r'\clearpage\section{'+section['title']+'}')
        for p in section['paragraphs']:
            if p['id']=='T4':parts.append(r'\newpage')
            if p['id']=='R1':parts.append(r'\input{results.tex}');continue
            cite=r' \citep{'+','.join(p['keys'])+'}' if p['keys'] else ''
            if p.get('base_parts'):
                # Each attributed claim retains its own source, rather than a decorative cluster.
                b='; '.join(item['text'].rstrip('.!?')+r' \citep{'+item['key']+'}' for item in p['base_parts'])+'.'
                parts.append(p['A']+cite+'. '+b+' '+p['C']+cite+'. '+p['D']+cite+'.')
            else:
                # Own context/procedures/results are described; they are not external literature.
                own=p['id'] in ['I2','M1','R1','R2','F1']
                parts.append(' '.join(p[k]+('' if own or (p['id']=='M2' and k in ['A','C','D']) or (p['id'] in ['T3','T4','T6','D1'] and k=='C') or (p['id']=='I1' and k=='A') else cite)+'.' for k in ['A','B','C','D']))
    (ROOT/'paper/argumento.tex').write_text('\n\n'.join(parts)+'\n')
    full=(ROOT/'paper/bibliography.tex').read_text()
    assert '{projeto}' not in full
    cited={k for sec in x['sections'] for p in sec['paragraphs'] for k in p['keys']}
    entries=re.findall(r'\\bibitem.*?(?=\\bibitem|\\end\{thebibliography\})',full,re.S)
    kept=[e for e in entries if re.search(r'\]\{([^}]+)\}',e)[1] in cited]
    (ROOT/'paper/references-core.tex').write_text(r'\begin{thebibliography}{99}'+'\n'+ '\n'.join(kept)+r'\end{thebibliography}'+'\n')
    print({'scientific_sources':80,'paragraphs':sum(len(s['paragraphs']) for s in x['sections'])})
if __name__=='__main__':main()
