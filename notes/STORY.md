# Story, organization and evidence map (working notes)

Started 2026-09-28 evening PT. Lab records live under
`/home/dsaini2/data/Research/BAGLRQs/v9/`, abbreviated `V/` below. Every number in the
paper must trace to a file listed here. Prose goes in `sections/`, and these notes stay
the single place where claims meet evidence.

## Thesis, one sentence

On a billion-node social graph, a model trained with random negatives already places graph
neighbours close together in embedding space. Clustering anchors by those embeddings turns
that locality into harder in-batch negatives and cheaper training steps, while the
conventional industry source of hard negatives, exposures, hurts. The same concentration
that makes clustered batches useful can make the model forget other regions on skewed
graphs, and a per-cluster row cap prevents that. Where concentration is low, the cap costs
nothing.

## Arc (user's sketch, 2026-09-28) mapped to sections

| # | Beat | Section file | Evidence status |
|---|---|---|---|
| 1 | Setting: billion-node graph, two-tower GNN retrieval, contrastive training | `03_setting.tex` | ready |
| 2 | Observation: random-trained embeddings are graph-local; clustering by embedding gives batch locality and cheaper steps | `04_locality.tex` | ready: direct measurement at full scale, 2 seeds (`V/lab13-internal-evidence/embedding-locality-r1/READ.md`); learned-vs-architectural control done 2026-09-29: learned within 50 updates (untrained 1-hop gap +0.06 vs +0.66) |
| 3 | Observation: exposure negatives, the conventional industry source, hurt; why | `05_exposure.tex` | effect ready (one pair); the *why* is pending the random-substitute control, see risk 2 |
| 4 | Idea: cluster anchors by embedding to mine negatives; cached asynchronously it is almost free | `06_clustered_mining.tex` | quality: 2 seeds at 2 epochs + 1 seed at 3 epochs, third seed running; cost ready |
| 5 | Concentration cuts both ways: regional forgetting | `07_concentration_capping.tex` | ready on public graphs; absent internally by construction |
| 6 | Intervention: per-cluster row cap | `07_concentration_capping.tex` | ready (public); internal null explained by the concentration diagnostic |
| 7 | Public benchmarks, capped vs uncapped, mechanism | `08_public.tex` | ready, with the metric caveats in risks 4 and 5 |

Organization choice: narrative order (observation, idea, risk, fix, generality) rather than
the classic Method / Experiments split. The internal results sit with the method, because the
internal graph is where mining gains accuracy. The public graphs are where the risk and the fix
show up. Alternative if reviewers want the classic shape: fold sections 4-5 into
"Observations", 6-7 into "Method", 8 plus the internal numbers into "Experiments".

## Claims and evidence

