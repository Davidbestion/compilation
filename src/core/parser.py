from tools.cmp.evaluation import evaluate_reverse_parse
from tools.cmp.utils import Token
from tools.parsers import LR1Parser
from core.grammar import G

parser = None

def parse(tokens: list[Token]):
    print('>>> Parsing...')

    if parser == None:
        parse = LR1Parser(G,verbose=False)
    result = parse(tokens, get_shift_reduce=True)

    right_parse, operations = result
    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    return ast

def build_parser():
    return LR1Parser(G, verbose=False)

