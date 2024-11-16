from src.code_gen.register import Register
from src.code_gen.stack import Stack


class IfElseGenerator:
    """ else is optional and gets paired to nearest if """

    def __init__(self, not_label, end_label):
        self.not_label = not_label
        self.end_label = end_label
        self.else_generated = False

    def enter_if(self):
        body = f'# if_else\n'
        body += f'{Stack.pop(Register.AX)}\n'
        body += f'JUMPZ {self.not_label} {Register.AX}\n'
        return body

    def enter_else(self):
        self.else_generated = True
        body = f'JUMP {self.end_label}\n'
        body += f'LABEL {self.not_label}\n'
        return body

    def exit_if_else(self):
        if self.else_generated:
            return f'LABEL {self.end_label}\n'
        else:
            return f'LABEL {self.not_label}\n'
