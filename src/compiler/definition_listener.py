from antlr4.tree.Tree import ParseTreeListener

from src.antlr_src.VypParser import VypParser  # for the constants
from src.sym_table import *


class DefinitionListener(ParseTreeListener):
    """
    This class is responsible for semantic analysis and building the symbol table.

    Beware function names if you do typo you won't get any error nor enter any f()
    """

    def __init__(self):
        self.sym_table = SymbolTable()

    def exitProgram(self, ctx):
        # every good program should have a main function
        # self.sym_table.get_symbol("main")
        print("exiting with symtable:")
        print(self.sym_table)
        pass

    def enterFunction_def(self, ctx):
        # print("enterFunction_def", ctx.getText())
        # todo add f() as a symbol
        self.sym_table.push_scope()

    def exitFunction_def(self, ctx):
        # self.sym_table.pop_scope()
        pass

    def enterDeclaration(self, ctx):
        # print("varType:", ctx.children[0].children[0].symbol.text)
        # print("ID:", ctx.children[1].symbol.text)
        # print("constant trial:", VypParser.INT)
        # todo surprisingly string can match enum string but we should retype it
        _symbol = Symbol(ctx.children[1].symbol.text, ctx.children[0].children[0].symbol.text)
        self.sym_table.add_symbol(_symbol)
        #print("ID:", ctx.children[3].symbol.text)
        pass
