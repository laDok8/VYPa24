from antlr4.tree.Tree import ParseTreeListener

from src.antlr_src.VypParser import VypParser  # for the constants
from src.sym_table import *
from src.sym_table.function_symbol import FunctionSymbol
from src.sym_table.symbol import SymbolTypes


class DefinitionListener(ParseTreeListener):
    """
    First pass of semantic control - build f() and class definitions

    Beware function names if you do typo you won't get any error nor enter any f()
    """

    def __init__(self):
        self.function_table = SymbolTable()
        self.symbol_table = SymbolTable()
        self.curr_class = None
        self.curr_fid = ''

    def getFunctionTable(self) -> SymbolTable:
        return self.function_table

    def exitProgram(self, _):
        # every good program should have a main function
        self.function_table.get_symbol("main")

        print("exiting 1st pass with symtable:")
        print(self.function_table)

    def _defineFunc(self, name, ret_type):
        self.curr_fid = name
        fun_sym = FunctionSymbol(name, ret_type)
        self.function_table.add_symbol(fun_sym)

    def _defineFuncArg(self, name, var_type):
        arg = Symbol(name, SymbolTypes.VAR, var_type)
        self.function_table.get_symbol(self.curr_fid).add_param(arg)

    def enterFunction_def(self, ctx: VypParser.Function_defContext):
        f_ret = ctx.ret_type().getText()
        f_id = ctx.ID().getText()
        self._defineFunc(f_id, f_ret)

    def enterF_param_def(self, ctx: VypParser.F_param_defContext):
        _id = ctx.ID().getText()
        _type = ctx.var_type().getText()
        self._defineFuncArg(_id, _type)

    def enterClass_def(self, ctx):
        pass

    def exitClass_def(self, ctx):
        pass

    def enterCode_block(self, ctx: VypParser.Code_blockContext):
        self.symbol_table.push_scope()

    def exitCode_block(self, ctx: VypParser.Code_blockContext):
        self.symbol_table.pop_scope()
