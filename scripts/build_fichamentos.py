"""Guided reading records from attributed claims; no invented quality ratings."""
import json
from pathlib import Path
from build_literature import tex,GROUPS
ROOT=Path(__file__).resolve().parents[1]
PROMPTS={
 'education':('Relacionar suporte ao planejamento com o ciclo autorregulatório, preservando o limite entre registro e aprendizagem','Planejar uma avaliação futura de processos e compreensão, sem usar conclusão de tarefa como desfecho educacional'),
 'accessibility':('Identificar a dimensão de barreira ou usabilidade discutida, sem presumir representatividade da escola','Preparar uma inspeção ou estudo contextual que registre tarefa, barreira e critério; não declarar acessibilidade pela execução funcional'),
 'offline-security':('Distinguir ameaça, mecanismo de armazenamento e comportamento observado no MVP','Converter uma ameaça pertinente em cenário seguro com condição, entrada, resultado esperado e evidência; não declarar vulnerabilidade antes de reproduzir'),
 'engineering':('Separar tipo de teste, plataforma e requisito observado','Reproduzir apenas procedimentos compatíveis com a implementação, registrando versão e ambiente; não transferir validação de ferramentas automaticamente'),
 'supplemental':('Distinguir recomendação metodológica, instrumento e evidência de validade','Auditar seleção, atribuição e limitações; qualquer rubrica local exige estudo próprio antes de ser chamada de validada')}
