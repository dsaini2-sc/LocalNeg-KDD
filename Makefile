# Build the paper: make (pdf), make clean
main.pdf: main.tex macros.tex sections/*.tex tables/*.tex figures/*.pdf figures/*.tex references/references.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
clean:
	latexmk -C main.tex
.PHONY: clean
