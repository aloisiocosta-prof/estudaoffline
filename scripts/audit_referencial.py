"""Verify current section caps from compiled PDF bookmarks and final bibliography."""
import argparse,json,re
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pdf-dir',type=Path,required=True);args=parser.parse_args();report={}
    titles=[s['title'] for s in json.loads((ROOT/'study/literature/argumento-abcd.json').read_text())['sections']]
    for name in ['artigo','entrega-escolar']:
        doc=fitz.open(args.pdf_dir/(name+'.pdf'));assert len(doc)>0
        toc=doc.get_toc();starts=[(t,next(p for level,label,p in toc if level==1 and label==t)) for t in titles]
        # Bibliography can be an unnumbered heading without a PDF bookmark.
        ref=next(i+1 for i,p in enumerate(doc) if p.get_text().lstrip().startswith('Referências'))
        bookmarks=[p for level,title,p in toc if title=='Referências']
        assert bookmarks and all(p==ref for p in bookmarks),(name,'bibliography bookmark',bookmarks,ref)
        starts.append(('Referências',ref));result={}
        for i,(title,start) in enumerate(starts):
            stop=starts[i+1][1]-1 if i+1<len(starts) else len(doc)
            cap=1 if title in ['Considerações finais','Referências'] else 2
            assert stop>=start and stop-start+1<=cap,(name,title,start,stop,cap)
            text=' '.join(doc[p-1].get_text() for p in range(start,stop+1))
            assert '(??)' not in text and '(?)' not in text,(name,title,'unresolved citation')
            result[title]={'start_page':start,'end_page':stop,'pages':stop-start+1,'maximum_pages':cap,'passed':True}
        report[name]=result
    (ROOT/'study/referencial-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
