"""Pinned optional technical graph; never validates a scientific publication."""
import hashlib,json,re,subprocess,tarfile,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='v0.11.0'
ARCHIVE='codebase-memory-mcp-linux-amd64.tar.gz'
SHA256='032b33c1833919a2d1de67ff6367fa6ea46aee8689c86ef223c88fae3b6e4536'
def main():
 out=ROOT/'study/technical-graph';out.mkdir(exist_ok=True)
 base=ROOT/'build/codebase-memory';base.mkdir(parents=True,exist_ok=True)
 url=f'https://github.com/DeusData/codebase-memory-mcp/releases/download/{VERSION}/{ARCHIVE}'
 data=urllib.request.urlopen(url,timeout=60).read()
 assert hashlib.sha256(data).hexdigest()==SHA256,'Archive checksum mismatch'
 archive=base/ARCHIVE;archive.write_bytes(data)
 with tarfile.open(archive) as t:t.extractall(base,filter='data')
 binary=next(base.rglob('codebase-memory-mcp'))
 commands=[['index_repository','--repo-path',str(ROOT),'--name','estudaoffline','--mode','full','--persistence','false'],['get_graph_schema','--project','estudaoffline'],['query_graph','--project','estudaoffline','--query',"MATCH (f:Function) WHERE f.name CONTAINS 'assess' RETURN f.name LIMIT 20"]]
 results=[]
 for args in commands:
  p=subprocess.run([str(binary),'cli','--json',*args],capture_output=True,text=True,timeout=120)
  envelope=json.loads(p.stdout) if p.stdout.strip() else {}
  results.append({'tool':args[0],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'tool_error':envelope.get('isError',False)})
  if p.returncode or envelope.get('isError'):break
 query_text=' '.join(c.get('text','') for c in envelope.get('content',[]))
 target_found=len(results)==3 and bool(re.search(r'\brows:\s*[1-9]\d*',query_text))
 report={'version':VERSION,'archive_sha256':SHA256,'results':results,'target_assess_found':target_found,'success':len(results)==3 and target_found and all(r['returncode']==0 and not r['tool_error'] for r in results),'scope':'Code graph only; bibliographic support is tracked separately in evidence-graph.json.'}
 (out/'codebase-memory-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'version':VERSION,'success':report['success'],'tools':[r['tool'] for r in results],'returncodes':[r['returncode'] for r in results]}))
 if not report['success']:raise SystemExit('Technical indexing failed; inspect recorded evidence')
if __name__=='__main__':
 try:main()
 except Exception as error:
  out=ROOT/'study/technical-graph';out.mkdir(exist_ok=True)
  (out/'codebase-memory-report.json').write_text(json.dumps({'version':VERSION,'archive_sha256':SHA256,'success':False,'error':str(error),'scope':'Technical code indexing only'},indent=2)+'\n')
  raise
