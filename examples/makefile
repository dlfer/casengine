CE=../casengine.py

default:
	@echo read the makefile first

makesty:
	$(CE) --sty

e_sympy e_sage e_maple e_mathematica e_gap e_maxima e_sage-nonva: makesty
	$(CE) -v $@.tex 
	pdflatex $@_symout.tex

all-test: e_sympy e_sage e_maple e_mathematica e_gap e_maxima


clean:
	rm -f e_*.pdf
	rm -f e_*.log
	rm -f e_*.aux
	rm -f e_*_symout.tex
