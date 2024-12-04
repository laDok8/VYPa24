'''
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
'''

import re

from src.code_gen.cls import ClassCodeGenerator
from src.code_gen.function import Function
from src.code_gen.if_else import IfElseGenerator
from src.code_gen.literal import Literal
from src.code_gen.register import Register
from src.code_gen.stack import Stack
from src.code_gen.static import Builtin
from src.compiler import SemanticDeclarationError
from src.sym_table import *


# WARN: for some reason, stack grows up
class CodeGenerator:
    """
    use modified cdecl calling convention
        args are pushed on stack from LTR, callee cleans up, return value on stack
     """

    def __init__(self):
        self.header = '''#! /bin/vypint
# VYPcode: 1.0
# Generated by xdokou14'''
        self.body = ''
        self.vmts = ''
        self.variables = []
        self.order_class_list = []
        # TODO: perhaps refactor to function class
        self.params = []
        self.if_else_stack = []
        self.cur_func = None
        self.cur_class_gen = None
        self.while_stack = []

    def get_var_offset(self, symbol: str) -> str:
        if symbol in self.variables:
            return '+' + str(self.variables.index(symbol) + 1)  # 0 is BP
        elif symbol in self.params:
            # in negative 0-BP, 1-PC, 3-arg1, 4-arg2, 5-arg3, (RTL) ...
            return str(-(self.params.index(symbol) + 2))
        else:
            raise SemanticDeclarationError(f"Variable {symbol} not found")

    def generate_code(self):
        self.body += Builtin.get_all_funs()
        self.prettifyOutput()
        print(self.header)
        print(Register.aliases())
        print(self.vmts)
        print("SET $BP $SP")
        print("CALL [$SP+1] main")
        print("JUMP _end\n\n")
        print("# User program")
        print(self.body)
        print("LABEL _end")

    def prettifyOutput(self):
        """add tabs"""

        lines = self.body.split('\n')
        result = []
        indent = False
        exclusion = r'(_end_while|_start_while|_else|_end)$'

        for line in lines:
            if line.strip().startswith("LABEL"):
                label_name = line.strip().split()[1]
                indent = True
                indent_self = re.search(exclusion, label_name)
                result.append(f'\t{line}' if indent_self else line)
            else:
                result.append(f'\t{line}' if indent else line)

        self.body = '\n'.join(result)

    def declaration(self, symbol: Symbol):
        _name = symbol.name
        self.variables.append(_name)
        _type = symbol.data_type
        self.body += f'# declare {_name}\n'
        self.body += f'SET [{Register.BP}{self.get_var_offset(_name)}] 0\n'
        self.body += f'{Stack.push()}\n\n'

    def fun_call(self, fun: FunctionSymbol, args: [Symbol]):
        f = Function(fun)

        if self.cur_class_gen:
            self.body += self.cur_class_gen.cls_fun_call(f, args)
        else:
            self.body += f.call(args)
        self.cur_func = f

    def literal(self, symbol: Symbol):
        if symbol.data_type == 'int':
            self.body += Literal.int_literal(symbol.name)
        else:
            self.body += Literal.string_literal(symbol.name)

    def restore_stack(self):
        _vars = len(self.variables)
        self.body += f'# restore stack\n'
        self.body += f'ADDI {Register.SP} {Register.BP} {_vars}\n\n'

    def function_def(self, fun_sym: FunctionSymbol):
        function = Function(fun_sym)
        self.body += function.define()

        # add params to stack
        for param in fun_sym.get_params():
            self.params.insert(0, param.name)
        self.cur_func = function  # beware im using this for both definition and call TO be refactored

    def exit_function(self):
        self.body += self.cur_func.exit()
        self.cur_func = None
        self.params = []
        self.variables = []

    def VMT(self, current_class: ClassSymbol):
        # here don't care ClassCodeGenerator
        cls_gen = ClassCodeGenerator(current_class)
        self.order_class_list.append(current_class)
        self.vmts += cls_gen.VMT()

    def create_instance(self, class_sym: ClassSymbol):
        # here don't care ClassCodeGenerator
        cls_gen = ClassCodeGenerator(class_sym)
        self.body += cls_gen.create_cls_instance(self.order_class_list)

    def assign_field(self, field):
        self.body += self.cur_class_gen.assign_cls_field(field)

    def push_object(self, first: str):
        ref = f'[{Register.BP}{self.get_var_offset(first)}]'

        self.body += f'# push object ref {first}\n'
        self.body += f'{Stack.push(ref)}\n'
        # self.body += f'PUSH [{Register.BP}{self.get_var_offset(first)}]\n\n'

    def assign_var(self, _id):
        self.body += f'# assign var {_id}\n'
        self.body += f'SET [{Register.BP}{self.get_var_offset(_id)}] [{Register.SP}]\n\n'

    def field_expr(self, field):
        self.body += self.cur_class_gen.field_expr_gen(field)

    def binary_op(self, op: str):
        op_map = {
            '+': 'ADDI',
            '-': 'SUBI',
            '*': 'MULI',
            '/': 'DIVI',
            '<': 'LTI',
            '>=': 'LTI',  # ! < # can't be done in single instruction
            '>': 'GTI',
            '<=': 'GTI',  # ! >
            '==': 'EQI',
            '!=': 'EQI',  # !  ==
            '&&': 'AND',
            '||': 'OR',
        }
        cur_op = op_map.get(op)

        self.body += f'# binary operation: {op}\n'
        self.body += f'{Stack.binary_op(cur_op)}\n\n'

        op_map2 = {
            '>=': '!',
            '<=': '!',
            '!=': '!',
        }
        cur_op = op_map2.get(op)
        if cur_op:
            self.unary_op(cur_op)

    def unary_op(self, op: str):
        op_map = {
            '!': 'NOT',
        }
        cur_op = op_map.get(op)

        self.body += f'# unary operation: {op}\n'
        self.body += f'{Stack.unary_op(cur_op)}\n\n'

    def ret_val(self, symb: Symbol):
        self.body += self.cur_func.exit_with_val(symb)
        pass

    def gen_enter_if(self, not_label, end_label):
        if_else_generator = IfElseGenerator(not_label, end_label)
        self.if_else_stack.append(if_else_generator)
        self.body += self.if_else_stack[-1].enter_if()

    def gen_enter_else(self):
        self.body += self.if_else_stack[-1].enter_else()

    def gen_exit_if_else(self):
        self.body += self.if_else_stack[-1].exit_if_else()
        self.if_else_stack.pop()

    def gen_enter_while1(self, start_label, end_label):
        self.while_stack.append((start_label, end_label))
        self.body += f'# while stmt\n'
        self.body += f'LABEL {start_label}\n'

    def gen_enter_while2(self):
        start_label, end_label = self.while_stack[-1]
        self.body += f'JUMPZ {end_label} [{Register.SP}]\n'

    def gen_exit_while(self):
        start_label, end_label = self.while_stack.pop()
        self.body += f'JUMP {start_label}\n'
        self.body += f'LABEL {end_label}\n'

    def ResetExprClass(self):
        self.cur_class_gen = None

    def push_expr(self, cls_sym, instance_name, copy_to_obj_reg=False):
        """push object reference and memorize class"""
        self.cur_class_gen = ClassCodeGenerator(cls_sym)
        self.push_object(instance_name)
        if copy_to_obj_reg:
            self.body += f'SET {Register.OBJ} [{Register.SP}]\n\n'
        # 2nd one is different
