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
            Builtin.getClass()
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
ADDI {Register.SP} {Register.SP} 2
SET [{Register.SP}] {Register.BP}
SET {Register.BP} {Register.SP}
#[BP-2] = n, [BP-3] = i, [BP-4] = str
SET $BX [{Register.BP}-3] # i

GETSIZE {Register.AX} [{Register.BP}-4]
LTI {Register.EX} {Register.BX} 0
GTI {Register.OBJ} {Register.BX} {Register.AX}
OR {Register.EX} {Register.EX} {Register.OBJ} # i < 0 || i > size

CREATE {Register.DI} 1
SETWORD {Register.DI} 0 ""
JUMPNZ subStr_end {Register.EX}

RESIZE {Register.DI} [{Register.BP}-2]

SET {Register.EX} [{Register.BP}-2]
ADDI {Register.EX} {Register.EX} {Register.BX} # n + i

GTI {Register.CX} {Register.EX} {Register.AX} # n + i > size
JUMPNZ subStr_min_else {Register.CX}
JUMP subStr_min_end # n + 1 <= size
LABEL subStr_min_else # n + i > size
SET {Register.EX} [{Register.BP}-4]
LABEL subStr_min_end
#SUBI {Register.EX} {Register.EX} 1
ADDI {Register.SP} {Register.SP} 1
SET [{Register.SP}] {Register.EX} # [{Register.SP}]=min(n+i,len(str))- 1


SET {Register.AX} 0 #index new
#SET {Register.BX} {Register.BX} #index old
LABEL subStr_start_while
LTI {Register.EX} {Register.BX} [{Register.SP}] # i < n+i-1
JUMPZ subStr_end {Register.EX}


GETWORD {Register.EX} [{Register.BP}-4] {Register.BX} # EX=[{Register.BP}-4][{Register.BX}] - char from SI

SETWORD {Register.DI} {Register.AX} {Register.EX} # rewrite char

ADDI {Register.AX} {Register.AX} 1
ADDI {Register.BX} {Register.BX} 1
JUMP subStr_start_while


LABEL subStr_end
# exit function
SET {Register.SP} {Register.BP}
SET {Register.BP} [{Register.SP}]
SUBI {Register.SP}, {Register.SP}, 4
SET [{Register.SP}] {Register.DI}
RETURN [{Register.SP}+3]\n\n'''

    @staticmethod
    def toString():
        return f'''LABEL Object:toString
INT2STRING {Register.AX} [{Register.SP}]
SET [{Register.SP}] {Register.AX}
RETURN [{Register.SP}]\n\n'''

    @staticmethod
    def getClass():
        return f'''LABEL Object:getClass
GETWORD {Register.AX} [{Register.SP}] 2
SET [{Register.SP}] {Register.AX}
RETURN [{Register.SP}+1]\n\n'''

# TODO: concatenate_strings
