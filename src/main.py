import sys

from antlr4 import *
from antlr4.error.ErrorListener import ConsoleErrorListener

from antlr_src.VypLexer import VypLexer
from antlr_src.VypParser import VypParser
from src.utils import _constants
from src.utils.lexical_error_listener import LexicalErrorListener


def _exit(code: int, message: str):
    print(message, file=sys.stderr)
    sys.exit(code)


def main(argv):
    input_stream = None  # stops IDE from complaining
    try:
        input_stream = FileStream(argv[1])
    except IndexError:
        _exit(_constants.INTERNAL_ERROR, "Missing argument: input file")
    except FileNotFoundError:
        _exit(_constants.INTERNAL_ERROR, "File not found")

    lexer = VypLexer(input_stream)
    lexer.removeErrorListener(ConsoleErrorListener.INSTANCE)  # useful for debugging
    lexical_error_listener = LexicalErrorListener()
    lexer.addErrorListener(lexical_error_listener)

    stream = CommonTokenStream(lexer)
    parser = VypParser(stream)
    parser.removeErrorListener(ConsoleErrorListener.INSTANCE)  # useful for debugging
    tree = parser.program()

    if lexical_error_listener.has_errors:
        _exit(_constants.LEXICAL_ERROR, "Lexical error")
    if parser.getNumberOfSyntaxErrors() > 0:
        _exit(_constants.SYNTAX_ERROR, "Syntax error")

    print(tree.toStringTree(recog=parser))
    # now it's time for semantic analysis (and code generation)


if __name__ == '__main__':
    main(sys.argv)
