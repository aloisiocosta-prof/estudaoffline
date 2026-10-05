"""Regression checks for false-positive editorial audit approvals."""
import tempfile
import json
from contextlib import contextmanager
import unittest
from pathlib import Path
from unittest.mock import patch
import fitz
import audit_latex
from source_citations import citation

class EditorialAuditTests(unittest.TestCase):
    def test_document_without_pages_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'study').mkdir()
            with patch('fitz.open', return_value=[]), patch.object(audit_latex, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'no pages'):
                    audit_latex.audit_pdf(root)

    def test_blank_page_is_not_approved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'study').mkdir()
            for name in ['artigo', 'entrega-escolar', 'poster']:
                doc = fitz.open()
                doc.new_page()
                doc.save(root / (name + '.pdf'))
                doc.close()
            with patch.object(audit_latex, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'no extractable text'):
                    audit_latex.audit_pdf(root)

    def test_spaces_do_not_count_as_characters(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'study').mkdir()
            for name in ['artigo', 'entrega-escolar', 'poster']:
                doc = fitz.open()
                page = doc.new_page(width=595, height=842)
                page.insert_text((50, 100), 'A' + ' ' * 60 + 'B', fontsize=20)
                doc.save(root / (name + '.pdf'))
                doc.close()
            with patch.object(audit_latex, 'ROOT', root):
                report = audit_latex.audit_pdf(root)
            self.assertEqual(report['artigo']['lines_below_half_width'], 0)
            self.assertFalse(report['artigo']['literal_every_line_requirement_met'])
            self.assertGreater(report['artigo']['lines_below_half_character_width'], 0)


    @contextmanager
    def source_fixture(self):
        selected=json.loads((audit_latex.ROOT/'study/literature/selected.json').read_text())
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'study/literature').mkdir(parents=True);(root/'paper').mkdir()
            (root/'study/literature/selected.json').write_text(json.dumps(selected))
            keys=[s['key'] for s in selected]
            text=r'\citep{'+','.join(keys)+'}'+ '\n'.join(r'\bibitem{'+k+'} Source' for k in keys)
            for name in ['artigo','entrega-escolar','poster','fichamentos']:(root/'paper'/(name+'.tex')).write_text(text)
            with patch.object(audit_latex,'ROOT',root):
                audit_latex.audit_sources() # baseline fixture passes before each invalid mutation
                yield root,selected

    def test_own_study_bibliography_is_rejected(self):
        with self.source_fixture() as (root,selected):
            path=root/'paper/artigo.tex'
            path.write_text(path.read_text()+r'\citep{projeto}\bibitem{projeto} Own study')
            with self.assertRaisesRegex(AssertionError,'own-study bibliography prohibited'):audit_latex.audit_sources()

    def test_missing_scientific_doi_is_rejected(self):
        with self.source_fixture() as (root,selected):
            selected[0].pop('doi');(root/'study/literature/selected.json').write_text(json.dumps(selected))
            with self.assertRaisesRegex(AssertionError,'requires DOI and URL'):audit_latex.audit_sources()

    def test_fewer_than_eighty_sources_is_rejected(self):
        with self.source_fixture() as (root,selected):
            (root/'study/literature/selected.json').write_text(json.dumps(selected[:79]))
            with self.assertRaises(AssertionError):audit_latex.audit_sources()


    def test_unverified_page_note_is_not_emitted(self):
        records={'source':{'status':'pagina_pendente','citation_locator':'p. 99'}}
        self.assertEqual(citation(['source'],records=records),r'\citep{source}')

    def test_verified_page_note_is_emitted(self):
        records={'source':{'status':'pagina_conferida','citation_locator':'p. 336–337'}}
        self.assertEqual(citation(['source'],records=records),r'\citep[p. 336–337]{source}')

    def test_source_audit_accepts_optional_locator(self):
        with self.source_fixture() as (root,selected):
            path=root/'paper/artigo.tex'
            path.write_text(path.read_text().replace(r'\citep{',r'\citep[sec. Abstract]{',1))
            self.assertEqual(audit_latex.audit_sources()['artigo']['scientific_publications_cited'],80)

if __name__ == '__main__':
    unittest.main()
