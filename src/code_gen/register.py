class Register:
    SP = '$SP'
    BP = '$BP'
    AX = '$AX'
    BX = '$BX'
    CX = '$CX'
    DX = '$DX'
    EX = '$EX'
    SI = '$SI'
    DI = '$DI'

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
