"""Evidence graph and conservative, claim-scoped admission checks; no certification."""
import argparse, csv, hashlib, json, re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name): return json.loads((ROOT/'study/literature'/name).read_text())
def assess(source, locator, appraisal, uses=None):
    checks={
      'identificacao':bool(source.get('authors') and source.get('title') and source.get('year')),
      'doi_registrado':bool(re.fullmatch(r'10\.\d{4,9}/\S+',source.get('doi',''),re.I)),
      'url_registrada':source.get('url','').startswith('https://'),
      'localizador_conferido':locator.get('status')=='pagina_conferida' and bool(locator.get('pages_pdf')),
      'conferencia_dirigida':bool(appraisal),
      'limites_registrados':bool(source.get('limitation_pt')),
    }
    ready=all(checks.values())
    fingerprint=hashlib.sha256(json.dumps({'source':source,'locator':locator,'appraisal':appraisal,'uses':uses or []},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
    return {'input_fingerprint':fingerprint,'checks':checks,'status':'apta_para_revisao' if ready else 'pendente',
      'bloqueios':[k for k,v in checks.items() if not v],
      'decisao_final':'nao_registrada','revisor':None,
      'limite':'Triagem documental da paráfrase registrada; não valida instrumento, causalidade, qualidade global ou aprovação escolar.'}
def apply_decision(record, decision):
    if not decision:return record
    required=('revisor','data','justificativa','afirmacoes_conferidas')
    if decision.get('decisao')=='aceita' and decision.get('input_fingerprint')==record['input_fingerprint'] and record['status']=='apta_para_revisao' and all(decision.get(k) for k in required):
      record.update(decisao_final='aceita',revisor=decision['revisor'],decision_evidence=decision)
    else:record.update(decisao_final='pendente',decision_evidence=decision)
    return record
def check_freshness(root, hashes):
    for name,expected in hashes.items():
      if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected:
        raise ValueError('Rastreamento desatualizado: '+name)
def enforce_final_acceptance(report):
    if report['final_accepted']<80:
      raise SystemExit('Entrega final bloqueada: menos de 80 fontes com decisão de inclusão documentada')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--strict',action='store_true');parser.add_argument('--verify-fresh',action='store_true');args=parser.parse_args()
    if args.verify_fresh:
      report=load('admission-report.json');check_freshness(ROOT,report['input_sha256'])
      if args.strict:enforce_final_acceptance(report)
      print('Rastreamento corresponde aos arquivos atuais');return
    sources=load('selected.json');locations=load('source-locators.json')
    appraisals={s['key']:s for s in load('core-source-appraisal.json')['core_sources']}
    decisions=load('admission-decisions.json')['source_decisions']
    plan=load('argumento-abcd.json');rows=[];nodes=[];edges=[]
    for sec in plan['sections']:
      for p in sec['paragraphs']:
        nodes.append({'id':'paragraph:'+p['id'],'type':'Paragraph','section':sec['title'],'ABCD':{k:p[k] for k in 'ABCD'}})
        for key in p['keys']:edges.append({'from':'paragraph:'+p['id'],'to':'source:'+key,'type':'CITES','scope':'paráfrase registrada; sustentação deve ser conferida por afirmação'})
        for i,item in enumerate(p.get('base_parts',[])):
          ident=f"claim:{p['id']}:{i+1}";nodes.append({'id':ident,'type':'Claim','text':item['text']})
          edges.extend([{'from':'paragraph:'+p['id'],'to':ident,'type':'HAS_BASE'},{'from':ident,'to':'source:'+item['key'],'type':'ATTRIBUTED_TO'}])
    for s in sources:
      uses=[p for sec in plan['sections'] for p in sec['paragraphs'] if s['key'] in p['keys']]
      decision=apply_decision(assess(s,locations[s['key']],appraisals.get(s['key']),uses),decisions.get(s['key']))
      rows.append({'key':s['key'],'doi':s['doi'],'reading_url':locations[s['key']]['reading_url'],'pages':locations[s['key']]['pages_printed'],**decision})
      nodes.append({'id':'source:'+s['key'],'type':'Source','doi':s['doi'],'title':s['title'],'decision':decision['status']})
      for criterion,passed in decision['checks'].items():edges.append({'from':'source:'+s['key'],'to':'criterion:'+criterion,'type':'CHECK_RESULT','passed':passed})
    nodes += [{'id':'criterion:'+k,'type':'AdmissionCriterion','name':k} for k in rows[0]['checks']]
    model=json.loads((ROOT/'docs/school-model-requirements.json').read_text())
    nodes.append({'id':'artifact:entrega-escolar','type':'Artifact','path':'paper/entrega-escolar.tex'})
    for req in model['requirements']:
      nodes.append({'id':'requirement:'+req['id'],'type':'Requirement',**req})
      edges.append({'from':'artifact:entrega-escolar','to':'requirement:'+req['id'],'type':'MAPS_TO','state':req['status']})
    inputs=[ROOT/'study/literature'/n for n in ['selected.json','source-locators.json','argumento-abcd.json','core-source-appraisal.json','admission-decisions.json']]+[ROOT/'docs/school-model-requirements.json']
    digest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    report={'policy':'Triagem local conservadora; apta para revisão não equivale a aceita pelo orientador. Referências de trabalho permanecem provisórias até decisão registrada.',
      'counts':dict(Counter(r['status'] for r in rows)),'final_accepted':sum(r['decisao_final']=='aceita' for r in rows),'input_sha256':digest,'records':rows}
    out=ROOT/'study/literature';(out/'admission-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (out/'evidence-graph.json').write_text(json.dumps({'nodes':nodes,'edges':edges,'limits':'Grafo documental próprio, separado do grafo de código do codebase-memory-mcp; uma aresta não comprova sustentação.'},ensure_ascii=False,indent=2)+'\n')
    with (out/'admission-report.csv').open('w',newline='') as f:
      w=csv.writer(f);w.writerow(['key','status','decisao_final','pagina_impressa','DOI','URL','bloqueios'])
      for r in rows:w.writerow([r['key'],r['status'],r['decisao_final'],r['pages'],r['doi'],r['reading_url'],'; '.join(r['bloqueios'])])
    md=['# Rastreabilidade e admissibilidade','',report['policy'],'',f"Fontes aptas para revisão: {report['counts'].get('apta_para_revisao',0)}; pendentes: {report['counts'].get('pendente',0)}; decisões finais registradas: {report['final_accepted']}.",'','| Fonte | Triagem | Página | Bloqueios |','|---|---|---|---|']
    md += [f"| {r['key']} | {r['status']} | {r['pages'] or 'pendente'} | {', '.join(r['bloqueios']) or 'nenhum bloqueio documental deste controle'} |" for r in rows]
    (out/'admission-report.md').write_text('\n'.join(md)+'\n');print(report['counts'])
    if args.strict:enforce_final_acceptance(report)
if __name__=='__main__':main()
