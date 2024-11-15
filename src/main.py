import sys

from antlr4 import *
from antlr4.error.ErrorListener import ConsoleErrorListener

from antlr_src.VypLexer import VypLexer
from antlr_src.VypParser import VypParser
from src.compiler import *
from src.utils import constants


def _exit(code: int, message: str):
    print(message, file=sys.stderr)
    sys.exit(code)


def main(argv):
    input_stream = None  # stops IDE from complaining
    try:
        input_stream = FileStream(argv[1])
    except IndexError:
        _exit(constants.INTERNAL_ERROR, "Missing argument: input file")
    except FileNotFoundError:
        _exit(constants.INTERNAL_ERROR, "File not found")

    parser, tree = None, None
    try:
        lexer = VypLexer(input_stream)
        lexer.removeErrorListener(ConsoleErrorListener.INSTANCE)  # useful for debugging
        lexical_error_listener = LexicalErrorListener()
        lexer.addErrorListener(lexical_error_listener)

        stream = CommonTokenStream(lexer)
        parser = VypParser(stream)
        parser.removeErrorListener(ConsoleErrorListener.INSTANCE)  # useful for debugging
        tree = parser.program()
    except CompilerError as e:
        e.handle()

    if parser.getNumberOfSyntaxErrors() > 0:
        _exit(constants.SYNTAX_ERROR, "Syntax error")

    definition_listener = DefinitionListener()
    walker = ParseTreeWalker()
    walker.walk(definition_listener, tree)

    # 2nd pass
    semantic_checker = SemanticListener(definition_listener.getFunctionTable(), definition_listener.getClassTable())
    try:
        walker.walk(semantic_checker, tree)
    except CompilerError as e:
        e.handle()


if __name__ == '__main__':
    main(sys.argv)
