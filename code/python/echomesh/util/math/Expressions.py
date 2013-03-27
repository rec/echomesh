from pyparsing import Literal, CaselessLiteral, Word, Group, Optional, \
    ZeroOrMore, Forward, nums, alphas, Regex, ParseException

import math
import operator
import re

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
    def pushFirst(strg, loc, toks):
        exprStack.append(toks[0])

    def pushUMinus(strg, loc, toks):
        for t in toks:
          if t == '-':
            exprStack.append('unary -')
            #~ exprStack.append('-1')
            #~ exprStack.append('*')
          else:
            break

    point = Literal('.')
    e     = CaselessLiteral('E')
    #~ fnumber = Combine(Word('+-'+nums, nums) +
                       #~ Optional(point + Optional(Word(nums))) +
                       #~ Optional(e + Word('+-'+nums, nums)))
    fnumber = Regex(r' [+-]? \d+ (:? \. \d* )? (:? [eE] [+-]? \d+)?', re.X)
    xnumber = Regex(r'0 [xX] [0-9 a-f A-F]+', re.X)
    ident = Word(alphas, alphas+nums+'_$')

    plus  = Literal('+')
    minus = Literal('-')
    mult  = Literal('*')
    div   = Literal('/')
    lpar  = Literal('(').suppress()
    rpar  = Literal(')').suppress()
    addop  = plus | minus
    multop = mult | div
    expop = Literal('^')
    pi    = CaselessLiteral('PI')

    expr = Forward()
    atom_parts = pi | e | fnumber | xnumber | ident + lpar + expr + rpar | ident
    atom_action = atom_parts.setParseAction(pushFirst)
    group = Group(lpar + expr + rpar)
    atom = ((0, None) * minus + atom_action | group).setParseAction(pushUMinus)

    # by defining exponentiation as 'atom [ ^ factor ]...' instead of 'atom [ ^ atom ]...', we get right-to-left exponents, instead of left-to-righ
    # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
    factor = Forward()
    factor << atom + ZeroOrMore((expop + factor).setParseAction(pushFirst))

    term = factor + ZeroOrMore((multop + factor).setParseAction(pushFirst))
    expr << term + ZeroOrMore((addop + term).setParseAction(pushFirst))
    return expr


# map operator symbols to corresponding arithmetic operations
epsilon = 1e-12
opn = { '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '/' : operator.truediv,
        '^' : operator.pow }
fn  = { 'sin' : math.sin,
        'cos' : math.cos,
        'tan' : math.tan,
        'abs' : abs,
        'trunc' : lambda a: int(a),
        'round' : round,
        'sgn' : lambda a: abs(a)>epsilon and cmp(a,0) or 0}

def evaluateStack(s):
    op = s.pop()
    if op == 'unary -':
        return -evaluateStack(s)
    if op in '+-*/^':
        op2 = evaluateStack(s)
        op1 = evaluateStack(s)
        return opn[op](op1, op2)
    elif op == 'PI':
        return math.pi # 3.1415926535
    elif op == 'E':
        return math.e  # 2.718281828
    elif op in fn:
        return fn[op](evaluateStack(s))
    elif op[0].isalpha():
        raise Exception('invalid identifier "%s"' % op)
    elif op.startswith('0x') or op.startswith('0X'):
        return int(op, 16)
    elif '.' in op or 'e' in op or 'E' in op:
        return float(op)
    else:
        return int(op)

def evaluate(expression, exprStack=None):
  exprStack = exprStack or []
  bnf(exprStack).parseString(expression, parseAll=True)
  return evaluateStack(exprStack[:])

from pyparsing import ParserElement

ParserElement.verbose_stacktrace = True
