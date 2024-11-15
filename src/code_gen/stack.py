from src.code_gen.register import Register

class Stack:
    @staticmethod
    def push(x=None):
        if x is None:
            return f'ADDI {Register.SP}, {Register.SP}, 1'
        else:
            return f'''ADDI {Register.SP}, {Register.SP}, 1
SET [{Register.SP}] {x}'''

    @staticmethod
    def pop(x=None):
        if x is None:
            return f'SUBI {Register.SP}, {Register.SP}, 1'
        else:
            return f'''SET {x} [{Register.SP}]
SUBI {Register.SP}, {Register.SP}, 1'''

    @staticmethod
    def leave():
        """leave function (reset SP, BP, return)"""
        return f'''SET {Register.SP} {Register.BP}
{Stack.pop(Register.BP)}
{Stack.pop()}
RETURN [{Register.SP}+1]'''

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
        return f'''{op} {Register.AX} [{Register.SP}] [{Register.SP}-1]\n
{Stack.pop()}
{Stack.replace(Register.AX)}'''
