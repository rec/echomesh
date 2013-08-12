from __future__ import absolute_import, division, print_function, unicode_literals

import re

from pyparsing import Literal, Word, Group, Optional, \
  ZeroOrMore, Forward, nums, alphas, Regex

def bnf(exprStack):
  """
  expop   :: '^'
  multop  :: '*' | '/'
  addop   :: '+' | '-'
  integer :: ['+' | '-'] '0'..'9'+
  atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
  factor  :: atom [ expop factor ]*
  term    :: factor [ multop factor ]*
  expr    :: term [ addop term ]*
  """
  def pushFirst(_, __, toks):
    exprStack.append(toks[0])

  def pushUMinus(_, __, toks):
    for t in toks:
      if t == '-':
        exprStack.append('unary -')
      else:
        break

  fnumber = Regex(r' [+-]? \d+ (:? \. \d* )? (:? [eE] [+-]? \d+)?', re.X)
  xnumber = Regex(r'0 [xX] [0-9 a-f A-F]+', re.X)
  ident = Word(alphas, alphas + nums + '_$.')

  plus  = Literal('+')
  minus = Literal('-')
  mult  = Literal('*')
  div   = Literal('/')

  lpar  = Literal('(').suppress()
  rpar  = Literal(')').suppress()
  addop  = plus | minus
  multop = mult | div
  expop = Literal('**')

  expr = Forward()
  atom_parts = fnumber | xnumber | ident + lpar + expr + rpar | ident
  atom_action = atom_parts.setParseAction(pushFirst)
  group = Group(lpar + expr + rpar)
  atom = ((0, None) * minus + atom_action | group).setParseAction(pushUMinus)

  # by defining exponentiation as 'atom [ ^ factor ]...'
  # instead of 'atom [ ^ atom ]...', we get right-to-left exponents, instead of left-to-righ
  # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
  factor = Forward()
  factor << atom + ZeroOrMore((expop + factor).setParseAction(pushFirst))

  term = factor + ZeroOrMore((multop + factor).setParseAction(pushFirst))
  expr << term + ZeroOrMore((addop + term).setParseAction(pushFirst))

  return expr
