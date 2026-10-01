"""figures/locality.pdf from the lab records: full-scale locality and the exposure probe, mean of the two random-negative models."""
import csv, json, statistics as st
from pathlib import Path
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
rows = list(csv.DictReader(open('/home/dsaini2/data/Research/BAGLRQs/v9/lab13-internal-evidence/embedding-locality-r1/metrics.csv')))
probe = json.load(open('/home/dsaini2/data/Research/BAGLRQs/v9/lab13-internal-evidence/embedding-locality-r1/exposure-probe/metrics.json'))
avg = lambda c, k: st.mean(float(r[k]) for r in rows if r['class'] == c)
C = ['hop1', 'hop2', 'hop3', 'random']; m = [avg(c, 'mean') for c in C]
err = [[x - avg(c, 'ci_lo') for x, c in zip(m, C)], [avg(c, 'ci_hi') - x for x, c in zip(m, C)]]
fig, ax = plt.subplots(figsize=(4.2, 3.0))
ax.bar(range(4), m, 0.6, yerr=err, label='random-trained')
ax.axhline(avg('positive', 'mean'), ls='--', c='k', lw=1, label='future friends (positives)')
ax.axhline(st.mean(probe[s]['mean'] for s in ('s1506', 's1505')), ls=':', c='k', lw=1.3, label='stored exposure negatives')
ax.set_xticks(range(4)); ax.set_xticklabels(['1 hop', '2 hops', '3 hops', 'random'])
ax.set_ylabel('cosine similarity (query space)'); ax.legend(fontsize=7, frameon=False); fig.tight_layout()
fig.savefig(Path(__file__).resolve().parents[1] / 'figures/locality.pdf')
print('bars', [round(x, 3) for x in m], 'positives', round(avg('positive', 'mean'), 3))
