"""Verified locator formatting; DOI does not certify methodological quality."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def locators():return json.loads((ROOT/'study/literature/source-locators.json').read_text())
def citation(keys,command='citep',records=None):
    records=locators() if records is None else records
    # Separate citations prevent page notes for one publication being attributed to another.
    parts=[]
    for key in keys:
        entry=records.get(key,{})
        note=entry.get('citation_locator') if entry.get('status')=='pagina_conferida' else None
        parts.append('\\'+command+('['+note+']' if note else '')+'{'+key+'}')
    return ' '.join(parts)
