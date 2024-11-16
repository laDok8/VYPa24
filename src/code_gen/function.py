from src.code_gen.register import Register
from src.code_gen.stack import Stack
from src.sym_table import Symbol, FunctionSymbol


class Function:
    def __init__(self, func: FunctionSymbol):
        self.f_name = func.name
        self.args = func.get_params()  # store param count/name/types

    def define(self):
        body = f'LABEL {self.f_name}\n'
        body += f'{Stack.enter()}\n'
        return body

    def exit(self):
        len_args = len(self.args)
        body = f'# exit function\n'
        body += f'{Stack.leave(len_args)}\n'
        return body

    @staticmethod
    def _print(symbol: [Symbol]):
        body = f'# print\n'

        for acc, s in enumerate(symbol, -len(symbol) + 1):
            acc = '' if acc == 0 else acc
            if s.data_type == 'int':
                body += f'WRITEI [{Register.SP}{acc}]\n'
            else:
                body += f'WRITES [{Register.SP}{acc}]\n'
        return body

    def call(self, args: [Symbol] = []):
        if self.f_name == 'print':
            return Function._print(args)

        body = f'# function call {self.f_name}\n'
        if not args:  # usually we overwrite deepest stack val
            body += f'{Stack.push()} # space for return value\n'
        body += f'CALL [{Register.SP}+1] {self.f_name}\n\n'
        return body

    def exit_with_val(self, symb: Symbol):
        body = f'# return value\n'
        # overwrite arg0 with retval
        ret_symb = str(0) if symb is None else Register.SP
        len_args = len(self.args)

        offset = str(-1 - len(self.args)) if len(self.args) != 0 else str(-2 - len(self.args))  # below  PC, args
        body += f'SET [{Register.BP}{offset}] [{ret_symb}]\n'
        body += f'{Stack.leave(len_args)}\n\n'
        return body
