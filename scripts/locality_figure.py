"""figures/locality.pdf from the lab records: (a) full-scale locality and the exposure probe, mean of the two random-negative
models; (b) the mini-graph control, degree-matched gap at three training stages."""
import csv, json, statistics as st
from pathlib import Path
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False})
rows = list(csv.DictReader(open('/home/dsaini2/data/Research/BAGLRQs/v9/lab13-internal-evidence/embedding-locality-r1/metrics.csv')))
probe = json.load(open('/home/dsaini2/data/Research/BAGLRQs/v9/lab13-internal-evidence/embedding-locality-r1/exposure-probe/metrics.json'))
avg = lambda c, k: st.mean(float(r[k]) for r in rows if r['class'] == c)
C = ['hop1', 'hop2', 'hop3', 'random']; m = [avg(c, 'mean') for c in C]
err = [[x - avg(c, 'ci_lo') for x, c in zip(m, C)], [avg(c, 'ci_hi') - x for x, c in zip(m, C)]]
fig, (ax, bx) = plt.subplots(2, 1, figsize=(3.4, 3.7))
ax.bar(range(4), m, 0.6, yerr=err)
ax.axhline(avg('positive', 'mean'), ls='--', c='k', lw=1, label='future friends (positives)')
ax.axhline(st.mean(probe[s]['mean'] for s in ('s1506', 's1505')), ls=':', c='k', lw=1.3, label='stored exposure negatives')
ax.set_xticks(range(4)); ax.set_xticklabels(['1 hop', '2 hops', '3 hops', 'random'])
ax.set_ylabel('cosine similarity'); ax.set_title('(a) Full scale, after 3 epochs', fontsize=8, loc='left'); ax.legend(fontsize=6.5, frameon=False, loc='upper right'); ax.set_ylim(0, 0.98)
ctrl = list(csv.DictReader(open('/home/dsaini2/data/Research/BAGLRQs/v9/lab13-internal-evidence/embedding-locality-r1/mini-control/metrics.csv')))
for i, stage in enumerate(['untrained', '50 updates', '10 epochs']):
    g = [float(next(r['gap_same_degree'] for r in ctrl if r['model'] == stage and r['class'] == c)) for c in C[:3]]
    bx.bar([j + (i - 1) * 0.27 for j in range(3)], g, 0.27, label=stage); print(stage, [round(x, 3) for x in g])
bx.set_xticks(range(3)); bx.set_xticklabels(['1 hop', '2 hops', '3 hops']); bx.set_ylabel('gap over random users\nof the same degree')
bx.set_title('(b) Sampled graph, one model during training', fontsize=8, loc='left'); bx.legend(fontsize=6.5, frameon=False, ncol=3, loc='upper right')
bx.set_ylim(0, 0.9); fig.tight_layout()
fig.savefig(Path(__file__).resolve().parents[1] / 'figures/locality.pdf')
print('bars', [round(x, 3) for x in m], 'positives', round(avg('positive', 'mean'), 3))
