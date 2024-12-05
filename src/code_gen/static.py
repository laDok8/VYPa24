'''
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
'''

from src.code_gen.register import Register


class Builtin:
    @staticmethod
    def get_all_funs():
        functions = [
            Builtin.read_string(),
            Builtin.read_int(),
            Builtin.length(),
            Builtin.subStr(),
            Builtin.toString(),
            Builtin.getClass(),
            Builtin.concat()
        ]
        return ''.join(functions)

    @staticmethod
    def read_string():
        return f'''LABEL readString
READS {Register.AX}
SET [{Register.SP}] {Register.AX}
RETURN [{Register.SP}+1]\n\n'''

    @staticmethod
    def read_int():
        return f'''LABEL readInt
READI {Register.AX}
SET [{Register.SP}] {Register.AX}
RETURN [{Register.SP}+1]\n\n'''

    @staticmethod
    def length():
        return f'''LABEL length
GETSIZE {Register.AX} [{Register.SP}]
SET [{Register.SP}] {Register.AX}
RETURN [{Register.SP}+1]\n\n'''



    @staticmethod
    def subStr():
        return f'''LABEL subStr
#[{Register.SP}] = n, [{Register.SP}-1] = i, [{Register.SP}-2] = str
CREATE {Register.DI} 1
SETWORD {Register.DI} 0 ""
GETWORD {Register.DI} {Register.DI} 0

LTI {Register.AX} [{Register.SP}-1] 0
JUMPNZ subStr_end {Register.AX}
LTI {Register.AX} [{Register.SP}] 0
JUMPNZ subStr_end {Register.AX}
GETSIZE {Register.AX} [{Register.SP}-2]
LTI {Register.EX} [{Register.SP}-1] {Register.AX}
NOT {Register.EX} {Register.EX}
JUMPNZ subStr_end {Register.EX}

ADDI {Register.EX} [{Register.SP}-1] [{Register.SP}] # n + i
GETSIZE {Register.AX} [{Register.SP}-2]
GTI {Register.CX} {Register.EX} {Register.AX} # n + i > SI.length()
JUMPZ subStr_min_end {Register.CX}
SUBI {Register.EX} {Register.AX} [{Register.SP}-1] # n = SI.length() - i
SET [{Register.SP}] {Register.EX}
LABEL subStr_min_end

CREATE {Register.DI} [{Register.SP}]

SET {Register.CX} 0
SET {Register.BX} [{Register.SP}-1]
LABEL subStr_start_while
LTI {Register.EX} {Register.CX} [{Register.SP}] # i < n
JUMPZ subStr_end {Register.EX}

GETWORD {Register.AX} [{Register.SP}-2] {Register.BX} # char from SI
SETWORD {Register.DI} {Register.CX} {Register.AX} # rewrite char

ADDI {Register.CX} {Register.CX} 1
ADDI {Register.BX} {Register.BX} 1
JUMP subStr_start_while

LABEL subStr_end
SUBI {Register.SP} {Register.SP} 2
SET [{Register.SP}] {Register.DI}
RETURN [{Register.SP}+3]
'''

    @staticmethod
    def toString():
        return f'''LABEL Object:toString
INT2STRING {Register.AX} [{Register.SP}]
SET [{Register.SP}] {Register.AX}
RETURN [{Register.SP}+1]\n\n'''

    @staticmethod
    def getClass():
        return f'''LABEL Object:getClass
GETWORD {Register.AX} [{Register.SP}] 2
SET [{Register.SP}] {Register.AX}
RETURN [{Register.SP}+1]\n\n'''

    @classmethod
    def concat(cls):
        return f'''LABEL __str_concat__
# {Register.BX}=len(left), {Register.EX}=len(right)
# {Register.AX}={Register.BX}+{Register.EX}
# {Register.DI}=copy(left)
# {Register.DI}=resize({Register.DI},{Register.AX})

SUBI {Register.SP} {Register.SP} 1
GETSIZE {Register.BX} [{Register.SP}]
GETSIZE {Register.EX} [{Register.SP} + 1]
COPY {Register.DI} [{Register.SP}]
ADDI {Register.AX} {Register.BX} {Register.EX}
RESIZE {Register.DI} {Register.AX}
SET {Register.CX} 0

# for {Register.CX}=0,{Register.BX}=len(left); {Register.CX}<{Register.EX}; {Register.CX}++,{Register.BX}++
# {Register.DI}[{Register.BX}]=$right[{Register.CX}]

LABEL __str_concat__loop
LTI {Register.AX} {Register.CX} {Register.EX}
JUMPZ __str_concat__end {Register.AX}

GETWORD {Register.SI} [{Register.SP}+1] {Register.CX}
SETWORD {Register.DI} {Register.BX} {Register.SI}

ADDI {Register.BX} {Register.BX} 1
ADDI {Register.CX} {Register.CX} 1
JUMP __str_concat__loop
LABEL __str_concat__end

# return {Register.DI}
SET [{Register.SP}] {Register.DI}
RETURN [{Register.SP}+2]\n\n'''
