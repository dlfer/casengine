CE=../casengine.py

default:
	@echo read the makefile first

makesty:
	$(CE) --sty

e_sympy e_sage e_maple e_mathematica e_gap e_maxima: makesty
	$(CE) -v $@.tex 
	pdflatex $@_symout.tex

all-test: e_sympy e_sage e_maple e_mathematica e_gap e_maxima


clean:
	rm e_*.pdf
	rm e_*.log
	rm e_*.aux
	rm e_*_symout.tex
