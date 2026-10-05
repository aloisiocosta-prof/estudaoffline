"""Follow a bibliographic key to paragraphs, claims and admission blockers."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--key',required=True);a=p.parse_args()
 graph=json.loads((ROOT/'study/literature/evidence-graph.json').read_text())
 report=json.loads((ROOT/'study/literature/admission-report.json').read_text())
 record=next((r for r in report['records'] if r['key']==a.key),None)
 if record is None:p.error('Chave ausente do corpus')
 parents={e['from'] for e in graph['edges'] if e['to']=='source:'+a.key}
 print(json.dumps({'source':record,'uses':[n for n in graph['nodes'] if n['id'] in parents]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
