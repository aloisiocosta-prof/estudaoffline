"""Verify the requested minimum of three content pages in compiled documents."""
import argparse
import json
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf-dir', type=Path, required=True)
    args = parser.parse_args()
    report = {}
    for name in ['artigo', 'entrega-escolar']:
        doc = fitz.open(args.pdf_dir / (name + '.pdf'))
        # Numbered outline entries distinguish the section from the school TOC.
        toc = doc.get_toc()
        start = next(page for level, title, page in toc if level == 1 and title == 'Referencial teórico')
        following = [page for level, title, page in toc if level == 1 and page > start]
        stop = min(following) - 1
        words = [len(doc[p - 1].get_text().split()) for p in range(start, stop + 1)]
        substantial = sum(count >= 100 for count in words)
        assert substantial >= 3, (name, start, stop, words)
        text = '\n'.join(doc[p - 1].get_text() for p in range(start, stop + 1))
        assert '(??)' not in text
        report[name] = {'start_page': start, 'end_page': stop,
                        'content_pages': stop - start + 1,
                        'pages_with_at_least_100_words': substantial,
                        'extracted_words_per_page': words,
                        'minimum_three_content_pages_met': True,
                        'limitations': 'Page count is editorial verification, not validation of theoretical or scientific claims.'}
    (ROOT / 'study/referencial-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
