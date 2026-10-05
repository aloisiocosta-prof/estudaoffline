"""Regression checks for false-positive editorial audit approvals."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import fitz
import audit_latex

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

if __name__ == '__main__':
    unittest.main()
