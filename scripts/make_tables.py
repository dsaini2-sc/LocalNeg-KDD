"""Generate the paper's data tables (tables/*.tex) from the lab records. Re-run when new seeds land."""
import csv, json, re, statistics as st
from pathlib import Path
V = Path('/home/dsaini2/data/Research/BAGLRQs/v9'); L = V / 'lab13-internal-evidence'; OUT = Path(__file__).resolve().parents[1] / 'tables'
ARMS = [('random', 'Random'), ('fresh_uncapped', 'Fresh clustered'), ('async_uncapped', 'Cached clustered'), ('fresh_capped', 'Fresh clustered, capped'), ('async_capped', 'Cached clustered, capped')]
STEPS = [(5360, '1'), (10520, '2'), (15679, '3')]
pct = lambda x: 100 * float(x)
def ms(xs):
    return f"{st.mean(xs):.2f} $\\pm$ {st.stdev(xs):.2f} ({len(xs)})" if len(xs) > 1 else (f"{xs[0]:.2f} (1)" if xs else '--')
def table(name, spec, header, rows, caption, label, star=False):
    env = 'table*' if star else 'table'
    body = '\n'.join(' & '.join(r) + ' \\\\' for r in rows)
    (OUT / name).write_text(f"\\begin{{{env}}}[t]\n  \\caption{{{caption}}}\n  \\label{{{label}}}\n  \\footnotesize\\setlength{{\\tabcolsep}}{{4pt}}\n  \\begin{{tabular}}{{{spec}}}\n    \\toprule\n    {header} \\\\\n    \\midrule\n{body}\n    \\bottomrule\n  \\end{{tabular}}\n\\end{{{env}}}\n")

# Every internal number is the mean of the three seeds (all fifteen cells of each seed collected 2026-09-30).
SEEDS = ('1504', '1505', '1506')
internal = [r for r in csv.DictReader(open(L / 'full-scale-replicates/evaluation/analysis/metrics.csv')) if r['seed'] in SEEDS]
get = lambda arm, step, k='macro_recall_at_1000': [pct(r[k]) for r in internal if r['arm'] == arm and int(r['step']) == step]
sd = max(st.stdev(get(a, s)) for a, _ in ARMS for s, _ in STEPS if len(get(a, s)) > 1)
table('internal.tex', 'lrrr', 'Method & 1 epoch & 2 epochs & 3 epochs',
      [[n] + [f"{st.mean(get(a, s)):.2f}" for s, _ in STEPS] for a, n in ARMS],
      f'Macro recall@1000 (\\%) on the frozen production panel (38.96M queries, 85.3M candidates), mean over three seeds; the standard deviation across seeds is at most {sd:.1f} points in every cell. All arms share a 200-update random prefix; epochs count the updates after it.',
      'tab:internal')
(OUT / 'internal.tex').write_text(f'% mean of seeds {", ".join(SEEDS)}; seeds per cell (arm: e1/e2/e3): ' + '; '.join(f"{a}: " + '/'.join(str(len(get(a, s))) for s, _ in STEPS) for a, _ in ARMS) + '\n' + (OUT / 'internal.tex').read_text())
cols = [('macro_recall_at_10', '\\recall{10}'), ('macro_recall_at_100', '\\recall{100}'), ('macro_recall_at_500', '\\recall{500}'), ('macro_recall_at_1000', '\\recall{1000}'), ('mrr_at_1000', 'MRR'), ('ndcg_at_10', 'nDCG@10')]
rows = [[e, n] + [f"{st.mean(get(a, s, k)):.2f}" for k, _ in cols] for s, e in STEPS for a, n in ARMS]
table('app_internal.tex', 'll' + 'r' * len(cols), 'Ep. & Method & ' + ' & '.join(h for _, h in cols), rows,
      'Every full-scale metric at one, two and three epochs, mean over three seeds (macro, \\%).', 'tab:app-internal', star=True)
(OUT / 'app_internal.tex').write_text(f'% mean of seeds {", ".join(SEEDS)}\n' + (OUT / 'app_internal.tex').read_text())

pub = list(csv.DictReader(open(V / 'lab14-shared-cached-mining/replicates-s2s3/table.csv')))
DS = [('collab', 'Collab'), ('c2', 'Citation2'), ('lj', 'LiveJournal')]
rows = []
for ep in ('mining', 'continuation'):
    for d, dn in DS:
        for a, n in ARMS:
            for r in sorted((r for r in pub if r['dataset'] == d and r['policy'] == a and r['endpoint'] == ep), key=lambda r: r['seed']):
                rows.append([ep, dn, n, r['seed'], f"{float(r['r10']):.2f}", f"{float(r['r1000']):.2f}", f"{float(r['mrr']):.2f}", f"{float(r['official']):.2f}"])
