"""
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
"""

import sys
import traceback

from antlr4 import *

from antlr_src.VypParser import VypParser
from antlr_src.VypLexer import VypLexer
from compiler.exceptions import *
from compiler.lexical_error_listener import LexicalErrorListener
from compiler.definition_listener import DefinitionListener
from compiler.semantic_check_listener import SemanticListener
from utils import constants


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

    stdout_file = 'test.vc'
    if len(argv) == 3:
        stdout_file = argv[2]

    sys.stdout = open(stdout_file, "w")

    parser, tree = None, None
    try:
        lexer = VypLexer(input_stream)
        # lexer.removeErrorListener(ConsoleErrorListener.INSTANCE)
        lexical_error_listener = LexicalErrorListener()
        lexer.addErrorListener(lexical_error_listener)

        stream = CommonTokenStream(lexer)
        parser = VypParser(stream)
        # parser.removeErrorListener(ConsoleErrorListener.INSTANCE)  # useful for debugging
        tree = parser.program()
    except CompilerError as e:
        e.handle()

    if parser.getNumberOfSyntaxErrors() > 0:
        _exit(constants.SYNTAX_ERROR, "Syntax error")

    definition_listener = DefinitionListener()
    try:
        walker = ParseTreeWalker()
        walker.walk(definition_listener, tree)
    except CompilerError as e:
        e.handle()

    # 2nd pass
    semantic_checker = SemanticListener(definition_listener.getFunctionTable(), definition_listener.getClassTable())
    try:
        walker.walk(semantic_checker, tree)
    except CompilerError as e:
        e.handle()
    except Exception as e:
        traceback.print_exc()
        _exit(constants.SEMANTIC_DECLARATION_ERROR, str(e))


if __name__ == '__main__':
    main(sys.argv)