def main():
 sources=json.loads((ROOT/'study/literature/selected.json').read_text())
 core={s['key']:s for s in json.loads((ROOT/'study/literature/core-source-appraisal.json').read_text())['core_sources']}
 rows=[]
 for s in sources:
  c=core.get(s['key'],{})
  relation,opportunity=PROMPTS[s['group']]
  opportunity={
   'SU10':'Propor um roteiro que separe meta, estratégia, acompanhamento e reflexão; conferir cada componente com o modelo antes de implementar, sem tratar o registro como instrumento validado',
   'SU11':'Documentar pergunta, critérios de seleção, acesso e cadeia afirmação–fonte; confirmar no original cada paráfrase usada no manuscrito',
   'education_araka2020':'Extrair população, operacionalização, instrumentos e evidências de validade antes de escolher uma medida futura; manter minutes e done como dados de tarefa',
   'education_prasse2024':'Mapear funcionalidades propostas às fases do ciclo e registrar sobreposição entre revisões; avaliar separadamente a utilidade de cada suporte em investigação futura',
   'education_palalas2020':'Extrair separadamente achados favoráveis, neutros e desfavoráveis e condições de uso; formular hipóteses alternativas antes de atribuir benefício ao organizador',
   'eng06':'Selecionar um atributo não funcional, plataforma e procedimento reproduzível; registrar ambiente, condição de falha e resultado esperado antes do ensaio técnico'
  }.get(s['key'],opportunity)
  rows.append(dict(key=s['key'],reference=s['authors'],title=s['title'],year=s['year'],url='https://doi.org/'+s['doi'] if s.get('doi') else s['url'],kind=s['kind'],access=s['access_level'],location=c.get('location','Resumo/metadados: localizar seção e página no texto integral antes de uso metodológico'),methods_observed=c.get('methods_observed','Método e amostra não extraídos nesta ficha; consultar o original'),finding=s['claim_pt'],limit=s['limitation_pt']+' '+c.get('limit','Não foi realizada avaliação integral e uniforme de risco de viés'),strength=c.get('judgement','Apoio preliminar restrito à paráfrase registrada; não permite inferência causal sobre o MVP'),connection=relation,opportunity=opportunity,paragraphs=[p['id'] for sec in json.loads((ROOT/'study/literature/argumento-abcd.json').read_text())['sections'] for p in sec['paragraphs'] if s['key'] in p['keys']],status='conferência dirigida' if c else 'ficha preliminar'))
 (ROOT/'study/literature/fichamentos-orientados.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 intro='Caderno de orientação com 80 registros; fichamento não substitui leitura integral nem demonstra qualidade metodológica de todas as fontes (Snyder, 2019, DOI10.1016/j.jbusres.2019.07.039). As oportunidades abaixo são propostas do projeto, separadas dos achados atribuídos, e não benefícios já demonstrados (EstudaOffline, 2026, protocolo).'
 md=['# Fichamentos orientados — EstudaOffline','',intro,'','## Como trabalhar com uma ficha','','1. Abrir a fonte e confirmar nível de acesso e localizador.','2. Extrair pergunta, população, desenho, amostra, instrumentos, resultado e limites; marcar não disponível quando ausente.','3. Separar achado do autor de proposta do projeto e identificar se o achado responde à afirmação pretendida.','4. Escrever A, sustentar B, comparar/aplicar com limite em C e ligar D ao conceito seguinte.','5. Conferir a paráfrase no original e documentar a revisão antes de incorporar ao manuscrito.','','Procedimento local de orientação, sem escore de validade científica; adaptação apoiada na transparência de síntese discutida por Snyder (2019).','','## Mapa do argumento','','Planejamento → apoio digital condicionado → amplitude do ciclo → validade dos registros → verificação técnica → acessibilidade → método → resultados → limites → continuidade (Panadero, 2017; Araka et al., 2020; Prasse et al., 2024; EstudaOffline, 2026).','']
 latex=[r'\section*{Caderno de fichamentos orientados}',tex(intro),r'\section*{Uso na orientação}',r'Consultar o original, conferir localizadores, separar achado de proposta e testar a sustentação da paráfrase antes de incorporá-la ao argumento \citep{SU11}. O modelo ABCD é uma convenção editorial proposta pelo orientador, sem alegação de validação empírica \citep{projeto}. As oportunidades de pesquisa são propostas, não resultados do MVP \citep{projeto}.']
 labels={'access':'Acesso efetivo','location':'Localizador consultado','methods_observed':'Método observado','finding':'Achado atribuível','strength':'Força pertinente ao argumento','limit':'Limitação e transferência','connection':'Relação com a pesquisa — proposta','opportunity':'Oportunidade e tarefa — proposta','status':'Estado da ficha'}
 for i,s in enumerate(rows,1):
  md.extend([f"## {i:02d}. {s['key']} — {s['title']}",'',f"**Referência:** {'; '.join(s['reference'])}. {s['year']}. {s['url']}",''])
  latex.extend([r'\clearpage\section*{Ficha '+str(i)+': '+tex(s['title'])+'}',r'Fonte: \citet{'+s['key']+'}.'])
  for field,label in labels.items():
   val=s[field];citation='EstudaOffline, 2026, protocolo' if field in ['connection','opportunity','status','access','location','methods_observed'] else f"{s['reference'][0]}, {s['year']}"
   md.append(f'**{label}:** {val} ({citation}).\n')
   latex.append(r'\noindent\textbf{'+tex(label)+':} '+tex(val.rstrip('.'))+r' \citep{'+('projeto' if field in ['connection','opportunity','status','access','location','methods_observed'] else s['key'])+r'}.\par\medskip')
  used=', '.join(s['paragraphs']) or 'Não usada no manuscrito conciso; leitura complementar'
  md.append(f'**Destino:** {used} (EstudaOffline, 2026, mapa ABCD).\n')
  latex.append(r'\noindent\textbf{Destino no argumento:} '+tex(used)+r' \citep{projeto}.')
 (ROOT/'study/literature/fichamentos-orientados.md').write_text('\n'.join(md)+'\n')
 full=(ROOT/'paper/bibliography.tex').read_text()
 import re
 entries=re.findall(r'\\bibitem.*?(?=\\bibitem|\\end\{thebibliography\})',full,re.S)
 keep={s['key'] for s in sources}|{'projeto'}
 kept=[e for e in entries if re.search(r'\]\{([^}]+)\}',e)[1] in keep]
 (ROOT/'paper/references-fichamentos.tex').write_text(r'\begin{thebibliography}{99}'+'\n'+ '\n'.join(kept)+r'\end{thebibliography}'+'\n')
 (ROOT/'paper/fichamentos-conteudo.tex').write_text('\n\n'.join(latex)+'\n')
 prefix=(ROOT/'paper/artigo.tex').read_text().split(r'\title')[0]
 (ROOT/'paper/fichamentos.tex').write_text(prefix+r'\begin{document}\sloppy\input{fichamentos-conteudo.tex}\clearpage\input{references-fichamentos.tex}\end{document}'+'\n')
 print({'records':len(rows),'directed_core':len(core),'not_used_in_short_manuscript':sum(not r['paragraphs'] for r in rows)})
if __name__=='__main__':main()
