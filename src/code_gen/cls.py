from src.code_gen.register import Register
from src.code_gen.stack import Stack
from src.sym_table import ClassSymbol


class ClassCodeGenerator:
    def __init__(self, cls: ClassSymbol):
        self.cls = cls

    def VMT(self):
        """VMT goes before functions"""
        methods = self.cls.getVMT().keys()
        body = f'# VMT for {self.cls.name}\n'
        body += f'CREATE {Register.AX} {len(methods)}\n'
        for i, method in enumerate(methods):
            body += f'SETWORD {Register.AX} {i} "{method}"\n'

        body += f'{Stack.push(Register.AX)}\n\n'

        # TODO: need to store it as "variable" as it's on stack
        body += '\n'
        return body
