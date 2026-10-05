"""Build transparent paraphrase/source appendices; never manufacture references."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    'education': 'Planejamento e autorregulação da aprendizagem',
    'accessibility': 'Acessibilidade, usabilidade e desigualdade digital',
    'offline-security': 'Persistência local, cache, segurança e privacidade',
    'engineering': 'Engenharia, testes e reprodutibilidade',
    'supplemental': 'Integridade, atribuição e revisão da escrita',
}
EXCLUDED = {'OS04', 'OS05', 'OS11', 'OS12', 'OS16', 'OS19', 'OS20', 'eng19', 'eng09'}

def tex(s):
    return ''.join({'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
                    '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
                    '^': r'\textasciicircum{}', '\\': r'\textbackslash{}'}.get(c, c) for c in str(s))

def main():
    selected, excluded, seen = [], [], set()
    for group in GROUPS:
        path = ROOT / 'study/literature' / (group + '.json')
        if not path.exists():
            continue
        for source in json.loads(path.read_text()):
            source = dict(source, group=group)
            identity = (source.get('doi') or re.sub(r'\W', '', source['title']).lower()).lower()
            if source['key'] in EXCLUDED or 'preprint' in source['kind'].lower() or identity in seen:
                excluded.append(source)
                continue
            assert source['authors'] and source['claim_pt'] and source['limitation_pt']
            seen.add(identity)
            selected.append(source)
    selected.sort(key=lambda s: (list(GROUPS).index(s['group']), s['key']))
    (ROOT / 'study/literature/selected.json').write_text(json.dumps(selected, ensure_ascii=False, indent=2))
    (ROOT / 'study/literature/excluded.json').write_text(json.dumps(excluded, ensure_ascii=False, indent=2))
    synthesis = [r'\section{Fundamentação rastreável e limites de transferência}',
        r'Esta síntese exploratória relaciona planejamento, interfaces, funcionamento local, engenharia e integridade da escrita. Foram consultados principalmente resumos e metadados; não foi realizada avaliação sistemática do risco de viés de cada estudo. As fontes sustentam os enunciados delimitados abaixo, sem validar o EstudaOffline nem comprovar aprendizagem. O registro de busca e seleção integra o protocolo do projeto \citep{projeto}.']
    bib = [r'\begin{thebibliography}{99}']
    rows = ['# Matriz de afirmações e fontes', '',
            '| Chave | Afirmação indireta | Limite | Tipo | Acesso | Fonte |',
            '|---|---|---|---|---|---|']
    def author_label(s):
        names = s.get('citation_names') or [name.split()[-1] for name in s['authors']]
        return names[0] + (' et al.' if len(names) > 2 else (' e ' + names[1] if len(names) == 2 else ''))
    from collections import Counter, defaultdict
    label_counts = Counter((author_label(s), s['year']) for s in selected)
    label_index = defaultdict(int)
    current = None
    for s in selected:
        if current != s['group']:
            current = s['group']
            synthesis.append(r'\subsection{' + GROUPS[current] + '}')
        synthesis.append(tex(s['claim_pt']) + ' ' + tex(s['limitation_pt']) + r' \citep{' + s['key'] + '}.\n')
        label = author_label(s)
        pair = (label, s['year'])
        suffix = chr(97+label_index[pair]) if label_counts[pair] > 1 else ''
        label_index[pair] += 1
        venue = s.get('journal') or s.get('venue') or s.get('publication_venue') or s['kind']
        bib.append(r'\bibitem[' + tex(label) + '(' + str(s['year']) + suffix + ')]{' + s['key'] + '} ' +
                   tex('; '.join(s['authors'])) + '. ' + tex(s['title']) + '. ' + tex(venue) + ', ' + str(s['year']) + '. ' +
                   (r'DOI: \url{https://doi.org/' + s['doi'] + '}.' if s.get('doi') else r'URL: \url{' + s['url'].split('?')[0] + '}.') +
                   ' Metadados e resumo consultados em 5 out. 2026.')
        rows.append('| ' + ' | '.join(str(s.get(k, '')).replace('|','/').replace('\n',' ') for k in ['key','claim_pt','limitation_pt','kind','access_level','url']) + ' |')
    for key, label, title, url in [
        ('flutter','Flutter','Web FAQ','https://docs.flutter.dev/platform-integration/web/faq'),
        ('local','MDN','Window: localStorage property','https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage'),
        ('quota','MDN','Storage quotas and eviction criteria','https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria'),
        ('sw','MDN','Service Worker API','https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API'),
        ('projeto','EstudaOffline','Protocolo, buscas e observações técnicas do projeto','https://github.com/aloisiocosta-prof/estudaoffline/tree/main/study'),
    ]:
        suffix = {'local':'a','quota':'b','sw':'c'}.get(key,'')
        bib.append(r'\bibitem['+label+'(2026'+suffix+')]{'+key+'} '+label+'. '+tex(title)+r'. \url{'+url+'}. Acesso em 5 out. 2026. Registro técnico, fora da contagem de fontes científicas.')
    bib.append(r'\end{thebibliography}')
    (ROOT/'paper/literature.tex').write_text('\n\n'.join(synthesis).replace('\\n','\n'))
    (ROOT/'paper/bibliography.tex').write_text('\n\n'.join(bib))
    (ROOT/'study/literature/claim-source-matrix.md').write_text('\n'.join(rows)+'\n')
    print(json.dumps({'selected':len(selected),'excluded':len(excluded),'minimum_met':len(selected)>=80}))

if __name__ == '__main__':
    main()
