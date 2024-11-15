import src.compiler.exceptions as exceptions
from src.sym_table import *


def binary_op(func):
    def wrapper(self, ctx):
        op = ctx.op.text
        lhs = self.result[ctx.expr(0)]
        rhs = self.result[ctx.expr(1)]
        if lhs.data_type != rhs.data_type:
            raise exceptions.SemanticTypeError(f"{lhs.data_type} {op} {rhs.data_type} incompatible")
        _res = Symbol('tmp', SymbolTypes.VAR, 'int')
        self.result[ctx] = _res
        self.code_generator.binary_op(op)
        return func(self, ctx)
    return wrapper
