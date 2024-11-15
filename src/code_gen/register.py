class Register:
    SP = '$SP'
    BP = '$BP'  # - 0
    AX = '$AX'  # return values, arithmetics
    BX = '$BX'  # index
    CX = '$CX'  # iterator
    DX = '$DX'  # I/O & AX extension div/mul ?
    EX = '$EX'  # misc
    SI = '$SI'  # string src
    DI = '$DI'  # string dest

    @staticmethod
    def aliases():
        return f'''
ALIAS BP $0
ALIAS AX $1
ALIAS BX $2
ALIAS CX $3
ALIAS DX $4
ALIAS EX $5
ALIAS SI $6
ALIAS DI $7\n'''
