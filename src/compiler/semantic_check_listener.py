from antlr4.tree.Tree import ParseTreeListener

from src.antlr_src.VypParser import VypParser  # for the constants
from src.code_gen.code_generator import *
from src.sym_table import *


class SemanticListener(ParseTreeListener):
    """
    2nd pass of semantic builder - type checks and build AST

    Beware function names if you do typo you won't get any error nor enter any f()
    """

    def __init__(self, fun_symbols: SymbolTable, class_symbols: SymbolTable):
        self.fun_call_stack = []
        self.fun_symbols = fun_symbols
        self.class_symbols = class_symbols
        self.sym_table = SymbolTable()
        self._legal_data_types = ['int', 'string']
        self.code_generator = CodeGenerator()
        # add classes to legal data types
        self._legal_data_types.extend([sym for sym in class_symbols.get_current_symbols()])
        self.result = {}

    def exitProgram(self, _):
        self.code_generator.generate_code()

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

        self.code_generator.function_def(fun_name)

    def exitFunction_def(self, ctx: VypParser.Function_defContext):
        self.sym_table.pop_scope()
        self.code_generator.exit_function()

    def enterDeclaration(self, ctx: VypParser.DeclarationContext):
        _type = ctx.var_type().getText()
        self.assert_legal_data_type(_type)

        # multiple ids can be declared at once
        for _id in ctx.ID():
            _symbol = Symbol(_id.getText(), SymbolTypes.VAR, _type)
            self.sym_table.add_symbol(_symbol)
            self.code_generator.declaration(_symbol)

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

    def enterFun_call(self, ctx: VypParser.Fun_callContext):
        self.fun_call_stack.append([])

    def exitFun_call(self, ctx: VypParser.Fun_callContext):
        fun_name = ctx.ID().getText()
        args = self.result[ctx.f_call_list()]
        if fun_name == 'print':
            self.code_generator.print(args)
        else:
            self.code_generator.fun_call(fun_name)


    def exitLiteral_expr(self, ctx: VypParser.Literal_exprContext):
        _sym = Symbol(ctx.getText(), SymbolTypes.LIT, 'string' if ctx.literal_val().INT_LIT() is None else 'int')
        self.code_generator.literal(_sym)
        self.result[ctx] = _sym

    def exitF_call_list(self, ctx: VypParser.F_call_listContext):
        # arg_count = len(self.fun_call_stack[-1])
        f_args = []
        for arg in ctx.expr():
            f_args.append(self.result[arg])
        self.result[ctx] = f_args

    def exitStatement(self, ctx: VypParser.StatementContext):
        self.code_generator.restore_stack()
