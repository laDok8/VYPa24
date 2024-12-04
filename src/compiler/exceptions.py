'''
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
'''

import sys


class CompilerError(Exception):
    def __init__(self, message, exit_code):
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code

    def handle(self):
        print(f"Error: {self.message}", file=sys.stderr)
        exit(self.exit_code)


class LexicalError(CompilerError):
    def __init__(self, message):
        super().__init__(message, 11)


class SyntaxError(CompilerError):
    def __init__(self, message):
        super().__init__(message, 12)


class SemanticTypeError(CompilerError):
    def __init__(self, message):
        super().__init__(message, 13)


class SemanticDeclarationError(CompilerError):
    def __init__(self, message):
        super().__init__(message, 14)


class CodeGenerationError(CompilerError):
    def __init__(self, message):
        super().__init__(message, 15)


class InternalError(CompilerError):
    def __init__(self, message):
        super().__init__(message, 19)
