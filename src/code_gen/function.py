from src.code_gen.register import Register
from src.code_gen.stack import Stack
from src.sym_table import Symbol


class Function:
    def __init__(self, f_name: str):
        self.f_name = f_name

    def define(self):
        body = f'LABEL {self.f_name}\n'
        body += f'{Stack.enter()}\n'
        return body

    @staticmethod
    def exit():
        body = f'# exit function\n'
        body += f'{Stack.leave()}\n'
        return body

    def _print(self, symbol: [Symbol]):
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
            return self._print(args)

        body = f'# function call {self.f_name}\n'
        body += f'{Stack.push()} # space for return value\n'
        body += f'CALL [{Register.SP}+1] {self.f_name}\n\n'
        return body
