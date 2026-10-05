from pathlib import Path
import hashlib,json,sys
p=Path(sys.argv[1] if len(sys.argv)>1 else 'build/web')
index=p/'index.html';s=index.read_text();s=s.replace('<!-- OFFLINE_BOOTSTRAP -->',Path('web/offline-bootstrap.html').read_text());index.write_text(s)
files=sorted(x.relative_to(p).as_posix() for x in p.rglob('*') if x.is_file() and x.suffix not in ('.map',) and x.name not in ('sw.js','flutter_service_worker.js'))
fingerprint=hashlib.sha256()
for f in files:
    # Asset paths are part of the cache contract, even when bytes are identical.
    fingerprint.update(f.encode('utf-8')+b'\0')
    fingerprint.update(hashlib.sha256((p/f).read_bytes()).digest())
version=fingerprint.hexdigest()[:16]
source=Path('web/sw-template.js').read_text().replace('__VERSION__',version).replace('__FILES__',json.dumps(files))
(p/'sw.js').write_text(source)
print(json.dumps({'version':version,'cached_files':len(files),'bytes':sum((p/f).stat().st_size for f in files)}))
