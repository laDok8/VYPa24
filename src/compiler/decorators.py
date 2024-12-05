'''
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
'''

import src.compiler.exceptions as exceptions
from src.sym_table import *


def binary_op(func):
    def wrapper(self, ctx):
        op = ctx.op.text
        lhs = self.result[ctx.expr(0)]
        rhs = self.result[ctx.expr(1)]

        if lhs.data_type != rhs.data_type:
            raise exceptions.SemanticTypeError(f"{lhs.data_type} {op} {rhs.data_type} incompatible")

        if op == '+' and lhs.data_type == 'string':
            return func(self, ctx) # solved in semantics

        if lhs.data_type not in ['int', 'string']:
            raise exceptions.SemanticTypeError(f"{op} {lhs.data_type} binary operation inapplicable")

        _res = Symbol('tmp', SymbolTypes.VAR, 'int') # note: not stored in symbol table
        self.result[ctx] = _res
        self.code_generator.binary_op(op,lhs.data_type)
        return func(self, ctx)

    return wrapper


def unary_op(func):
    def wrapper(self, ctx):
        op = ctx.op.text
        expr = self.result[ctx.expr()]
        if expr.data_type != 'int':
            raise exceptions.SemanticTypeError(f"{op} {expr.data_type} unary operation inapplicable")
        _res = Symbol('tmp', SymbolTypes.VAR, 'int')
        self.result[ctx] = _res
        self.code_generator.unary_op(op)
        return func(self, ctx)

    return wrapper
