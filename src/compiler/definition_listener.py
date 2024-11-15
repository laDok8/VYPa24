from antlr4.tree.Tree import ParseTreeListener

from src.antlr_src.VypParser import VypParser  # for the constants
from src.sym_table import *


class DefinitionListener(ParseTreeListener):
    """
    First pass of semantic control - build f() and class definitions

    Beware function names if you do typo you won't get any error nor enter any f()
    """

    def __init__(self):
        self.function_table = SymbolTable()
        self.symbol_table = SymbolTable()
        self.class_table = SymbolTable()
        self.curr_class = None
        self.curr_fun = None
        self._define_builtin()


    def getFunctionTable(self) -> SymbolTable:
        return self.function_table

    def getClassTable(self) -> SymbolTable:
        return self.class_table

    def exitProgram(self, _):
        # every good program should have a main function
        self.function_table.get_symbol("main")

        # set parents for classes
        for class_sym in self.class_table.get_current_symbols().values():
            if not class_sym.parent:
                continue
            class_sym.set_parent(self.class_table.get_symbol(class_sym.parent))

    def _define_builtin(self):
        # classes
        object_sym = ClassSymbol("Object", None)
        object_sym.add_method(FunctionSymbol('toString', 'string'))
        object_sym.add_method(FunctionSymbol('getClass', 'string'))
        self.class_table.add_symbol(object_sym)

        # functions
        self.function_table.add_symbol(FunctionSymbol("print", "void"))
        self.function_table.add_symbol(FunctionSymbol("readInt", "int"))
        self.function_table.add_symbol(FunctionSymbol("readString", "string"))

        length_func = FunctionSymbol('length', 'int')
        length_func.add_param(Symbol('s', SymbolTypes.VAR, 'string'))

        substr_func = FunctionSymbol('subStr', 'string')
        substr_func.add_param(Symbol('s', SymbolTypes.VAR, 'string'))
        substr_func.add_param(Symbol('i', SymbolTypes.VAR, 'int'))
        substr_func.add_param(Symbol('n', SymbolTypes.VAR, 'int'))

        self.function_table.add_symbol(length_func)
        self.function_table.add_symbol(substr_func)

    def _defineFunc(self, name, ret_type):
        fun_sym = FunctionSymbol(name, ret_type)
        self.curr_fun = fun_sym

        if self.curr_class:
            self.curr_class.add_method(fun_sym)
        else:
            self.function_table.add_symbol(fun_sym)

    def _defineFuncArg(self, name, var_type):
        arg = Symbol(name, SymbolTypes.VAR, var_type)
        self.curr_fun.add_param(arg)

    def enterFunction_def(self, ctx: VypParser.Function_defContext):
        f_ret = ctx.ret_type().getText()
        f_id = ctx.ID().getText()
        self._defineFunc(f_id, f_ret)

    def enterF_param_def(self, ctx: VypParser.F_param_defContext):
        _id = ctx.ID().getText()
        _type = ctx.var_type().getText()
        self._defineFuncArg(_id, _type)

    def enterClass_def(self, ctx: VypParser.Class_defContext):
        c_name, prt_name = ctx.class_id.text, ctx.parent_id.text
        _class = ClassSymbol(c_name, prt_name)
        self.curr_class = _class
        self.class_table.add_symbol(_class)

    def exitClass_def(self, ctx: VypParser.Class_defContext):
        self.curr_class = None

    def enterCode_block(self, ctx: VypParser.Code_blockContext):
        self.symbol_table.push_scope()

    def exitCode_block(self, ctx: VypParser.Code_blockContext):
        self.symbol_table.pop_scope()

    def enterClass_field(self, ctx: VypParser.Class_fieldContext):
        _type = ctx.declaration().var_type().getText()
        # TODO: need to check types, unable to do it here

        # multiple ids can be declared at once
        for _id in ctx.declaration().ID():
            _symbol = Symbol(_id.getText(), SymbolTypes.VAR, _type)
            self.curr_class.add_field(_symbol)

    def exitFunction_def(self, ctx: VypParser.Function_defContext):
        self.curr_fun = None
