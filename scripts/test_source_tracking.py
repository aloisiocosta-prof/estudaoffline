import hashlib,tempfile,unittest
from pathlib import Path
from track_sources import assess,apply_decision,check_freshness
class AdmissionTests(unittest.TestCase):
    def setUp(self):
      self.s={'authors':['Autor'],'title':'Título','year':2020,'doi':'10.1234/test','url':'https://doi.org/10.1234/test','limitation_pt':'Escopo limitado'}
      self.l={'status':'pagina_conferida','pages_pdf':[3]}
    def test_doi_alone_does_not_admit(self):
      self.assertEqual(assess(self.s,{},None)['status'],'pendente')
    def test_verified_locator_still_needs_appraisal(self):
      self.assertEqual(assess(self.s,self.l,None)['status'],'pendente')
    def test_ready_does_not_imply_approval(self):
      r=assess(self.s,self.l,{'judgement':'apoio delimitado'})
      self.assertEqual(r['status'],'apta_para_revisao');self.assertEqual(r['decisao_final'],'nao_registrada')
    def test_missing_limits_blocks(self):
      self.s['limitation_pt']='';self.assertIn('limites_registrados',assess(self.s,self.l,{'judgement':'apoio'})['bloqueios'])
    def test_approval_without_evidence_does_not_pass(self):
      r=assess(self.s,self.l,{'judgement':'apoio'})
      self.assertEqual(apply_decision(r,{'decisao':'aceita'})['decisao_final'],'pendente')
    def test_approval_cannot_override_missing_locator(self):
      d={'decisao':'aceita','revisor':'Revisor de teste','data':'2026-10-05','justificativa':'Teste sintético','afirmacoes_conferidas':['Teste sintético']}
      self.assertEqual(apply_decision(assess(self.s,{},None),d)['decisao_final'],'pendente')
    def test_stale_approval_is_rejected(self):
      r=assess(self.s,self.l,{'judgement':'apoio'})
      d={'decisao':'aceita','input_fingerprint':'stale','revisor':'Teste','data':'2026-10-05','justificativa':'Teste','afirmacoes_conferidas':['Teste']}
      self.assertEqual(apply_decision(r,d)['decisao_final'],'pendente')
    def test_documented_approval_passes_only_current_input(self):
      r=assess(self.s,self.l,{'judgement':'apoio'})
      d={'decisao':'aceita','input_fingerprint':r['input_fingerprint'],'revisor':'Revisor sintético','data':'2026-10-05','justificativa':'Fixture de teste','afirmacoes_conferidas':['Fixture de teste']}
      self.assertEqual(apply_decision(r,d)['decisao_final'],'aceita')
      changed=assess(self.s,self.l,{'judgement':'apoio'},[{'text':'alterado'}])
      self.assertEqual(apply_decision(changed,d)['decisao_final'],'pendente')
    def test_changed_input_blocks_stale_graph(self):
      with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);p=root/'input.json';p.write_text('original')
        hashes={'input.json':hashlib.sha256(p.read_bytes()).hexdigest()}
        check_freshness(root,hashes)
        p.write_text('alterado')
        with self.assertRaisesRegex(ValueError,'desatualizado'):check_freshness(root,hashes)
if __name__=='__main__':unittest.main()
