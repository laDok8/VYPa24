'''
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
'''

from src.code_gen.register import Register
from src.code_gen.stack import Stack


class Literal:
    @staticmethod
    def int_literal(value):
        body = f'# int literal {value}\n'
        body += f'{Stack.push(value)}\n\n'
        return body

    @staticmethod
    def string_literal(value):
        body = f'# string literal {value}\n'
        body += f'CREATE {Register.DI} 1\n'
        body += f'SETWORD {Register.DI} 0 {value}\n'
        body += f'GETWORD {Register.DI} {Register.DI} 0\n'
        body += f'{Stack.push(Register.DI)}\n\n'
        return body
