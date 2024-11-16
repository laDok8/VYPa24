# Generated from Vyp.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .VypParser import VypParser
else:
    from VypParser import VypParser

# This class defines a complete listener for a parse tree produced by VypParser.
class VypListener(ParseTreeListener):

    # Enter a parse tree produced by VypParser#program.
    def enterProgram(self, ctx:VypParser.ProgramContext):
        pass

    # Exit a parse tree produced by VypParser#program.
    def exitProgram(self, ctx:VypParser.ProgramContext):
        pass


    # Enter a parse tree produced by VypParser#function_def.
    def enterFunction_def(self, ctx:VypParser.Function_defContext):
        pass

    # Exit a parse tree produced by VypParser#function_def.
    def exitFunction_def(self, ctx:VypParser.Function_defContext):
        pass


    # Enter a parse tree produced by VypParser#var_type.
    def enterVar_type(self, ctx:VypParser.Var_typeContext):
        pass

    # Exit a parse tree produced by VypParser#var_type.
    def exitVar_type(self, ctx:VypParser.Var_typeContext):
        pass


    # Enter a parse tree produced by VypParser#ret_type.
    def enterRet_type(self, ctx:VypParser.Ret_typeContext):
        pass

    # Exit a parse tree produced by VypParser#ret_type.
    def exitRet_type(self, ctx:VypParser.Ret_typeContext):
        pass


    # Enter a parse tree produced by VypParser#f_param_list.
    def enterF_param_list(self, ctx:VypParser.F_param_listContext):
        pass

    # Exit a parse tree produced by VypParser#f_param_list.
    def exitF_param_list(self, ctx:VypParser.F_param_listContext):
        pass


    # Enter a parse tree produced by VypParser#f_call_list.
    def enterF_call_list(self, ctx:VypParser.F_call_listContext):
        pass

    # Exit a parse tree produced by VypParser#f_call_list.
    def exitF_call_list(self, ctx:VypParser.F_call_listContext):
        pass


    # Enter a parse tree produced by VypParser#f_param_def.
    def enterF_param_def(self, ctx:VypParser.F_param_defContext):
        pass

    # Exit a parse tree produced by VypParser#f_param_def.
    def exitF_param_def(self, ctx:VypParser.F_param_defContext):
        pass


    # Enter a parse tree produced by VypParser#code_block.
    def enterCode_block(self, ctx:VypParser.Code_blockContext):
        pass

    # Exit a parse tree produced by VypParser#code_block.
    def exitCode_block(self, ctx:VypParser.Code_blockContext):
        pass


    # Enter a parse tree produced by VypParser#statement.
    def enterStatement(self, ctx:VypParser.StatementContext):
        pass

    # Exit a parse tree produced by VypParser#statement.
    def exitStatement(self, ctx:VypParser.StatementContext):
        pass


    # Enter a parse tree produced by VypParser#declaration.
    def enterDeclaration(self, ctx:VypParser.DeclarationContext):
        pass

    # Exit a parse tree produced by VypParser#declaration.
    def exitDeclaration(self, ctx:VypParser.DeclarationContext):
        pass


    # Enter a parse tree produced by VypParser#var_assign.
    def enterVar_assign(self, ctx:VypParser.Var_assignContext):
        pass

    # Exit a parse tree produced by VypParser#var_assign.
    def exitVar_assign(self, ctx:VypParser.Var_assignContext):
        pass


    # Enter a parse tree produced by VypParser#instance_assign.
    def enterInstance_assign(self, ctx:VypParser.Instance_assignContext):
        pass

    # Exit a parse tree produced by VypParser#instance_assign.
    def exitInstance_assign(self, ctx:VypParser.Instance_assignContext):
        pass


    # Enter a parse tree produced by VypParser#ret_stmt.
    def enterRet_stmt(self, ctx:VypParser.Ret_stmtContext):
        pass

    # Exit a parse tree produced by VypParser#ret_stmt.
    def exitRet_stmt(self, ctx:VypParser.Ret_stmtContext):
        pass


    # Enter a parse tree produced by VypParser#if_else_stmt.
    def enterIf_else_stmt(self, ctx:VypParser.If_else_stmtContext):
        pass

    # Exit a parse tree produced by VypParser#if_else_stmt.
    def exitIf_else_stmt(self, ctx:VypParser.If_else_stmtContext):
        pass


    # Enter a parse tree produced by VypParser#if_cond.
    def enterIf_cond(self, ctx:VypParser.If_condContext):
        pass

    # Exit a parse tree produced by VypParser#if_cond.
    def exitIf_cond(self, ctx:VypParser.If_condContext):
        pass


    # Enter a parse tree produced by VypParser#else_stmt.
    def enterElse_stmt(self, ctx:VypParser.Else_stmtContext):
        pass

    # Exit a parse tree produced by VypParser#else_stmt.
    def exitElse_stmt(self, ctx:VypParser.Else_stmtContext):
        pass


    # Enter a parse tree produced by VypParser#while_stmt.
    def enterWhile_stmt(self, ctx:VypParser.While_stmtContext):
        pass

    # Exit a parse tree produced by VypParser#while_stmt.
    def exitWhile_stmt(self, ctx:VypParser.While_stmtContext):
        pass


    # Enter a parse tree produced by VypParser#while_cond.
    def enterWhile_cond(self, ctx:VypParser.While_condContext):
        pass

    # Exit a parse tree produced by VypParser#while_cond.
    def exitWhile_cond(self, ctx:VypParser.While_condContext):
        pass


    # Enter a parse tree produced by VypParser#id_expr.
    def enterId_expr(self, ctx:VypParser.Id_exprContext):
        pass

    # Exit a parse tree produced by VypParser#id_expr.
    def exitId_expr(self, ctx:VypParser.Id_exprContext):
        pass


    # Enter a parse tree produced by VypParser#cast_expr.
    def enterCast_expr(self, ctx:VypParser.Cast_exprContext):
        pass

    # Exit a parse tree produced by VypParser#cast_expr.
    def exitCast_expr(self, ctx:VypParser.Cast_exprContext):
        pass


    # Enter a parse tree produced by VypParser#instance_creation_expr.
    def enterInstance_creation_expr(self, ctx:VypParser.Instance_creation_exprContext):
        pass

    # Exit a parse tree produced by VypParser#instance_creation_expr.
    def exitInstance_creation_expr(self, ctx:VypParser.Instance_creation_exprContext):
        pass


    # Enter a parse tree produced by VypParser#invocation_expr.
    def enterInvocation_expr(self, ctx:VypParser.Invocation_exprContext):
        pass

    # Exit a parse tree produced by VypParser#invocation_expr.
    def exitInvocation_expr(self, ctx:VypParser.Invocation_exprContext):
        pass


    # Enter a parse tree produced by VypParser#mul_div_expr.
    def enterMul_div_expr(self, ctx:VypParser.Mul_div_exprContext):
        pass

    # Exit a parse tree produced by VypParser#mul_div_expr.
    def exitMul_div_expr(self, ctx:VypParser.Mul_div_exprContext):
        pass


    # Enter a parse tree produced by VypParser#rel_expr.
    def enterRel_expr(self, ctx:VypParser.Rel_exprContext):
        pass

    # Exit a parse tree produced by VypParser#rel_expr.
    def exitRel_expr(self, ctx:VypParser.Rel_exprContext):
        pass


    # Enter a parse tree produced by VypParser#not_expr.
    def enterNot_expr(self, ctx:VypParser.Not_exprContext):
        pass

    # Exit a parse tree produced by VypParser#not_expr.
    def exitNot_expr(self, ctx:VypParser.Not_exprContext):
        pass


    # Enter a parse tree produced by VypParser#add_sub_expr.
    def enterAdd_sub_expr(self, ctx:VypParser.Add_sub_exprContext):
        pass

    # Exit a parse tree produced by VypParser#add_sub_expr.
    def exitAdd_sub_expr(self, ctx:VypParser.Add_sub_exprContext):
        pass


    # Enter a parse tree produced by VypParser#and_expr.
    def enterAnd_expr(self, ctx:VypParser.And_exprContext):
        pass

    # Exit a parse tree produced by VypParser#and_expr.
    def exitAnd_expr(self, ctx:VypParser.And_exprContext):
        pass


    # Enter a parse tree produced by VypParser#brace_expr.
    def enterBrace_expr(self, ctx:VypParser.Brace_exprContext):
        pass

    # Exit a parse tree produced by VypParser#brace_expr.
    def exitBrace_expr(self, ctx:VypParser.Brace_exprContext):
        pass


    # Enter a parse tree produced by VypParser#or_expr.
    def enterOr_expr(self, ctx:VypParser.Or_exprContext):
        pass

    # Exit a parse tree produced by VypParser#or_expr.
    def exitOr_expr(self, ctx:VypParser.Or_exprContext):
        pass


    # Enter a parse tree produced by VypParser#literal_expr.
    def enterLiteral_expr(self, ctx:VypParser.Literal_exprContext):
        pass

    # Exit a parse tree produced by VypParser#literal_expr.
    def exitLiteral_expr(self, ctx:VypParser.Literal_exprContext):
        pass


    # Enter a parse tree produced by VypParser#eq_expr.
    def enterEq_expr(self, ctx:VypParser.Eq_exprContext):
        pass

    # Exit a parse tree produced by VypParser#eq_expr.
    def exitEq_expr(self, ctx:VypParser.Eq_exprContext):
        pass


    # Enter a parse tree produced by VypParser#fun_call_expr.
    def enterFun_call_expr(self, ctx:VypParser.Fun_call_exprContext):
        pass

    # Exit a parse tree produced by VypParser#fun_call_expr.
    def exitFun_call_expr(self, ctx:VypParser.Fun_call_exprContext):
        pass


    # Enter a parse tree produced by VypParser#fun_call.
    def enterFun_call(self, ctx:VypParser.Fun_callContext):
        pass

    # Exit a parse tree produced by VypParser#fun_call.
    def exitFun_call(self, ctx:VypParser.Fun_callContext):
        pass


    # Enter a parse tree produced by VypParser#instance_creation.
    def enterInstance_creation(self, ctx:VypParser.Instance_creationContext):
        pass

    # Exit a parse tree produced by VypParser#instance_creation.
    def exitInstance_creation(self, ctx:VypParser.Instance_creationContext):
        pass


    # Enter a parse tree produced by VypParser#literal_val.
    def enterLiteral_val(self, ctx:VypParser.Literal_valContext):
        pass

    # Exit a parse tree produced by VypParser#literal_val.
    def exitLiteral_val(self, ctx:VypParser.Literal_valContext):
        pass


    # Enter a parse tree produced by VypParser#first_instance_ref.
    def enterFirst_instance_ref(self, ctx:VypParser.First_instance_refContext):
        pass

    # Exit a parse tree produced by VypParser#first_instance_ref.
    def exitFirst_instance_ref(self, ctx:VypParser.First_instance_refContext):
        pass


    # Enter a parse tree produced by VypParser#instance_expr.
    def enterInstance_expr(self, ctx:VypParser.Instance_exprContext):
        pass

    # Exit a parse tree produced by VypParser#instance_expr.
    def exitInstance_expr(self, ctx:VypParser.Instance_exprContext):
        pass


    # Enter a parse tree produced by VypParser#nested_invocation.
    def enterNested_invocation(self, ctx:VypParser.Nested_invocationContext):
        pass

    # Exit a parse tree produced by VypParser#nested_invocation.
    def exitNested_invocation(self, ctx:VypParser.Nested_invocationContext):
        pass


    # Enter a parse tree produced by VypParser#class_def.
    def enterClass_def(self, ctx:VypParser.Class_defContext):
        pass

    # Exit a parse tree produced by VypParser#class_def.
    def exitClass_def(self, ctx:VypParser.Class_defContext):
        pass


    # Enter a parse tree produced by VypParser#class_field.
    def enterClass_field(self, ctx:VypParser.Class_fieldContext):
        pass

    # Exit a parse tree produced by VypParser#class_field.
    def exitClass_field(self, ctx:VypParser.Class_fieldContext):
        pass


    # Enter a parse tree produced by VypParser#class_method.
    def enterClass_method(self, ctx:VypParser.Class_methodContext):
        pass

    # Exit a parse tree produced by VypParser#class_method.
    def exitClass_method(self, ctx:VypParser.Class_methodContext):
        pass



del VypParser