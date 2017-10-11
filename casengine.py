#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# LICENCE:  GNU AFFERO GENERAL PUBLIC LICENSE v.3 https://github.com/dlfer/casengine/blob/master/LICENSE
# https://github.com/dlfer/casengine
# (C) DLFerrario http://www.dlfer.xyz

r"""
# Version: 2017-10-10
casengine.py [options] [filename]

a Pre-Processor for (La)TeX files, that interact with Compuuter Algebra Systems: sympy, maple, ... 

RUN: casengine.py < example.tex > example_out.tex 
[or] casengine.py example.tex  
       ==> example_symout.tex generated 

OPTIONS:
        --help|-h       Help
        --verbose|-v    Verbose Running
        --output=|-o [FILENAME] explicit output filename
        --sty           Generate the file `casengine.sty` in the current dir.
        --noexec|-n     Do not execute any sympy code.

EXAMPLES:
        $ casengine.py --sty
        $ casengine.py -o example_out.tex example.tex 

LATEX:
%s
 =>
%s 

     https://github.com/dlfer/casengine
(C)  DLFerrario http://www.dlfer.xyz
""" 

import sys
import re
import os
import getopt
import datetime, time

#--------------------------------------------------------------------------
__sty__=r"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\fileversion{0.92}
\def\filedate{2017-06-12}
\def\Copyright{**********************************************
Quest'opera è stata rilasciata con licenza Creative Commons Attribuzione - Non commerciale - Non opere derivate 3.0 Unported. Per leggere una copia della licenza visita il sito web http://creativecommons.org/licenses/by-nc-nd/3.0/ o spedisci una lettera a Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.

Credits to https://tex.stackexchange.com/questions/127010/how-can-i-make-lstinline-function-normally-inside-math-mode

(C) DLFerrario http://www.dlfer.xyz
**********************************************
}
\NeedsTeXFormat{LaTeX2e}[1996/06/01]
\typeout{Package `CasEngine' <\filedate>.}
\typeout{\Copyright}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage{kvoptions}
\SetupKeyvalOptions{
family = CAS,
prefix = CAS@
}
\DeclareStringOption{CAS}
\DeclareStringOption{CASOptions}
\DeclareStringOption{CASPrompt}
\DeclareStringOption{CASLatex}
\DeclareStringOption{CASLatexOutsep}
\DeclareStringOption{CASAssignString}
\DeclareStringOption{CASPreamble}
\ProcessKeyvalOptions*
\typeout{%
CAS=\CAS@CAS,
CASOptions=\CAS@CASOptions,
CASPrompt=\CAS@CASPrompt,
CASLatex=\CAS@CASLatex,
CASLatexOutsep=\CAS@CASLatexOutsep,
CASAssignString=\CAS@CASAssignString,
CASPreamble=\CAS@CASPreamble
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{listings}
\lstset{language=Python,
basicstyle=\ttfamily,
mathescape=true
}

\usepackage{letltxmacro}
\newcommand*{\SavedLstInline}{}
\LetLtxMacro\SavedLstInline\lstinline
\DeclareRobustCommand*{\lstinline}{%
  \ifmmode
    \let\SavedBGroup\bgroup
    \def\bgroup{%
      \let\bgroup\SavedBGroup
      \hbox\bgroup
    }%
  \fi
  \SavedLstInline
}

\newenvironment{symfor}[2]{%

\noindent\lstinline|((for #1 in  [#2] ))|

}{%

\noindent\lstinline|((end for ))|

}

\newcommand{\sym}[1]{%
\lstinline|(( #1 ))|
}

\newcommand{\symexec}[1]{%
\lstinline|((symexec: #1 ))|
}
"""


#--------------------------------------------------------------------------
VERBOSE=False
NOEXEC=False

#--------------------------------------------------------------------------
example_tex=r"""
% the following command restart the NameSpace (it is the only non-python command)
\symexec{CLEAR}
\symexec{x=t**2-t-1
y=t**3-t**2+1}
\begin{symfor}{A}{x+1;x-2;y+4} % separator is ";", every symbolic expression in between
\begin{symfor}{t}{range(-1,2)} % same syntax as python (1,2 or 3 arguments)
$t=\sym{t}$ %its value
\end{symfor}
Now this is the first line
This is the second line:
$\sym{1+1}$ %its value
\symexec{B=A**3} % execute code
\[
\sym{factor(B+A**2)}
\]
Last line
\end{symfor}
"""

example_tex_maple=r"""
\documentclass[a4paper,twoside,leqno]{article}
\usepackage{amsmath,amsthm,amssymb,amsfonts}
\usepackage{mathpazo} % I like it.

\usepackage[CAS=maple]{casengine}

\newcounter{exer}
\numberwithin{exer}{subsection}
\renewcommand{\theexer}{(E\arabic{exer})}
\renewcommand{\thesubsection}{\Alph{subsection})}
\newtheoremstyle{exer}% name
     {24pt}%      Space above
     {24pt}%      Space below
     {}%         Body font: it was: \itshape
     {}%         Indent amount (empty = no indent, \parindent = para indent)
     {\bfseries}% Thm head font
     {}%        Punctuation after thm head
     {.5em}%     Space after thm head: " " = normal interword space;
               % \newline = linebreak
     {}%         Thm head spec (can be left empty, meaning `normal')

\theoremstyle{exer}
\newtheorem{exe}[exer]{}

\begin{document}

\section{Esercizi}
\begin{symfor}{q}{range(1,3)}%
\begin{symfor}{c}{range(1,3)}%
\begin{symfor}{x}{cos(t);sin(t);tan(t);exp(t);cosh(t);sinh(t);t**3-t**2+t-1}%

\symexec{g:=q*x+c;}
\begin{exe}
Try to compute 
\symexec{F:=Diff(expand(g),t);}
\[
\sym{F}
\]
Answer: $\sym{simplify(value(F))}$. 
\end{exe}
\end{symfor}

\end{symfor}
\end{symfor}
\end{document}
"""

#--------------------------------------------------------------------------

def my_strftime(td):
    secs=td.total_seconds()
    x=secs - td.seconds
    h, rem = divmod(secs,60*60)
    m,s    = divmod(rem,60)
    return "%02i:%02i:%02i%s" % (h,m,s,  ("%.02f" % (x))[1:] ) 
#--------------------------------------------------------------------------
class Logger():
  def write(self,s):
    dt=datetime.datetime.fromtimestamp(int(time.time()))
    global VERBOSE
    if VERBOSE: 
      sys.stderr.write("# %s #: %s" % (dt.isoformat(" "), s))
  def msg(self,s):
    sys.stderr.write("%s" % s)
  def times(self,start_time,end_time,filename, casengine=None):
    FMT="YYYY-MM-DD HH:MM:SS"
    start_datetime=datetime.datetime.fromtimestamp(int(start_time))
    end_datetime=datetime.datetime.fromtimestamp(int(end_time))
    elapsed_time=datetime.timedelta(seconds=end_time-start_time) 
    output="File %s created by casengine.py (CAS engine: %s)\nStarted: %s\nFinished: %s\nElapsed time: %s\n" % (filename,casengine, start_datetime.isoformat(" "), end_datetime.isoformat(" "), my_strftime(elapsed_time) )
    return output
LOG=Logger()

#--------------------------------------------------------------------------
class CasEngine(object):
 def __init__(self,name=None,start_time=time.time()):
  LOG.write("__init__ called!\n")
  self.reg_forcycleiter=re.compile( r"(\\begin{symfor}{(?P<var>.+?)}{(?P<symlist>.+?)})|(\\end{symfor})", re.M and re.DOTALL)
  # self.reg_forcycleiter=re.compile( r"(\n\\symfor{(?P<var>.+?)}{(?P<symlist>.+?)})|(\n\\symforend)", re.M and re.DOTALL)
  self.reg_symexec=re.compile(r"\\symexec{")
  self.reg_sym=re.compile(r"\\(sym|symexec){(?P<symdata>.+?)}", re.M and re.DOTALL)
  self.reg_range=re.compile(r" *range\((?P<rangearg>.+)\)" )
  self.name=name
  self.localNameSpace={}
  self.cas_engine=None
  self.cas_init()
  self.number_of_syms=None #initialized by filter 
  self.number_of_syms_iter=None
  self.start_time=start_time
 # To be defined according to wich CAS system... 
 def cas_latex(self):
  return "LATEX"
 def cas_init(self):
  LOG.write("nothing done!\n")
 def cas_exec(self,s):
  return None
 def cas_get(self,s):
  return None
 def cas_let(self,a,b):
  return None
 def cas_forlist(self,s):
  mo=self.reg_range.search(s)
  if mo:
   # sanitize the input of the eval... 
   return ["%s" % x for x in eval("range(%s)" % mo.group('rangearg') , {'__builtins__':None}, {'range': range } ) ]
  else:
   return s.split(';')
 def tex_comment(self,s):
  return "".join([("%%%s" % l) for l in s.splitlines(True)])
 #Now: common functions to parse LaTeX 
 def expand_forcycle(self,s):
  LOG.write("expand_forcycle called on a tex string of length: %s chars\n" % len(s))
  ff= self.reg_forcycleiter.search(s)
  if ff:
   all = [ff for ff in self.reg_forcycleiter.finditer(s)]
   lenall=len(all)
   for i in range(lenall-1): 
      if all[i].group('var') and not  all[i+1].group('var'):
        s_before=s[:all[i].start()]
        s_during=s[all[i].end():all[i+1].start()]
        s_after=s[all[i+1].end():]
        s_var=all[i].group('var')
        s_symlist=self.cas_forlist(all[i].group('symlist'))
        s_symlist_tokens=[ "%%%%sym_for %s:\n\symexec{%s}%s%%%%end sym_for %s" % (s_var,self.cas_let( s_var, x) ,s_during, s_var) for x in s_symlist ] 
        s_during_expanded = "\n".join(s_symlist_tokens)
        return self.expand_forcycle( ( s_before + s_during_expanded + s_after ) ) 
   raise Exception ("CasEngine ERROR: symfor does not end well!\n")
  else:
   return s
 def sym_filter(self,s):
   LOG.write("sym_filter called on a tex string of length: %s chars\n" % len(s))
   self.number_of_syms=len(self.reg_sym.findall(s))
   self.number_of_syms_iter=0
   LOG.write("There are %s sym's to be processed...\n" % self.number_of_syms)
   return self.reg_sym.sub(self.my_filter_func,s)
 def my_filter_func(self,ob):
  self.number_of_syms_iter += 1
  ETA=(time.time() - self.start_time) * (self.number_of_syms*1.0/self.number_of_syms_iter - 1 ) 
  ETAstr=my_strftime(datetime.timedelta(seconds=ETA))
  numlen=str(len(str(self.number_of_syms)))
  if VERBOSE:
      LOG.msg(("\rProgress: %"+numlen+"i/%i (%6.2f%%: ETA = %s)                 ") % (self.number_of_syms_iter, self.number_of_syms , self.number_of_syms_iter * 100.0 / self.number_of_syms ,ETAstr ))
  else:
      LOG.msg(".")
  if self.reg_symexec.match(ob.group()):
   if ob.group('symdata').strip() == 'CLEAR':
    LOG.write("Trying to clear namespace...\n")
    #preserve the number of syms...
    tmpsyms=self.number_of_syms
    tmpsyms_iter=self.number_of_syms_iter
    self.__init__(name=self.name,start_time=self.start_time)
    self.number_of_syms=tmpsyms
    self.number_of_syms_iter=tmpsyms_iter
    LOG.write(" ...done!\n")
    return self.tex_comment(" ==> NameSpace CLEARED")
   else:
    return self.cas_exec( ob.group('symdata') )
  else:
   return self.cas_get( ob.group('symdata') )

#--------------------------------------------------------------------------
class SympyEngine(CasEngine):
 def cas_init(self):
  exec(r"""
from sympy import __version__
from sympy.abc import *
from sympy import *
""" , self.localNameSpace)
  self.cas_engine="SymPy Version %s" % self.localNameSpace['__version__']
 def cas_exec(self,s):
  output='cas_exec: %s' % s
  try:
   exec(s, self.localNameSpace)
  except Exception, v:
   output += " => ERROR: %s\n" % v
   raise Exception("SymPy Error: %s while processing command `%s'" % (v,s) )
  return self.tex_comment(output)
 def cas_get(self,s):
  exec(r"""output_string=latex(sympify(%s))""" % s, self.localNameSpace)
  return self.localNameSpace['output_string']
 def cas_let(self,a,b):
  """Return the string to assign variable value b to a"""
  return "%s=%s" % (a,b) 

#--------------------------------------------------------------------------
class ExpectEngine(CasEngine):
 def cas_init(self,
              cas='maple',
              cas_options='-t -c "interface(screenwidth=infinity,errorcursor=false)"', 
              cas_prompt='#-->', 
              cas_latex='latex(%s);', 
              cas_latex_outsep='\n',
              cas_assign_string='%s:= %s;',
              cas_preamble=None):
  import pexpect
  self.EOF=pexpect.EOF
  self.cas_name=cas
  self.cas_engine="pExpect -> %s " % cas
  self.cas_prompt=cas_prompt
  self.cas_latex=cas_latex
  self.cas_latex_outsep=cas_latex_outsep
  self.cas_assign_string=cas_assign_string
  cas_torun=(cas +" " + cas_options)
  self.child = pexpect.spawn(cas_torun , timeout=60, ignore_sighup=False )
  self.child.expect(self.cas_prompt)
  if cas_preamble:
   for x in cas_preamble.split("\n"):
    self.child.sendline(x)
    self.child.expect(self.cas_prompt)
  return
 def cas_exec(self,s):
  output='cas_exec: %s' % ( s,  ) 
  self.child.sendline(s)
  self.child.expect(self.cas_prompt)
  out_null=self.child.before
  return self.tex_comment(output)
 def cas_get(self,s):
  self.child.sendline(self.cas_latex % s)
  self.child.expect(self.cas_prompt)
  out=self.child.before
  # out = out[out.find(';')+1:].strip() ## __TODO__ change also this...
  # out = out[out.find('\n')+1:].strip() ## __TODO__ change also this...
  out = out[out.find(self.cas_latex_outsep)+len(self.cas_latex_outsep):].strip() 
  LOG.write("Found cas_get `%s`" % out)
  return out
 def cas_let(self,a,b):
  # TODO: switch cases...
  return self.cas_assign_string % (a,b)
 def __del__(self):
  LOG.write("Trying to clean up spawn processes...\n")
  # self.child.sendline("quit()")
  # self.child.expect(self.cas_prompt) #__TODO__ cmaple all the time running... 
  self.child.sendeof()
  # self.child.expect(self.EOF)
  self.child.close()
  self.child.terminate()

#--------------------------------------------------------------------------
DEFAULT_OPTIONS={
        'maple': {'CASOptions': '-t -c "interface(screenwidth=infinity,errorcursor=false)"' , 'CASPrompt': '#-->'  , 'CASLatex': 'latex(%s);' , 'CASLatexOutsep':'\n', 'CASAssignString': '%s:= %s;' , 'CASPreamble' : '' },
        'sage' : {'CASOptions': '-q', 'CASPrompt': 'sage: ', 'CASLatex': 'latex(%s)', 'CASLatexOutsep':'\n', 'CASAssignString' : '%s= %s' , 'CASPreamble': "%colors NoColor"},
        'math' : {'CASOptions': '-rawterm', 'CASPrompt': 'In[[0-9]+]:=', 'CASLatex': 'TeXForm [%s]', 'CASLatexOutsep':'TeXForm=', 'CASAssignString' : '%s= %s' , 'CASPreamble': ""},
        'gap' : {'CASOptions': '-b -T ', 'CASPrompt': 'gap>', 'CASLatex': 'Print(%s);', 'CASLatexOutsep':';', 'CASAssignString' : '%s:= %s;' , 'CASPreamble': ""}
}
# GAP LaTeXObj not working yet...

#--------------------------------------------------------------------------
def latex_unescape(s):
  tmps=re.sub(r"\\%","%",s)
  return tmps

#--------------------------------------------------------------------------
def  get_cas_options(s):
  global DEFAULT_OPTIONS
  options={}
  reg_cas_options=re.compile(r"^\\usepackage\[(?P<CasOptions>.+?)\]{casengine}", re.M)
  mo=reg_cas_options.search(s)
  if mo:
    LOG.write("cas_options found: %s\n" % mo.group('CasOptions') )
    for token in mo.group('CasOptions').split(","):
      k,v=token.partition("=")[::2]
      options[k.strip()]=latex_unescape(v.strip())
  else:
    LOG.write("No cas_options found\n" )
    return options
  if 'CAS' in options and options['CAS'] in DEFAULT_OPTIONS:
    result=DEFAULT_OPTIONS[options['CAS']]
    for k in options:
     result[k]=options[k]
  else:
    LOG.msg("WARNING: option %s has no default! Errors ahead...\n" % options['CAS'])
    result=options
  LOG.write(options)  
  return result

#--------------------------------------------------------------------------
def get_opt():
  global VERBOSE, NOEXEC
  explicit_output=False
  try:
    opts,args = getopt.getopt(sys.argv[1:],"hvno:",["help","output=","sty","verbose","noexec"])
  except getopt.GetoptError,err:
    sys.stderr.write("GetOpt Error: %s\n[option --help for help]\n" % err)
    sys.exit(2)
  for o,a in opts:
      if o in ("-v", "--verbose"):
          VERBOSE = True
      elif o in ("-n", "--noexec"):
          NOEXEC = True
      elif o in ("-h", "--help"):
          sys.stdout.write(__doc__ % (example_tex, example_test() ) )
          sys.exit()
      elif o in ("--sty",):
          fd=file('casengine.sty','wa')
          fd.write(__sty__)
          fd.close()
          LOG.msg("File %s created!\n" % fd.name)
          sys.exit()
      elif o in ("-o","--output"):
          explicit_output=True
          fd_output=file(a,'w')
      else:
          assert False, "unhandled option" 
  if len(args)==0:
    input_data=sys.stdin.read()
    if not explicit_output:
     fd_output=sys.stdout
  else:  
    input_data=file(args[0]).read()
    if not explicit_output:
     b,e=os.path.splitext(args[0])
     fd_output=file("%s_symout%s" % (b,e),'w')
  return input_data, fd_output       

#--------------------------------------------------------------------------

def example_test():
 SE=SympyEngine()
 # SE=ExpectEngine()
 # s= SE.expand_forcycle(example_tex_maple)
 s= SE.expand_forcycle(example_tex)
 LOG.msg("GET_CAS_DATA: %s\n"% get_cas_options(example_tex_maple))
 return(SE.sym_filter(s))

#--------------------------------------------------------------------------
def old_main():
 SE=SympyEngine()
 s=sys.stdin.read()
 LOG.write("expand for cycles...")
 s=SE.expand_forcycle(s)
 LOG.write("done!\n")
 sys.stdout.write(SE.sym_filter(s))
 LOG.write("Finished!\n")
#--------------------------------------------------------------------------
def main():
    global VERBOSE, NOEXEC
    start_time=time.time()
    input_data,fd_output = get_opt()
    cas_options=get_cas_options(input_data)
    # LOG.write("%s\n" % cas_options)
    if cas_options:
     SE=ExpectEngine(name=cas_options['CAS'])   
     SE.cas_init(cas=cas_options['CAS'],
                     cas_prompt=cas_options['CASPrompt'],
                     cas_options=cas_options['CASOptions'],
                     cas_latex=cas_options['CASLatex'],
                     cas_latex_outsep=cas_options['CASLatexOutsep'],
                     cas_assign_string=cas_options['CASAssignString'],
                     cas_preamble=cas_options['CASPreamble']
             )
     LOG.msg("  => Found CAS Engine= %s\n" % cas_options['CAS'])
    else:
     LOG.msg("No CAS Engine Stated: using SymPy\n" )
     SE=SympyEngine()
    expanded_data=SE.expand_forcycle(input_data)
    LOG.write("done expanding forcycles!\n")
    if NOEXEC:
     LOG.write("NOT executing symexec and sym commands...\n")
     output_data=expanded_data
    else: 
     LOG.write("now executing symexec and sym commands...\n")
     output_data=SE.sym_filter(expanded_data)
    end_time=time.time()
    fd_output.write(SE.tex_comment( LOG.times(start_time,end_time,fd_output.name, casengine=SE.cas_engine) ) )
    fd_output.write(output_data)
    LOG.msg("\n")
    del SE
    LOG.msg("\n  => ...done! File %s created!\n" % fd_output.name)

if __name__=='__main__':
  # example_test() 
  main()
