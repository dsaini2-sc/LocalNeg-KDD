# LocalNeg-KDD (working name)

Industry paper on negative mining for embedding-based retrieval on a billion-node social graph:
clustered-anchor batching, cached mining, per-cluster row capping, exposure negatives.

- `main.tex` — ACM `sigconf` review format; `macros.tex` — shared macros (`\todo`, `\evidence`).
- `sections/NN_*.tex` — one file per section, numbered in reading order.
- `notes/STORY.md` — thesis, section map, claims-to-evidence table, open risks. Every number in
  the prose must trace to a file listed there.
- `figures/`, `tables/`, `references/references.bib` (entries marked VERIFY need checking).

Build: `make` (latexmk + pdflatex). Build outputs are git-ignored.
