"""
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
"""

from antlr4.error.ErrorListener import ErrorListener

from compiler.exceptions import LexicalError


class LexicalErrorListener(ErrorListener):
    def __init__(self):
        super(LexicalErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise LexicalError(f"Lexical error at line {line}, column {column}: {msg}")
