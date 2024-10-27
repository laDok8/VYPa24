from antlr4.tree.Tree import ParseTreeListener

from src.antlr_src.VypParser import VypParser  # for the constants
from src.sym_table import *
from src.sym_table.symbol import SymbolTypes


# TODO: check signatures of functions (and vars) in 2nd pass as class may not be defined yet

class DefinitionListener(ParseTreeListener):
    """
    This class is responsible for semantic analysis and building the symbol table.

    Beware function names if you do typo you won't get any error nor enter any f()
    """

    def __init__(self):
        self.sym_table = SymbolTable()

    def exitProgram(self, ctx):
        # every good program should have a main function
        self.sym_table.get_symbol("main")

        print("exiting with symtable:")
        print(self.sym_table)
        pass

    def enterFunction_def(self, ctx: VypParser.Function_defContext):
        # f_def has to be in a global scope
        self.sym_table.push_scope()

        f_ret = ctx.ret_type().getText()
        f_id = ctx.ID().getText()
        f_args = []
        if ctx.f_param_list():
            _params = ctx.f_param_list().param()

            for _param in _params:
                _var_type = _param.var_type().getText()
                _id = _param.ID().getText()
                _symbol = Symbol(_id, _var_type)
                self.sym_table.add_symbol(_symbol)
                f_args.append(_id)

        f_symbol = Symbol(f_id, SymbolTypes.FNC, f_args=f_args, f_ret=f_ret)
        self.sym_table.add_global_symbol(f_symbol)

    def exitFunction_def(self, ctx):
        self.sym_table.pop_scope()

    def enterDeclaration(self, ctx: VypParser.DeclarationContext):
        _type = ctx.var_type().getText()

        # multiple ids can be declared at once
        for _id in ctx.ID():
            _symbol = Symbol(_id.getText(), _type)
            self.sym_table.add_symbol(_symbol)

        # TODO: surprisingly string can match enum string but we should retype it
        pass

    def enterIf_else_stmt(self, ctx):
        self.sym_table.push_scope()
        pass

    def exitIf_else_stmt(self, ctx):
        self.sym_table.pop_scope()
        pass

    def enterWhile_stmt(self, ctx):
        self.sym_table.push_scope()
        pass

    def exitWhile_stmt(self, ctx):
        self.sym_table.pop_scope()
        pass

    def enterClass_def(self, ctx):
        self.sym_table.push_scope()
        pass

    def exitClass_def(self, ctx):
        self.sym_table.pop_scope()
        pass