| Claim | Headline number(s) | Evidence file | Status |
|---|---|---|---|
| Graph scale | ~966M nodes (id map 965,969,407 rows, d0826); 104M positive-label sources; 211M distinct positive pairs | `V/lab13-internal-evidence/exposure-ablation/HANDOFF-EXPOSURE-NEGATIVES-2026-09-27.md`, `V/lab13-internal-evidence/README.md` | ready; clean edge count for d0826 still needed |
| Evaluation panel | 38,960,484 queries; 156,768,105 positives; 85,318,537 candidates; Sep 11-13 labels; macro recall primary | `V/lab13-internal-evidence/evaluation/all-results/READ.md`, `.../evaluation/METRIC-DECISION.md` | ready |
| Clustering by embedding co-locates graph regions | hop-1 nodes shared by >=2 roots 2.2% -> 4.7%; positives within one hop of another batch anchor 0.9% -> 2.6% | `V/lab13-internal-evidence/small-graph/batch-locality-r1/analysis/READ.md` | ready (mini) |
| Clustered batches are cheaper | sampled nodes per batch -35.1% median; per step nodes -22.7%, sequences -16.3%; full scale 917,794 vs ~700k nodes, 4.40 s vs 3.60 s median step | same + `V/lab13-internal-evidence/full-scale-cached-mining/analysis-overhead/READ.md` | ready |
| Exposure negatives hurt | add-back on d0826: macro R@1000 34.0862 -> 33.7399 (-0.3464 pp, -1.02% rel), every metric down; removal on d0731: +1.07%; harm concentrated on queries that own an exposure label (-0.72 pp vs +0.04 pp) | `V/lab13-internal-evidence/exposure-ablation/HANDOFF-EXPOSURE-NEGATIVES-2026-09-27.md` | effect: one pair, not compute-matched; why: pending |
| Clustered mining beats random, full scale (prose gate PASSED 23:20 PT Sep 28: seed 1504 at 2 epochs follows seed 1506 within 0.08 pp on every arm; gains +1.61..+1.74 pp) | 3 epochs, seed 1506: random 34.78 vs 36.38-36.53; 2 epochs, 2 seeds: random 34.08 vs 35.74-35.90 | `V/lab13-internal-evidence/full-scale-cached-mining/checkpoint-evaluation-r2/analysis-final/READ.md`, `V/lab13-internal-evidence/full-scale-replicates/evaluation/analysis/READ.md` | seed 1504 random at 2 epochs lands ~11:15 PM PT Sep 28; seed 1505 Sep 29 |
| Cached mining keeps the gain | cached within ~0.1 pp of fresh at every point | same | ready |
| Almost free | cached clustered training -7% GPU time vs random incl. one-time bootstrap, -15% excl.; fresh mining +13% | `V/lab13-internal-evidence/full-scale-cached-mining/analysis-overhead/READ.md`, `.../PAPER-NOTE.md` | ready |
| Uncapped clustered mining collapses on skewed graphs | three seeds, R@1000 gap vs random at mining end: Collab -9.4 (fresh) / -8.0 (cached), Citation2 -34.4 / -23.0, LJ -10.7 / -14.1 pp; capped -0.1 / -0.1, -0.5 / -0.5, +0.3 / +0.2; full-corpus MRR (x100) capped +0.23/-0.07, +0.18/+0.16, +0.51/+0.53; official: Collab Hits@50 capped +1.1/+1.2, Citation2 sampled MRR -0.48/-0.39, LJ sampled MRR +0.1 | `V/lab14-shared-cached-mining/replicates-s2s3/READ.md` | ready, three seeds (2026-09-29) |
| Collapse = few clusters per batch | last 100 updates, mean clusters per batch: Collab 20.4 (min 1) uncapped vs 83.4 (min 79) capped; LJ 25.1 (min 2) vs 67.1 (min 35) | `V/lab14-shared-cached-mining/reports/COLLAB-READ.md`, `.../LJ-READ.md` | ready |
| Regional forgetting | all 48 imbalanced depletion settings worsen other-region loss and R@10; 46 also improve own-region loss; acute, largely recoverable | `V/lab5-batch-causality/p14-p16-coordination/SCIENTIFIC-READ.md` | ready |
| Capping cuts query-level harm | harm incidence 14.64% -> 2.51% / 10.81% -> 2.54% / 8.77% -> 1.85% | `V/lab12-query-tracking/README.md`, `RESULTS.md` | ready |
| Capping gains on public metrics | two seeds: Collab Hits@50 +2.69%, Citation2 R@10 +2.10%, LJ R@10 +4.25% (rel.); three seeds P15: Collab Hits@50 +1.314 pp | `V/lab5-batch-causality/PAPER-POSITION-2026-09-19.md`, `V/lab1-hardneg-www2027/runs/m22_scheduler_from_start.md`, `V/lab5-batch-causality/p15-adaptive-mining/analysis/INTERPRETATION.md` | ready, but see risk 4 |
| Internal graph lacks the regime | data-prep cap 4 keeps 34.7% of rows; raw p99 82, max 3,380 positives per source; largest single-cluster share of a batch 11.4%; capped - uncapped -0.29..+0.21 pp at full scale | `V/lab13-internal-evidence/capping-regime/READ.md`, `V/lab13-internal-evidence/queue-audit/READ.md` | ready |

## Risks and open decisions

1. **Locality: measured directly (2026-09-28 evening).** Cosine in the query space 0.704 / 0.623 /
   0.446 at exactly 1 / 2 / 3 hops vs 0.072 for random users; future friends 0.605; two seeds agree
   to 0.001; degree-matched gaps +0.63 / +0.55 / +0.37 (`V/lab13-internal-evidence/embedding-locality-r1/READ.md`,
   figure copied to `figures/locality.pdf`). Remaining gap: whether the locality is learned or comes
   from the encoder aggregating overlapping neighbourhoods. An untrained-model control through the
   same inference separates the two; it needs one evaluator-sized inference job.
2. **The "why" of exposure harm is not established.** There are three open hypotheses:
   delayed or censored positives, candidates broadcast to every query in the batch, and extra
   negative pressure coupled with frequency correction. The random-substitute control is
   training on Prism: 7 runs at steps 5,650-8,150 of 12,725 as of 7:57 PM PT Sep 28. The
   add-back result is one pair and not compute-matched. The introduction should promise only
   what the control delivers.
3. **Forgetting and capping evidence is public-only.** The internal graph is low-concentration
   by construction because data prep caps positives at 4 per source. Carry this with the
   concentration-statistic table: public graphs high concentration with a capping benefit,
   internal low concentration with no effect.
4. **Citation2's official metric moves the wrong way.** Under P15, capping raises full-corpus
   R@10 and MRR in all 3 seeds but lowers the official sampled MRR (-0.454 on the x100 scale,
   all 3 seeds). The metric policy says each public dataset reports its established metric,
   and for Citation2 that is sampled MRR. Decision needed: report both with the
   candidate-universe explanation, or tell the Citation2 story through the collapse-prevention
   comparison (lab14), where capped stays within 0.5 pp of random while uncapped loses 34 pp.
5. **On public graphs capping prevents collapse more than it beats random.** In lab14, capped
   is about random (within +/-0.5 pp R@1000), and a durable advantage over random is not
   established (`V/lab11-long-random-tail/README.md`). So the public claim is safety plus
   modest head-metric gains, and the accuracy gain over random is an internal-graph claim.
   These two fit together, but the introduction must not blur them.
