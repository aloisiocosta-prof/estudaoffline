from pathlib import Path
import re,sys
version=sys.argv[1]
if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+',version): raise ValueError('invalid SemVer')
p=Path('pubspec.yaml')
p.write_text(re.sub(r'^version:.*$', 'version: '+version+'+1',p.read_text(),flags=re.M))