table('app_public.tex', 'lllrrrrr', 'Endpoint & Graph & Method & Seed & \\recall{10} & \\recall{1000} & MRR & Official', rows,
      'Every public run, per seed (full-corpus filtered metrics and the official metric, \\%; Official = Collab Hits@50, Citation2 and LiveJournal sampled MRR).', 'tab:app-public', star=True)

X = L / 'exposure-ablation/prism-evaluation/runs'   # three-seed means over the per-cell metrics behind READ-three-seeds.md
EXP = [('No exposure negatives', ('ref_base_s1501', 'base_s1502', 'base_s1503')), ('Exposure negatives added back', ('ref_exp_s1501', 'exp_s1502', 'exp_s1503')), ('Same slots, random users', ('ctl_s1501', 'ctl_s1502', 'ctl_s1503'))]
EK = ['macro_recall_at_1', 'macro_recall_at_10', 'macro_recall_at_100', 'macro_recall_at_500', 'macro_recall_at_1000', 'mrr_at_1000', 'ndcg_at_10']
rows = [[n] + [f"{st.mean(pct(json.loads((X / c / 'ranking/ranking_metrics.json').read_text())['metrics'][k]) for c in cells):.4f}" for k in EK] for n, cells in EXP]
table('app_exposure.tex', 'lrrrrrrr', 'Arm & \\recall{1} & \\recall{10} & \\recall{100} & \\recall{500} & \\recall{1000} & MRR & nDCG@10', rows,
      'Exposure negatives, all metrics, mean over three seeds (macro, \\%).', 'tab:app-exposure', star=True)

loc = list(csv.DictReader(open(L / 'embedding-locality-r1/metrics.csv')))
lab = {'hop1': '1 hop', 'hop2': '2 hops', 'hop3': '3 hops', 'random': 'Random user', 'positive': 'Future friend'}
avg = lambda c, k: st.mean(float(r[k]) for r in loc if r['class'] == c)   # the two random-negative models, averaged
assert all(len({r['pairs'] for r in loc if r['class'] == c}) == 1 for c in lab)
rows = [[lab[c], 'full scale', f"{int(next(r['pairs'] for r in loc if r['class'] == c)):,}".replace(',', '{,}'), f"{avg(c, 'mean'):.3f}", f"{avg(c, 'ci_lo'):.3f}--{avg(c, 'ci_hi'):.3f}", f"{avg(c, 'median'):.3f}", f"{avg(c, 'gap_same_degree'):+.3f}"] for c in lab]
pm = [json.loads((L / 'embedding-locality-r1/exposure-probe/metrics.json').read_text())[s] for s in ('s1506', 's1505')]   # the exposure probe, same models
rows.append(['Exposure negative', 'full scale', f"{pm[0]['exposure_pairs_embedded']:,}".replace(',', '{,}'), f"{st.mean(m['mean'] for m in pm):.3f}", f"{st.mean(m['ci'][0] for m in pm):.3f}--{st.mean(m['ci'][1] for m in pm):.3f}", f"{st.mean(m['median'] for m in pm):.3f}", f"{st.mean(m['degree_matched_gap'] for m in pm):+.3f}"])
ctrl = L / 'embedding-locality-r1/mini-control/metrics.csv'
if ctrl.exists():
    for r in csv.DictReader(open(ctrl)):
        rows.append([lab[r['class']], 'mini, ' + r['model'], f"{int(r['pairs']):,}".replace(',', '{,}'), f"{float(r['mean']):.3f}", f"{float(r['ci_lo']):.3f}--{float(r['ci_hi']):.3f}", f"{float(r['median']):.3f}", f"{float(r['gap_same_degree']):+.3f}"])
table('app_locality.tex', 'llrrrrr', 'Target & Model & Pairs & Mean & 95\\% CI & Median & Gap', rows,
      'Query-space cosine similarity by graph distance. Full scale: mean of two random-negative models at three epochs, with interval bounds and medians averaged over the two. Mini: the same model untrained, after 50 updates, and after 10 epochs. Gap: minus random users of the same degree.', 'tab:app-locality', star=True)
md = (L / 'full-scale-replicates/analysis-overhead/READ.md').read_text().split('## Three-seed mean')[1].split('\n## ')[0]
# three-seed cost accounting (seeds 1504-1506), same table as the seed-1506 READ
rows = [[re.sub(r'\*\*', '', c.strip()).replace('%', '\\%').replace('−', '$-$') for c in line.strip('|').split('|')] for line in md.splitlines() if line.startswith('| ') and not line.startswith('| |')]
table('app_cost.tex', 'lrrrr', ' & Random & Fresh uncapped & Cached uncapped & Cached capped', rows,
      'Full-scale training cost over the same 15{,}479 updates, mean over three seeds (16 A100 GPUs, rank-0 wall clock in seconds unless stated). Checkpoint I/O and evaluation excluded from the totals; bootstrap inference charged to the cached arms.', 'tab:app-cost', star=True)
print('tables written:', sorted(p.name for p in OUT.glob('*.tex')))
