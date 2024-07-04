from tools.cmp.pycompiler import Grammar
from tools.automata import NFA, nfa_to_dfa
from tools.automata import automata_union, automata_concatenation, automata_closure, automata_minimization
from tools.cmp.ast import get_printer, AtomicNode, UnaryNode, BinaryNode
from tools.cmp.utils import Token
from tools.parsers import LL1Parser
from tools.evaluation import evaluate_parse

printer = get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode)

# AST Nodes
EPSILON = 'ε'

class EpsilonNode(AtomicNode):
    def evaluate(self):
        states = 1
        finals = [0]
        transitions = {}
        return NFA(states, finals, transitions)
# EpsilonNode(EPSILON).evaluate()

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        states = 2
        finals = [1]
        transitions = {(0, s): [1]}
        return NFA(states, finals, transitions)
# SymbolNode('a').evaluate()

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)
# ClosureNode(SymbolNode('a')).evaluate()

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)
# UnionNode(SymbolNode('a'), SymbolNode('b')).evaluate()

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)
# ConcatNode(SymbolNode('a'), SymbolNode('b')).evaluate()

# ============================================= GRAMMAR DEFINITION =========================================
G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z,  = G.NonTerminals('T F A X Y Z ')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')
scape = G.Terminal('\\')

# > PRODUCTIONS
E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]

X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0], s[2])
X %= G.Epsilon, lambda h,s: h[0]

T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]

Y %= F + Y, lambda h,s: s[2], None, lambda h,s:ConcatNode(h[0], s[1])
Y %= G.Epsilon, lambda h,s: h[0]

F %= A + Z, lambda h,s: s[2], None, lambda h,s: s[1]

Z %= star + Z, lambda h,s: s[2], None, lambda h,s: ClosureNode(h[0])
Z %= G.Epsilon, lambda h,s: h[0]


def tmp(h,s):
           return SymbolNode(s[2])
A %= scape + symbol , tmp ,None ,None
A %= symbol , lambda h,s : SymbolNode(s[1]) , None
A %= opar + E + cpar, lambda h,s: s[2], None, None, None
A %= epsilon, lambda h,s: EpsilonNode(s[1]), None


# =============================================REGEX DEFINITION =========================================

def regex_tokenizer(text, G, skip_whitespaces=True) -> list[Token]:
    tokens = []
    fixed_tokens = {
        '|': Token('|', pipe),
        '*': Token('*', star),
        'ε': Token('ε', epsilon),
        '(': Token('(', opar),
        ')': Token(')', cpar),
        '\\': Token('\\',scape)
    }

    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        if len(tokens)>0 and tokens[-1].lex == '\\':
                tokens.append(Token(char, symbol))
        else:
            try:
                tokens.append(fixed_tokens[char])
            except KeyError:
                tokens.append(Token(char, symbol))

    tokens.append(Token('\0', G.EOF))
    return tokens

class Regex:
    def __init__(self, regex: str, skip_whitespaces=False) -> None:
        self.regex = regex
        self.automaton = self.build_automaton(regex, skip_whitespaces)
        
    def __call__(self, text: str):
        return self.automaton.recognize(text)

    @staticmethod
    def build_automaton(regex: str, skip_whitespaces=False):
        tokens = regex_tokenizer(regex, G, skip_whitespaces)
        parser = LL1Parser(G)
        left_parse = parser([t.token_type for t in tokens])
        
        ast = evaluate_parse(left_parse, tokens)
        # Automaton
        nfa = ast.evaluate()
        # display(nfa)
        dfa = nfa_to_dfa(nfa)
        # display(dfa)
        mini = automata_minimization(dfa)
        # display(mini)
        return mini

