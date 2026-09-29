# Build the paper: make (pdf), make clean
main.pdf: main.tex macros.tex sections/*.tex references/references.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
clean:
	latexmk -C main.tex
.PHONY: clean
