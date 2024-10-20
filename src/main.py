import sys
from antlr4 import *

from antlr_src.VypParser import VypParser
from antlr_src.VypLexer import VypLexer


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = VypLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = VypParser(stream)
    tree = parser.program()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    print(tree.toStringTree(recog=parser))



if __name__ == '__main__':
    main(sys.argv)
