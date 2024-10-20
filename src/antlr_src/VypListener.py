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


    # Enter a parse tree produced by VypParser#data_type.
    def enterData_type(self, ctx:VypParser.Data_typeContext):
        pass

    # Exit a parse tree produced by VypParser#data_type.
    def exitData_type(self, ctx:VypParser.Data_typeContext):
        pass


    # Enter a parse tree produced by VypParser#param_list.
    def enterParam_list(self, ctx:VypParser.Param_listContext):
        pass

    # Exit a parse tree produced by VypParser#param_list.
    def exitParam_list(self, ctx:VypParser.Param_listContext):
        pass


    # Enter a parse tree produced by VypParser#param.
    def enterParam(self, ctx:VypParser.ParamContext):
        pass

    # Exit a parse tree produced by VypParser#param.
    def exitParam(self, ctx:VypParser.ParamContext):
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


    # Enter a parse tree produced by VypParser#assignment.
    def enterAssignment(self, ctx:VypParser.AssignmentContext):
        pass

    # Exit a parse tree produced by VypParser#assignment.
    def exitAssignment(self, ctx:VypParser.AssignmentContext):
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


    # Enter a parse tree produced by VypParser#while_stmt.
    def enterWhile_stmt(self, ctx:VypParser.While_stmtContext):
        pass

    # Exit a parse tree produced by VypParser#while_stmt.
    def exitWhile_stmt(self, ctx:VypParser.While_stmtContext):
        pass


    # Enter a parse tree produced by VypParser#expr.
    def enterExpr(self, ctx:VypParser.ExprContext):
        pass

    # Exit a parse tree produced by VypParser#expr.
    def exitExpr(self, ctx:VypParser.ExprContext):
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


    # Enter a parse tree produced by VypParser#fun_call_head.
    def enterFun_call_head(self, ctx:VypParser.Fun_call_headContext):
        pass

    # Exit a parse tree produced by VypParser#fun_call_head.
    def exitFun_call_head(self, ctx:VypParser.Fun_call_headContext):
        pass


    # Enter a parse tree produced by VypParser#literal_val.
    def enterLiteral_val(self, ctx:VypParser.Literal_valContext):
        pass

    # Exit a parse tree produced by VypParser#literal_val.
    def exitLiteral_val(self, ctx:VypParser.Literal_valContext):
        pass


    # Enter a parse tree produced by VypParser#class_def.
    def enterClass_def(self, ctx:VypParser.Class_defContext):
        pass

    # Exit a parse tree produced by VypParser#class_def.
    def exitClass_def(self, ctx:VypParser.Class_defContext):
        pass


    # Enter a parse tree produced by VypParser#class_member.
    def enterClass_member(self, ctx:VypParser.Class_memberContext):
        pass

    # Exit a parse tree produced by VypParser#class_member.
    def exitClass_member(self, ctx:VypParser.Class_memberContext):
        pass



del VypParser