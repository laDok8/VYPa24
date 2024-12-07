"""
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
"""

from code_gen.register import Register


class Stack:
    @staticmethod
    def push(x=None):
        if x is None:
            return f'ADDI {Register.SP} {Register.SP} 1'
        else:
            return f'''ADDI {Register.SP} {Register.SP} 1
SET [{Register.SP}] {x}'''

    @staticmethod
    def pop(x=None):
        if x is None:
            return f'SUBI {Register.SP} {Register.SP} 1'
        else:
            return f'''SET {x} [{Register.SP}]
SUBI {Register.SP} {Register.SP} 1'''

    @staticmethod
    def pops(x: int):
        return f'SUBI {Register.SP} {Register.SP} {x}'

    @staticmethod
    def leave(pops: int):
        """leave function (reset SP, BP, return)"""
        sp_loc = pops + 1

        body = f'SET {Register.SP} {Register.BP}\n'
        body += f'{Stack.pop(Register.BP)}\n'
        body += f'{Stack.pops(pops)}\n'
        body += f'RETURN [{Register.SP}+{sp_loc - 1}]\n'
        return body

    @staticmethod
    def enter():
        """enter function (save BP, SP, PC)"""
        return f'''{Stack.push()} # space for PC
{Stack.push(Register.BP)}
SET {Register.BP} {Register.SP}'''

    @staticmethod
    def replace(x):
        return f'SET [{Register.SP}] {x}'

    @staticmethod
    def binary_op(op: str):
        """values and res on stack"""
        return f'''{op} {Register.AX} [{Register.SP}-1] [{Register.SP}]\n
{Stack.pop()}
{Stack.replace(Register.AX)}'''

    @staticmethod
    def unary_op(op: str):
        return f'''{op} {Register.AX} [{Register.SP}]\n
{Stack.replace(Register.AX)}'''
