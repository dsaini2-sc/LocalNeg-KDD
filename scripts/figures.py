"""figures/exposure_proximity.pdf and figures/public.pdf from the lab records (three-seed means)."""
import csv, json, statistics as st
from pathlib import Path
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
V = Path('/home/dsaini2/data/Research/BAGLRQs/v9'); OUT = Path(__file__).resolve().parents[1] / 'figures'
plt.rcParams.update({'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False})

# Exposure: the owner-cell loss and the shuffled repair, by mutual friends with the future friend (recall@1000).
d = json.load(open(V / 'lab13-internal-evidence/exposure-ablation/why/proximity-ranks.json'))
bins = d['bins']; x = range(len(bins))
fig, ax = plt.subplots(figsize=(3.4, 2.3))
for key, lbl, off, c in [('own-none@1000', 'harm: own source only $-$ never a negative', -0.18, 'tab:red'),
                         ('perm-exp@1000', 'repair: shuffled $-$ added back', 0.18, 'tab:blue')]:
    cells = d['paired_differences_pp'][key]; assert [r['bin'] for r in cells] == bins
    ax.bar([i + off for i in x], [r['mean'] for r in cells], 0.36, yerr=[r['half_ci'] for r in cells], color=c, label=lbl, capsize=1.5, error_kw={'lw': 0.7})
ax.axhline(0, c='k', lw=0.6); ax.set_xticks(list(x)); ax.set_xticklabels(bins)
ax.set_xlabel('mutual friends between user and future friend'); ax.set_ylabel('$\\Delta$ hit rate@1000 (points)')
fig.legend(*ax.get_legend_handles_labels(), fontsize=6.5, frameon=False, loc='upper center', ncol=2); fig.tight_layout(rect=(0, 0, 1, 0.9)); fig.savefig(OUT / 'exposure_proximity.pdf')
print('exposure', {k: [round(r['mean'], 2) for r in d['paired_differences_pp'][k]] for k in ('own-none@1000', 'perm-exp@1000')})

# Public: each benchmark's metric for random, uncapped and capped clustered batching (cached signal), mining endpoint.
pub = list(csv.DictReader(open(V / 'lab14-shared-cached-mining/replicates-s2s3/table.csv')))
DS = [('collab', 'Collab', 'official', 'Hits@50'), ('c2', 'Citation2', 'mrr', 'MRR $\\times$100'), ('lj', 'LiveJournal', 'mrr', 'MRR $\\times$100')]
ARMS = [('random', 'Random', '0.6'), ('async_uncapped', 'Uncapped', 'tab:red'), ('async_capped', 'LocalNeg', 'tab:blue')]
fig, axes = plt.subplots(1, 3, figsize=(3.4, 1.9))
for ax, (ds, name, col, metric) in zip(axes, DS):
    for i, (pol, lbl, c) in enumerate(ARMS):
        v = [float(r[col]) for r in pub if r['dataset'] == ds and r['policy'] == pol and r['endpoint'] == 'mining']; assert len(v) == 3, (ds, pol)
        ax.bar(i, st.mean(v), 0.7, yerr=st.stdev(v), color=c, label=lbl, capsize=1.5, error_kw={'lw': 0.7})
        print('public', ds, pol, round(st.mean(v), 2))
    ax.set_title(f'{name}\n{metric}', fontsize=7); ax.set_xticks([]); ax.tick_params(labelsize=7)
fig.legend(*axes[0].get_legend_handles_labels(), fontsize=6.5, frameon=False, loc='upper center', ncol=3)
fig.tight_layout(rect=(0, 0, 1, 0.88)); fig.savefig(OUT / 'public.pdf')
