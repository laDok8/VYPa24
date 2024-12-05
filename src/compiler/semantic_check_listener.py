'''
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
'''
from symtable import Class

from antlr4.tree.Tree import ParseTreeListener

from src.antlr_src.VypParser import VypParser  # for the constants
from src.code_gen.code_generator import *
from src.compiler.decorators import binary_op, unary_op
from src.compiler.exceptions import *
from src.sym_table import *


class SemanticListener(ParseTreeListener):
    """
    2nd pass of semantic builder - type checks and build AST

    Beware function names if you do typo you won't get any error nor enter any f()
    """

    def __init__(self, fun_symbols: SymbolTable, class_symbols: SymbolTable):
        self.skip_field_redeclaration = False
        self.fun_symbols = fun_symbols
        self.class_symbols = class_symbols
        self.sym_table = SymbolTable()
        self._legal_data_types = ['int', 'string']
        self.code_generator = CodeGenerator()
        # add classes to legal data types
        self._legal_data_types.extend([sym for sym in class_symbols.get_current_symbols().keys()])
        self.result = {}  # store results of expressions
        self.curr_class = None
        self.curr_obj = None
        self.cur_fun = None
        self.assigning_instance = False

        # generate VMT
        for class_sym in class_symbols.get_current_symbols().values():
            self.code_generator.VMT(class_sym)

    def exitProgram(self, _):
        # comment this to suppress output for debugging
        self.code_generator.generate_code()
        pass

    def assert_legal_data_type(self, _type):
        if _type not in self._legal_data_types:
            raise SemanticDeclarationError(f"Unknown data type {_type}")

    def assert_legal_return_type(self, _type):
        if _type not in [*self._legal_data_types, 'void']:
            raise SemanticDeclarationError(f"Unknown return type {_type}")

    def enterFunction_def(self, ctx: VypParser.Function_defContext):
        # this way f() pushes 2 scopes
        self.sym_table.push_scope()

        fun_name = ctx.ID().getText()
        current_fun = self.fun_symbols.get_symbol(fun_name)
        self.cur_fun = current_fun

        if self.curr_class:
            current_fun = self.curr_class.get_method(fun_name)
            self.cur_fun = current_fun

        self.assert_legal_return_type(current_fun.get_return_type())
        for param in current_fun.get_params():
            self.assert_legal_data_type(param.data_type)
            self.sym_table.add_symbol(param)

        self.code_generator.function_def(current_fun)

    def exitFunction_def(self, ctx: VypParser.Function_defContext):
        self.sym_table.pop_scope()
        self.code_generator.exit_function()

    def enterDeclaration(self, ctx: VypParser.DeclarationContext):
        if self.skip_field_redeclaration:
            return

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
        self.curr_class = self.class_symbols.get_symbol(class_name)

        # add symbols and fields from class to the table - f()
        for method in self.curr_class.getVMT().values():
            self.fun_symbols.add_symbol(method)
        for field in self.curr_class.get_fields().values():
            self.sym_table.add_symbol(field)

    def exitClass_def(self, ctx: VypParser.Class_defContext):
        self.sym_table.pop_scope()
        self.fun_symbols.pop_scope()
        self.curr_class = None

    def exitFun_call(self, ctx: VypParser.Fun_callContext):
        fun_name = ctx.ID().getText()
        fun_sym = self.fun_symbols.get_symbol(fun_name)
        if self.curr_obj:
            fun_sym = self.curr_obj.get_method(fun_name)
        args = self.result[ctx.f_call_list()]
        self.verify_fun_signature(fun_sym, args)

        super_call = self.curr_class is not None and self.curr_obj != self.curr_class

        self.code_generator.fun_call(fun_sym, args, super_call=super_call)
        self.result[ctx] = fun_sym

    def exitLiteral_expr(self, ctx: VypParser.Literal_exprContext):
        _sym = Symbol(ctx.getText(), SymbolTypes.LIT, 'string' if ctx.literal_val().INT_LIT() is None else 'int')
        self.code_generator.literal(_sym)
        self.result[ctx] = _sym

    def exitF_call_list(self, ctx: VypParser.F_call_listContext):
        f_args = []
        for arg in ctx.expr():
            res = self.result[arg]
            if isinstance(res, str):
                _res = self.sym_table.get_symbol(res)
                f_args.append(_res)
            else:
                f_args.append(res)
        self.result[ctx] = f_args

    def exitStatement(self, ctx: VypParser.StatementContext):
        self.code_generator.restore_stack()

    def enterClass_field(self, ctx: VypParser.Class_fieldContext):
        """due to grammar structure, we would redeclare fields as vars without this"""
        self.skip_field_redeclaration = True

    def exitClass_field(self, ctx: VypParser.Class_fieldContext):
        self.skip_field_redeclaration = False

    def exitInstance_creation(self, ctx: VypParser.Instance_creationContext):
        class_name = ctx.ID().getText()
        class_sym = self.class_symbols.get_symbol(class_name)
        self.result[ctx] = class_sym
        self.code_generator.create_instance(class_sym)

    def enterFirst_instance_ref(self, ctx: VypParser.First_instance_refContext):
        cls_sym = None
        if ctx.THIS():
            cls_sym = self.curr_class
            instance_sym = 'this'
        elif ctx.SUPER():
            cls_sym = self.curr_class.parent
            instance_sym = 'super'
        else:
            left = ctx.ID().getText()
            instance_sym = self.sym_table.get_symbol(left)
            cls_sym = self.class_symbols.get_symbol(instance_sym.data_type)
            instance_sym = instance_sym.name

        self.code_generator.push_expr(cls_sym, instance_sym, copy_to_obj_reg=True)

    def exitInstance_expr(self, ctx: VypParser.Instance_exprContext):
        first = self.result[ctx.first_instance_ref()]

        rightmost_sym = self.result[ctx.nested_invocation()]

        # get class symbol
        self.result[ctx] = rightmost_sym
        self.curr_obj = None
        # we either left side or expression altogether
        self.assigning_instance = False

    def exitFirst_instance_ref(self, ctx: VypParser.First_instance_refContext):
        if ctx.fun_call():
            self.result[ctx] = self.result[ctx.fun_call()]
        elif ctx.THIS():
            self.result[ctx] = self.curr_class
            self.curr_obj = self.curr_class
        elif ctx.SUPER():
            self.result[ctx] = self.curr_class.parent
            self.curr_obj = self.curr_class.parent
        else:
            _sym = self.sym_table.get_symbol(ctx.ref.text)
            _sym_type = _sym.data_type
            _cls_sym = self.class_symbols.get_symbol(_sym_type)
            self.curr_obj = _cls_sym
            self.result[ctx] = ctx.ID().getText()

    def enterNested_invocation(self, ctx: VypParser.Nested_invocationContext):
        # push next object ref, calls are solved automagically TODO: need to push cls ref
        if ctx.ID() is not None:
            field_name = ctx.ID().getText()
            if field_name:
                # when assigning to field we shouldn't push last one
                if not self.assigning_instance or ctx.nested_invocation():  # a -> b
                    field_sym = self.curr_obj.get_field(field_name)
                    self.code_generator.field_expr(field_sym)

    def exitNested_invocation(self, ctx: VypParser.Nested_invocationContext):
        # I just need to return last symbol
        if ctx.fun_call():
            res = self.result[ctx.fun_call()]
        else:
            res = ctx.ID().getText()  # field name
            res = self.curr_obj.get_field(res)
        if ctx.nested_invocation():
            res = self.result[ctx.nested_invocation()]
        self.result[ctx] = res

    def exitVar_assign(self, ctx: VypParser.Var_assignContext):
        right_sym = self.result[ctx.expr()]
        _id = ctx.ID().getText()
        left_sym = self.sym_table.get_symbol(_id)


        if right_sym.data_type not in ['int', 'string']:
            if isinstance(right_sym,FunctionSymbol):
                right_sym = self.class_symbols.get_symbol(right_sym.data_type)
            left_cls_sym = self.class_symbols.get_symbol(left_sym.data_type)
            if not left_cls_sym.is_direct_parent(right_sym):
                raise SemanticTypeError(f'assigning incompatible types {left_sym.data_type} = {right_sym.data_type}')
        elif right_sym.data_type != left_sym.data_type:
            raise SemanticTypeError(f'assigning incompatible types {left_sym.data_type} = {right_sym.data_type}')
        self.code_generator.assign_var(_id)

    def exitId_expr(self, ctx: VypParser.Id_exprContext):
        _id = ctx.ID().getText()
        # get symbol
        _sym = self.sym_table.get_symbol(_id)
        self.result[ctx] = _sym
        self.code_generator.push_object(_id)

    def enterInstance_assign(self, ctx: VypParser.Instance_assignContext):
        self.assigning_instance = True

    def exitInstance_assign(self, ctx: VypParser.Instance_assignContext):
        field = self.result[ctx.instance_expr()]
        self.code_generator.assign_field(field)
        self.code_generator.ResetExprClass()

    def exitInvocation_expr(self, ctx: VypParser.Invocation_exprContext):
        cls_member_sym = self.result[ctx.instance_expr()]
        self.result[ctx] = cls_member_sym
        # self.code_generator.field_expr(cls_member_sym)
        self.code_generator.ResetExprClass()

    @binary_op
    def exitAdd_sub_expr(self, ctx: VypParser.Add_sub_exprContext):
        lhs = self.result[ctx.expr(0)]
        rhs = self.result[ctx.expr(1)]

        if lhs.data_type == 'string':
            fun_sym = self.fun_symbols.get_symbol('__str_concat__')
            self.code_generator.fun_call(fun_sym, [lhs, rhs])
            _res = Symbol('tmp', SymbolTypes.VAR, 'string')
            self.result[ctx] = _res
            return

    @binary_op
    def exitMul_div_expr(self, ctx: VypParser.Mul_div_exprContext):
        pass

    @binary_op
    def exitRel_expr(self, ctx: VypParser.Rel_exprContext):
        pass

    @binary_op
    def exitEq_expr(self, ctx: VypParser.Eq_exprContext):
        pass

    @binary_op
    def exitAnd_expr(self, ctx: VypParser.And_exprContext):
        pass

    @binary_op
    def exitOr_expr(self, ctx: VypParser.Or_exprContext):
        pass

    def exitRet_stmt(self, ctx: VypParser.Ret_stmtContext):
        if self.cur_fun is None:
            raise SemanticTypeError("Return statement outside of function context")

        sym = None  # void
        if ctx.expr():
            sym = self.result[ctx.expr()]

        if sym is None:
            if self.cur_fun.get_return_type() != 'void':
                raise SemanticTypeError(f"Return mismatch {sym} != {self.cur_fun.get_return_type()}")
        else:
            if isinstance(sym, str):
                _sym = self.sym_table.get_symbol(sym)
                if _sym is None:
                    sym = self.sym_table.get_symbol(sym)
                else:
                    sym = _sym

            if sym.data_type != self.cur_fun.get_return_type():
                # for classes
                if isinstance(sym, ClassSymbol):
                    ret_type_sym = self.class_symbols.get_symbol(self.cur_fun.get_return_type())
                    if not sym.is_direct_parent(ret_type_sym):
                        raise SemanticTypeError(f"Return mismatch {sym.data_type} != {self.cur_fun.get_return_type()}")
                else:
                    raise SemanticTypeError(f"Return mismatch {sym.data_type} != {self.cur_fun.get_return_type()}")

        self.code_generator.ret_val(sym)

    def exitFun_call_expr(self, ctx: VypParser.Fun_call_exprContext):
        self.result[ctx] = self.result[ctx.fun_call()]

    def verify_fun_signature(self, fun_sym, args):
        arg_types = []
        for arg in args:
            if isinstance(arg, str):
                _arg = self.sym_table.get_symbol(arg)
                arg_types.append(_arg.data_type)
            else:
                arg_types.append(arg.data_type)

        if fun_sym.name == 'print':
            return all(arg_type in ['int', 'string'] for arg_type in arg_types)

        param_types = [param.data_type for param in fun_sym.get_params()]
        if arg_types != param_types:
            raise SemanticTypeError(f"Function call mismatch {arg_types} != {param_types}")

    def exitIf_cond(self, ctx: VypParser.If_condContext):
        ln = ctx.start.line
        not_label = self.cur_fun.name + "_" + str(ln) + '_else'
        end_label = self.cur_fun.name + "_" + str(ln) + '_end'
        self.code_generator.gen_enter_if(not_label, end_label)

    def exitIf_else_stmt(self, ctx: VypParser.If_else_stmtContext):
        self.code_generator.gen_exit_if_else()

    def enterElse_stmt(self, ctx: VypParser.Else_stmtContext):
        self.code_generator.gen_enter_else()

    def enterWhile_cond(self, ctx: VypParser.While_condContext):
        ln = ctx.start.line
        start_label = self.cur_fun.name + "_" + str(ln) + '_start_while'
        end_label = self.cur_fun.name + "_" + str(ln) + '_end_while'
        self.code_generator.gen_enter_while1(start_label, end_label)

    def exitWhile_cond(self, ctx: VypParser.While_condContext):
        self.code_generator.gen_enter_while2()

    def exitWhile_stmt(self, ctx: VypParser.While_stmtContext):
        self.code_generator.gen_exit_while()

    @unary_op
    def exitNot_expr(self, ctx: VypParser.Not_exprContext):
        pass

    @unary_op
    def exitMinus_expr(self, ctx: VypParser.Minus_exprContext):
        pass

    def exitCast_expr(self, ctx: VypParser.Cast_exprContext):
        castType = ctx.var_type().getText()
        inner_expr = self.result[ctx.expr()]
        if castType in ['int', 'string']:
            if inner_expr.data_type == 'int' and castType == 'string':
                self.code_generator.cast_int_to_string()
            else:
                raise SemanticTypeError(f"Cannot cast {inner_expr.data_type} to {castType}")

            res_sym = Symbol('tmp', SymbolTypes.VAR, castType)
            self.result[ctx] = res_sym
        elif castType := self.class_symbols.get_symbol(castType):
            inner_expr_type = self.class_symbols.get_symbol(inner_expr.data_type);
            if not inner_expr_type.is_direct_parent(castType):
                raise SemanticTypeError(f"Cannot cast {inner_expr_type.name} to {castType}")
            self.result[ctx] = inner_expr # class is implicit
        else:
            raise SemanticTypeError(f"Unknown cast type {castType}")

    def exitInstance_creation_expr(self, ctx: VypParser.Instance_creation_exprContext):
        self.result[ctx] = self.result[ctx.instance_creation()]

    def exitBrace_expr(self, ctx: VypParser.Brace_exprContext):
        self.result[ctx] = self.result[ctx.expr()]

    def enterCode_block(self, ctx:VypParser.Code_blockContext):
        self.sym_table.push_scope()

    def exitCode_block(self, ctx:VypParser.Code_blockContext):
        self.sym_table.push_scope()
