"""Auditable source counts and PDF line occupancy (PyMuPDF required locally)."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def expand(path, seen=None):
    seen = set() if seen is None else seen
    if path in seen:
        raise ValueError('Recursive LaTeX include')
    seen.add(path)
    text = path.read_text()
    text = re.sub(r'\\input\{([^}]+)\}', lambda m: expand(path.parent / m[1], seen.copy()), text)
    return text

def audit_sources():
    selected = json.loads((ROOT/'study/literature/selected.json').read_text())
    keys = {s['key'] for s in selected}
    assert len(keys) == len(selected) >= 80
    result = {}
    for name in ['artigo', 'entrega-escolar', 'poster']:
        text = expand(ROOT/'paper'/f'{name}.tex')
        cites = {k.strip() for m in re.finditer(r'\\cite(?:p|t)?\{([^}]+)\}', text) for k in m[1].split(',')}
        bibs = set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text))
        assert not (keys-cites), (name, 'missing science citations', sorted(keys-cites))
        assert not (cites-bibs), (name, 'undefined source keys', sorted(cites-bibs))
        result[name] = {'scientific_publications_cited':len(keys & cites),
            'bibliography_entries':len(bibs), 'undefined_keys':sorted(cites-bibs),
            'uncited_bibliography_entries':sorted(bibs-cites)}
    return result

def audit_pdf(directory):
    import fitz
    results = {}
    short_rows = ['document,page,line,width_ratio,text']
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['document','page','line','width_ratio','text'])
    for name in ['artigo','entrega-escolar','poster']:
        doc = fitz.open(directory / (name+'.pdf'))
        total = short = 0
        for page_no,page in enumerate(doc,1):
            # A1 margin30mm; A4 article25mm; school30mm left20mm right.
            margin_mm = 60 if name == 'poster' else 50
            width = page.rect.width-margin_mm*72/25.4
            # Links and citation runs can be separate extraction blocks on the
            # same printed line. Reassemble by baseline before measuring.
            physical = []
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        if span['text'].strip():
                            physical.append(span)
            bands = []
            for span in sorted(physical,key=lambda s:(s['origin'][1],s['bbox'][0])):
                match = next((b for b in bands if abs(b[0]-span['origin'][1]) < 1.5),None)
                if match is None:
                    bands.append([span['origin'][1],[span]])
                else:
                    match[1].append(span)
            for _,spans in bands:
                spans.sort(key=lambda s:s['bbox'][0])
                text = ' '.join(s['text'] for s in spans).strip()
                total += 1
                ratio = (max(s['bbox'][2] for s in spans)-min(s['bbox'][0] for s in spans))/width
                if ratio < .5:
                    short += 1
                    writer.writerow([name,page_no,total,round(ratio,4),text])
        results[name] = {'pages':len(doc),'text_lines':total,'lines_below_half_width':short,
            'literal_every_line_requirement_met':short == 0,
            'definition':'horizontal text bounding box / usable page width; single-column layout; all extracted text lines included'}
    (ROOT/'study/line-occupancy.csv').write_text(output.getvalue())
    return results

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--pdf-dir',type=Path)
    args=parser.parse_args()
    report={'sources':audit_sources(),
        'limitations':['Source count is not validation of eighty instruments or eighty independent experiments.',
            'Abstract-based paraphrases do not imply full-text review or source retraction screening.',
            'The 50% line-width threshold is an editorial requirement, not a validated scientific quality metric.']}
    if args.pdf_dir:
        report['pdf_lines']=audit_pdf(args.pdf_dir)
    (ROOT/'study/editorial-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
