import re

from src.code_gen.cls import ClassCodeGenerator
from src.code_gen.function import Function
from src.code_gen.literal import Literal
from src.code_gen.register import Register
from src.code_gen.stack import Stack
from src.sym_table import Symbol, ClassSymbol


# WARN: for some reason, stack grows up

class CodeGenerator:
    """
    use modified cdecl calling convention
        args are pushed on stack from RTL, caller cleans up, return value on stack
     """

    def __init__(self):
        self.header = '''#! /bin/vypint
# VYPcode: 1.0
# Generated by xdokou14'''
        self.body = ''
        self.variables = []
        self.classes = []

    def get_var_offset(self, symbol: str):
        return self.variables.index(symbol) + 1 # 0 is BP

    def generate_code(self):
        self.prettifyOutput()
        print(self.header)
        print(Register.aliases())
        print("SET $BP $SP")
        print("CALL [$SP+1] main")
        print("JUMP _end\n")
        print(self.body)
        print("LABEL _end")

    def prettifyOutput(self):
        """add tabs"""

        def add_tabs(match):
            lines = match.group(0).split('\n')
            return '\n' + lines[0] + '\n' + '\n'.join('\t' + line if line else line for line in lines[1:])

        self.body = re.sub(r'LABEL.*?(?=LABEL|$)', add_tabs, self.body, flags=re.DOTALL)

    def declaration(self, symbol: Symbol):
        _name = symbol.name
        self.variables.append(_name)
        _type = symbol.data_type
        self.body += f'# declare {_name}\n'
        self.body += f'SET [{Register.BP}+{self.get_var_offset(_name)}] 0\n'
        self.body += f'{Stack.push()}\n\n'

    def fun_call(self, fname: str, args: [Symbol]):
        f = Function(fname)
        self.body += f.call(args)

    def literal(self, symbol: Symbol):
        if symbol.data_type == 'int':
            self.body += Literal.int_literal(symbol.name)
        else:
            self.body += Literal.string_literal(symbol.name)

    def restore_stack(self):
        _vars = len(self.variables)
        self.body += f'# restore stack\n'
        self.body += f'ADDI {Register.SP} {Register.BP} {_vars}\n\n'

    def function_def(self, fun_name):
        function = Function(fun_name)
        self.body += function.define()

    def exit_function(self):
        self.body += Function.exit()

    def VMT(self, current_class: ClassSymbol):
        cls_gen = ClassCodeGenerator(current_class)
        self.classes.append(current_class)
        self.body += cls_gen.VMT()

    def create_instance(self, class_sym: ClassSymbol):
        cls_gen = ClassCodeGenerator(class_sym)
        self.body += cls_gen.create_instance(class_sym, self.classes)

    def assign_field(self, cls_sym, field):
        cls_gen = ClassCodeGenerator(cls_sym)
        self.body += cls_gen.assign_field(field)

    def push_object(self, first: str):
        ref = f'[{Register.BP}+{self.get_var_offset(first)}]'

        self.body += f'# push object ref {first}\n'
        self.body += f'{Stack.push(ref)}\n\n'
        # self.body += f'PUSH [{Register.BP}+{self.get_var_offset(first)}]\n\n'

    def assign_var(self, _id):
        self.body += f'# assign var {_id}\n'
        self.body += f'SET [{Register.BP}+{self.get_var_offset(_id)}] [{Register.SP}]\n\n'

    def field_expr(self, cls_sym, field):
        cls_gen = ClassCodeGenerator(cls_sym)
        self.body += cls_gen.field_expr(field)

    def binary_op(self, op: str):
        map = {
            '+': 'ADDI',
            '-': 'SUBI',
            '*': 'MULI',
            '/': 'DIVI',
            '<': 'LTI',
            '>': 'GTI',
            '=': 'EQI',
            '<': 'LTS',
            '>': 'GTS',
            '==': 'EQS',
            '&&': 'AND',
            '||': 'OR',
        }
        _op = map[op]
        # TODO: exceptions for >=, <=, !=

        self.body += f'# binary operation: {op}\n'
        self.body += f'{Stack.binary_op(_op)}\n\n'

    def ret_val(self, sym):
        self.body += f'# return value\n'
        # set return value below bp  ( PC is also ther)
        self.body += f'SET [{Register.BP}-2] [{Register.SP}]\n'
        self.body += f'{Stack.leave()}\n\n'
        pass
