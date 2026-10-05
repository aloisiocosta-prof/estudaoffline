"""Map shared prose to the supplied school model without changing the article."""
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    text=(ROOT/'paper/argumento.tex').read_text()
    chunks=re.split(r'\\clearpage\\section\{([^}]+)\}',text)
    sec={chunks[i]:chunks[i+1].strip() for i in range(1,len(chunks),2)}
    intro=r'O EstudaOffline investiga o planejamento de tarefas sintéticas. Panadero descreve a autorregulação como antecipação, execução e reflexão \citep[p. 1, 3]{SU10}. Organizar tarefas abrange apenas parte desse processo \citep[p. 1, 3]{SU10}. Essa delimitação orienta a investigação técnica sem presumir benefícios educacionais \citep[p. 1, 3]{SU10}.'
    intro+='\n\n'+'A investigação concentra-se'+sec['Introdução'].split('A investigação concentra-se',1)[1]
    body=[r'\section{Introdução}',intro,
      r'\subsection{Objetivos}',r'\subsubsection{Objetivo geral}',
      'Examinar a conservação e a manipulação de tarefas sintéticas no EstudaOffline por cenários técnicos reproduzíveis, delimitando persistência local, disponibilidade sem conexão e backup.',
      r'\subsubsection{Objetivos específicos}',r'\begin{enumerate}',
      r'\item Implementar o organizador Flutter web com criação, conclusão, armazenamento local e importação e exportação de tarefas sintéticas.',
      r'\item Verificar cenários técnicos de funcionamento e falha, registrando resultados, ambiente e limites sem inferir eficácia pedagógica.',r'\end{enumerate}',
      r'\subsection{Metodologia}',sec['Métodos'].split('A leitura das fontes')[0].strip(),
      r'A literatura foi organizada em síntese narrativa. Snyder relaciona a modalidade de revisão à pergunta e à transparência da seleção \citep[p. 336–337]{SU11}. Foram fichadas 80 publicações com níveis de acesso registrados, sem presumir 80 validações independentes. Esse registro delimita a interpretação técnica desenvolvida nos apêndices.',
      r'\clearpage\section{Referencial teórico}',sec['Referencial teórico'],
      r'\clearpage\section{Considerações finais}',sec['Considerações finais'],
      r'\clearpage\begingroup\linespread{1}\selectfont\setlength{\bibsep}{12pt}',
      r'\renewcommand{\refname}{4 Referências}\phantomsection\addcontentsline{toc}{section}{Referências}',
      r'\input{references-core.tex}\endgroup',
      r'\clearpage\section*{Apêndices}\phantomsection\addcontentsline{toc}{section}{Apêndices}',
      'Os apêndices preservam a síntese ampliada e os registros técnicos produzidos para a orientação. A lista bibliográfica é um corpus provisório: cinco fichas estão aptas para revisão documental e 75 têm pendências; a aprovação final de inclusão não está registrada. Os estados são auditáveis em admission-report.json, separados das evidências dos autores. A seleção e a extração devem permanecer transparentes '+r'\citep[p. 336–337]{SU11}.',
      r'\subsection*{Apêndice A Resultados técnicos}',sec['Resultados'],
      r'\subsection*{Apêndice B Discussão dos limites}',sec['Discussão']]
    for i,(title,content) in enumerate(sec.items()):
      if title not in ['Introdução','Referencial teórico','Métodos','Resultados','Discussão','Considerações finais']:
        body.extend([r'\clearpage\subsection*{'+title+'}',content])
    body += [r'\clearpage\section*{Anexos}\phantomsection\addcontentsline{toc}{section}{Anexos}',
      'Não foram incorporados documentos externos como anexos nesta demonstração. O modelo escolar foi consultado para organizar a entrega; os artigos científicos permanecem identificados por suas referências e endereços de leitura, sem reprodução integral de documentos de terceiros.']
    (ROOT/'paper/entrega-conteudo.tex').write_text('\n\n'.join(body)+'\n')
if __name__=='__main__':main()
