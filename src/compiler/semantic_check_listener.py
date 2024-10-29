from antlr4.tree.Tree import ParseTreeListener

from src.antlr_src.VypParser import VypParser  # for the constants
from src.sym_table import *
from src.sym_table.symbol import SymbolTypes


class SemanticListener(ParseTreeListener):
    """
    2nd pass of semantic builder - type checks and build AST

    Beware function names if you do typo you won't get any error nor enter any f()
    """

    def __init__(self, fun_symbols: SymbolTable):
        self.fun_symbols = fun_symbols
        self.sym_table = SymbolTable()



    def enterFunction_def(self, ctx: VypParser.Function_defContext):
        self.sym_table.push_scope()

        f_id = ctx.ID().getText()

        #TODO: take symbols from existing

    def exitFunction_def(self, ctx: VypParser.Function_defContext):
        self.sym_table.pop_scope()

    def enterDeclaration(self, ctx: VypParser.DeclarationContext):
        _type = ctx.var_type().getText()

        # TODO: check if type exists


        # multiple ids can be declared at once
        # for _id in ctx.ID():
        #     _symbol = Symbol(_id.getText(), _type)
        #     self.sym_table.add_symbol(_symbol)
        pass


    def enterClass_def(self, ctx: VypParser.Class_defContext):
        pass
        # TODO: symbols

    def exitClass_def(self, ctx: VypParser.Class_defContext):
        pass