6. **No online A/B result exists.** An applied-track reviewer will ask. Decide whether the
   paper says so or targets a deployment.

## Decisions, 2026-09-28 evening (user)

- **Exposure "why": assume it pans out.** The random-substitute control and the mechanism work run
  in a separate session. Write the exposure section as if the control separates the hypotheses;
  replace the placeholders when that session reports.
- **Online A/B: use it.** GTv17 A/B, segment "GTv17 A/B" (ID 225237), 2026-09-17 to 2026-09-26,
  control "GT random negative sc..." (Exp 2) vs. GTv17 (Exp 3, 50%). Numbers to refine later:

  | Metric | Change | Note |
  |---|---:|---|
  | New friends made with bidirectional communication | +2.09% +/- 0.29% | 0.205 -> 0.209, q < 0.001 |
  | New friends made | +1.01% +/- 0.23% | 0.799 -> 0.807, p < 0.001 |
  | Active days with new friends made with bidirectional communication | +1.23% +/- 0.12% | q < 0.001 |
  | New friends made with bidirectional Snap | +0.97% +/- 0.41% | q < 0.001 |
  | Active days with new friends made | +0.51% +/- 0.07% | q < 0.001 |
  | Friend adds seen by recipient | ~+0.5% | 5.737 -> 5.768; +3.836M rollout impact |
  | Active days with friend adds sent | +0.23% +/- 0.05% | q < 0.001 |
  | Significant friending metrics | 41 positive, 17 negative | |

  **Presentation (user decision, 2026-09-28 ~21:00 PT):** present the A/B as the user shared it: NGAME
  hard-negative mining trained without exposure negatives, against the production model trained with random and
  exposure negatives. Do not bring in the PPR-token or batch-size items from the console description. Section 6.5
  and intro P4 carry it. The trainer's clustered batching uses the same NGAME batch ordering
  (`positive_row_allocator.ngame_batch_order`), so the A/B and the offline method are the same family.
- **Citation2 metric: present both.** Headline the full-corpus number (the positive ranked against
  all 2.9M candidates, the harder and more principled measurement) and report the official OGB
  sampled MRR next to it, with one sentence on why they differ. Recommendation: apply the same rule
  to all three public datasets (headline the dataset's own metric computed against the full
  corpus, official sampled protocol in the next column), so the choice cannot look picked per
  dataset. For Collab and LiveJournal, check which full-corpus versions exist in the saved results.
- **Locality observation: measure it directly** (study `V/lab13-internal-evidence/embedding-locality-r1/`).

## Decisions, 2026-09-28 ~22:15 PT (user)

- **Shipped model = async cached capped.** The production NGAME model in the A/B is the cached,
  asynchronous, capped variant, so "capping is neutral on this graph and we run it enabled" is true.
- **The A/B is its own contribution bullet.**
- **NGAME in the introduction or only in related work: decide later.** Open.
- **Public replicates:** two more seeds of the five arms (random, fresh/cached x uncapped/capped) on
  Collab, Citation2 and LiveJournal, then check the new seeds against the recorded single-seed numbers.
  The capping paragraphs will draw on this one consistent set of runs. Launched 22:17-22:33 PT Sep 28:
  `V/lab14-shared-cached-mining/replicates-s2s3/` (30 cells, one A100 each; read in `READ.md` there).

## Open items (2026-09-29)

- Online A/B details (traffic share, user count, retrieval stage, declining metrics, final numbers): owned by the
  user, marked `\abtodo` (orange) in the source.
- Waiting on runs: three-seed exposure table (seeds 1502-1503), three-seed full-scale table (seed 1505), cost
  accounting for seeds 1504-1505.
- Decisions: title; NGAME named in the introduction or only in related work.

## Excluded from the manuscript (user decisions)

- Source-batched NGAME runs, including the M0 result and the M11 internal arm built on the M0
  checkpoint (2026-09-25).
- The uncapped mini dataset, `V/lab13-internal-evidence/small-graph/uncapped-five-arm-r1/`,
  which was artificial and uses a setting not used internally (2026-09-28).
- PPA; Amazon-book / MF / LightGCN; LF-AmazonTitles; MIND (withdrawn); micro recall except as
  a diagnostic.

## Title candidates

- Your Embeddings Already Know the Graph: Locality-Aware Negative Mining at Billion-Node Scale
- Cluster, Cap, Mine: Cheap Hard Negatives for Billion-Node Graph Retrieval
- Negatives from the Neighbourhood: Clustered Batching for Industrial Graph Retrieval

Earlier titles, for reference: "Balancing Nodes Is Not Enough: Example Exposure in Graph
Negative Mining" (`V/lab5-batch-causality/PAPER-CHECKPOINT-2026-09-21.md`); "Negative Mining
for Graphs: Example Exposure, Interference, and Recovery"
(`V/lab10-results-export/reviews/story-20260921/CURRENT-STORY.md`).
