
.PHONY: clean cleanall all

all: main.pdf

main.pdf: main.tex
	pdflatex main.tex
	makeglossaries main
	texi2pdf --tidy main.tex

clean:

	rm -f main.pdf *~ *.aux main.log main.run.* main.toc		\
	      main-blx.bib main.bbl main.blg main.bcf main.out		\
	      main.tdo main.ist main.not main.alg main.ntn main.acn	\
	      main.xdy main.abr main.acr main.brv main.glg main.glo	\
	      main.gls main.loe main.lof main.lol main.lot

cleanall: clean
	rm -rf main.t2d
