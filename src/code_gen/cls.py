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

        body += '\n'
        return body

    def create_instance(self, VMT_loc: int):
        """allocate memory for fields and VMT*"""
        body = f'# create instance of {self.cls.name}\n'
        # TODO: check field duplication?
        body += f'CREATE {Register.AX} {len(self.cls.get_all_fields()) + 1}\n'
        body += f'SETWORD {Register.AX} 0 [{VMT_loc}]\n'
        # init fields to 0
        for i in range(len(self.cls.get_all_fields())):
            body += f'SETWORD {Register.AX} {i + 1} 0\n'
        body += f'{Stack.push(Register.AX)}\n\n'
        return body
