# CASengine


**What for?** To generate parametrized exercises/texts in [LaTeX](https://en.wikipedia.org/wiki/LaTeX), from a compact source,
 while at the same time executing commands in **Computer Algebra Systems** in a localized namespace 
(such as 
[sympy](https://en.wikipedia.org/wiki/SymPy), 
[SageMath](https://en.wikipedia.org/wiki/SageMath), [maple](https://en.wikipedia.org/wiki/Maple_(software)), 
[mathematica](https://en.wikipedia.org/wiki/Mathematica), 
[maxima](https://en.wikipedia.org/wiki/Maxima_(software)),
[gap](https://en.wikipedia.org/wiki/GAP_(computer_algebra_system)), 
...). Adding one CAS interface should be relatively easy. 
 	 
```
OPTIONS:
        --help|-h       Help
        --verbose|-v    Verbose Running
        --output=|-o [FILENAME] explicit output filename
        --sty           Generate the file `casengine.sty` in the current dir.
        --noexec|-n     Do not execute any sympy code.
```


I do not have time yet to write extensive documentation. Somehow the source is self-explaining?  

Just to do, first generate the .sty LaTeX file:
```
$ casengine.py --sty
```

Then, write a (La)TeX file with the following commands (simple example):

```latex 
\documentclass{article}
\usepackage{casengine} % with no CAS, it will be assumed sympy
%%% \usepackage[CAS=maple]{casengine} % sage, maple, math, gap, whatever (see DEFAULT_OPTIONS in src)
\usepackage{enumerate}

\begin{document}
\symexec{CLEAR} % not really necessary. Sometimes.
\symexec{x=Derivative(sqrt(1+x**2))} % syntax-dependent (here it is sympy)
\begin{symfor}{q}{1;Rational(1,2);pi+sqrt(5)}% a list of symbolic expressions, separated by ";"
\begin{symfor}{c}{range(1,3)}% a python range of integers

This is a sentence with $\sym{q} + \sym{x} + \sym{c} = \sym{q+x.doit()+c}$.
\end{symfor}
\end{symfor}
\end{document}
```

Executing `casengine.py` on the file yields an outut such as the following
(the `symfor` cycles are cycled through,  the `\symexec` commands executed and the `\sym` expressions are latexified and printed, as follows:
```latex
%File test_symout.tex created by casengine.py (CAS engine: SymPy Version 0.7.4.1)
%Started: 2017-10-10 16:08:37.270242
%Finished: 2017-10-10 16:08:37.499979
%Elapsed time: 0:00:00.229737
\documentclass{article}
\usepackage{casengine} % with no CAS, it will be assumed sympy
%%% \usepackage[CAS=maple]{casengine} % sage, maple, math, gap, whatever (see DEFAULT_OPTIONS in src)
\usepackage{enumerate}

\begin{document}
% ==> NameSpace CLEARED % not really necessary. Sometimes.
%cas_exec: x=Derivative(sqrt(1+x**2)) % syntax-dependent (here it is sympy)
%%sym_for q:
%cas_exec: q=1% a list of symbolic expressions, separated by ";"
%%sym_for c:
%cas_exec: c=1% a python range of integers

This is a sentence with $1 + \frac{d}{d x} \sqrt{x^{2} + 1} + 1 = \frac{x}{\sqrt{x^{2} + 1}} + 2$.
%%end sym_for c
%%sym_for c:
%cas_exec: c=2% a python range of integers

This is a sentence with $1 + \frac{d}{d x} \sqrt{x^{2} + 1} + 2 = \frac{x}{\sqrt{x^{2} + 1}} + 3$.
%%end sym_for c
%%end sym_for q
%%sym_for q:
%cas_exec: q=Rational(1,2)% a list of symbolic expressions, separated by ";"
%%sym_for c:
%cas_exec: c=1% a python range of integers

This is a sentence with $\frac{1}{2} + \frac{d}{d x} \sqrt{x^{2} + 1} + 1 = \frac{x}{\sqrt{x^{2} + 1}} + \frac{3}{2}$.
%%end sym_for c
%%sym_for c:
%cas_exec: c=2% a python range of integers

This is a sentence with $\frac{1}{2} + \frac{d}{d x} \sqrt{x^{2} + 1} + 2 = \frac{x}{\sqrt{x^{2} + 1}} + \frac{5}{2}$.
%%end sym_for c
%%end sym_for q
%%sym_for q:
%cas_exec: q=pi+sqrt(5)% a list of symbolic expressions, separated by ";"
%%sym_for c:
%cas_exec: c=1% a python range of integers

This is a sentence with $\sqrt{5} + \pi + \frac{d}{d x} \sqrt{x^{2} + 1} + 1 = \frac{x}{\sqrt{x^{2} + 1}} + 1 + \sqrt{5} + \pi$.
%%end sym_for c
%%sym_for c:
%cas_exec: c=2% a python range of integers

This is a sentence with $\sqrt{5} + \pi + \frac{d}{d x} \sqrt{x^{2} + 1} + 2 = \frac{x}{\sqrt{x^{2} + 1}} + 2 + \sqrt{5} + \pi$.
%%end sym_for c
%%end sym_for q
\end{document}
```

Further engines (easy to extend: maple, mathematica, sage, gap, ...): see the examples dir. 

A note on elapsed times:

```
sympy:       Elapsed time: 00:00:00.59
maxima:      Elapsed time: 00:00:12.20
maple:       Elapsed time: 00:00:15.07
mathematica: Elapsed time: 00:00:16.10
sage:        Elapsed time: 00:00:25.66
gap:         Elapsed time: 00:00:18.53
```

## Inspired by...

The idea was to have an analogue of [SageTeX](https://github.com/sagemath/sagetex),
[sympytex](https://ctan.org/pkg/sympytex) or [pythontex](https://ctan.org/pkg/pythontex)
but more with the idea of parametrized exercises generation than of a math notebook 
document. This means that it acts as a LaTeX-to-LaTeX filter, allowing freedom to choose the CAS,
instead of a LaTeX-to-CAS-language-to-PDF. 


