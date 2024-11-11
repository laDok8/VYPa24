from src.code_gen.register import Register
from src.code_gen.stack import Stack


class Builtin:
    @staticmethod
    def read_string():
        return f'''
        LABEL readString
        READS {Register.AX}
        SET [{Register.SP}-1] {Register.AX}
        RETURN [{Register.SP}+1]
        '''

    @staticmethod
    def read_int():
        return f'''
        LABEL readInt
        READI {Register.AX}
        SET [{Register.SP}-1] {Register.AX}
        RETURN [{Register.SP}+1]
        '''

    @staticmethod
    def length():
        return f'''
        LABEL length
        GETSIZE {Register.AX} [{Register.SP}-2]
        {Stack.pop()}
        SET [{Register.SP}-1] {Register.AX}
        RETURN [{Register.SP}+1]
        '''
