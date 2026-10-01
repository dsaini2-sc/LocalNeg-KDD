# LocalNeg-KDD (working name)

Industry paper on negative mining for embedding-based retrieval on a billion-node social graph:
clustered-anchor batching, cached mining, per-cluster row capping, exposure negatives.

- `main.tex` — ACM `sigconf` review format; `macros.tex` — shared macros (`\todo`, `\evidence`).
- `sections/NN_*.tex` — one file per section, numbered in reading order.
- `notes/STORY.md` — thesis, section map, claims-to-evidence table, open risks. Every number in
  the prose must trace to a file listed there.
- `figures/`, `tables/`, `references/references.bib` (every entry checked against its publisher record, 2026-09-30).
- `scripts/make_tables.py` writes every `tables/*.tex` from the lab records; `scripts/locality_figure.py` writes `figures/locality.pdf`. `figures/locality-control.pdf` is a copy of `v9/lab13-internal-evidence/embedding-locality-r1/mini-control/locality-control.pdf`.
- Taking over the writing: read `notes/HANDOFF-2026-10-01.md` first.

Build: `make` (latexmk + pdflatex). Build outputs are git-ignored.
