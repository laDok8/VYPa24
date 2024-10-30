from antlr4.tree.Tree import ParseTreeListener

from src.antlr_src.VypParser import VypParser  # for the constants
from src.sym_table import *
from src.sym_table.symbol import SymbolTypes


class SemanticListener(ParseTreeListener):
    """
    2nd pass of semantic builder - type checks and build AST

    Beware function names if you do typo you won't get any error nor enter any f()
    """

    def __init__(self, fun_symbols: SymbolTable, class_symbols: SymbolTable):
        self.fun_symbols = fun_symbols
        self.class_symbols = class_symbols
        self.sym_table = SymbolTable()
        self._legal_data_types = ['int', 'string']
        # add classes to legal data types
        self._legal_data_types.extend([sym for sym in class_symbols.get_current_symbols()])

    def assert_legal_data_type(self, _type):
        if _type not in self._legal_data_types:
            raise ValueError(f"Unknown data type {_type}")

    def assert_legal_return_type(self, _type):
        if _type not in [*self._legal_data_types, 'void']:
            raise ValueError(f"Unknown return type {_type}")

    def enterFunction_def(self, ctx: VypParser.Function_defContext):
        # this way f() pushes 2 scopes
        self.sym_table.push_scope()

        fun_name = ctx.ID().getText()
        current_fun = self.fun_symbols.get_symbol(fun_name)
        self.assert_legal_return_type(current_fun.get_return_type())
        for param in current_fun.get_params():
            self.assert_legal_data_type(param.data_type)
            self.sym_table.add_symbol(param)

    def exitFunction_def(self, ctx: VypParser.Function_defContext):
        self.sym_table.pop_scope()

    def enterDeclaration(self, ctx: VypParser.DeclarationContext):
        _type = ctx.var_type().getText()
        self.assert_legal_data_type(_type)

        # multiple ids can be declared at once
        for _id in ctx.ID():
            _symbol = Symbol(_id.getText(), SymbolTypes.VAR, _type)
            self.sym_table.add_symbol(_symbol)
        pass

    def enterClass_def(self, ctx: VypParser.Class_defContext):
        self.sym_table.push_scope()
        self.fun_symbols.push_scope()
        class_name = ctx.class_id.text
        current_class = self.class_symbols.get_symbol(class_name)

        # add symbols from class to the table - f()
        # fields are added in declarations
        for method in current_class.get_methods().values():
            self.fun_symbols.add_symbol(method)

    def exitClass_def(self, ctx: VypParser.Class_defContext):
        self.sym_table.pop_scope()
        self.fun_symbols.pop_scope()
