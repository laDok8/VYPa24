from src.code_gen.function import Function
from src.code_gen.register import Register
from src.code_gen.stack import Stack
from src.sym_table import ClassSymbol


class ClassCodeGenerator:
    VMT_HEADER = 3  # VMT, parent, classname

    def __init__(self, cls: ClassSymbol):
        self.cls = cls

    def _get_field_offset(self, field_name: str):
        return self.cls.get_field_offset(field_name) + ClassCodeGenerator.VMT_HEADER

    def VMT(self):
        """VMT goes before functions"""
        _m = [m.name for m in self.cls.getVMT().values()]
        methods = self.cls.getVMT().keys()
        body = f'# VMT for {self.cls.name}\n'
        body += f'CREATE {Register.AX} {len(methods)}\n'
        for i, method in enumerate(methods):
            body += f'SETWORD {Register.AX} {i} "{method}"\n'

        body += f'{Stack.push(Register.AX)}\n\n'

        body += '\n'
        return body

    def create_instance(self, class_sym: ClassSymbol, vmts: list):
        """allocate memory for fields and VMT* and call constructor"""
        vmt_loc = vmts.index(class_sym)
        vmt_prt = vmts.index(class_sym.parent) if class_sym.parent else 0

        body = f'# new {self.cls.name}\n'
        # TODO: check field duplication?
        # VMT, prt, fields
        body += f'CREATE {Register.AX} {len(self.cls.get_all_fields()) + ClassCodeGenerator.VMT_HEADER}\n'
        body += f'SETWORD {Register.AX} 0 [{vmt_loc}]\n'
        body += f'SETWORD {Register.AX} 1 [{vmt_prt}]\n'
        body += f'SETWORD {Register.AX} 2 "{self.cls.name}"\n'
        # init fields to 0
        for i in range(1, len(self.cls.get_all_fields()) + ClassCodeGenerator.VMT_HEADER - 1):
            body += f'SETWORD {Register.AX} {i + 1} 0\n'
        body += '\n'

        """call constructors from outmost parent* to child - omit if default"""
        prts_const = []
        prt = class_sym
        while prt:
            cons = prt.get_constructor()
            if cons:
                prts_const.insert(0, cons)
            prt = prt.parent

        for cons in prts_const:
            f = Function(cons.name)
            body += f.call(ret_val=False)

        body += f'{Stack.push(Register.AX)}\n\n'
        return body

    def assign_field(self, field_name: str):
        body = f'# assign field {field_name}\n'
        body += f'SETWORD [{Register.SP}-1] {self._get_field_offset(field_name)} [{Register.SP}]\n'
        return body

    def field_expr(self, field):
        body = f'# field expr {field}\n'
        # TODO: cast index problem
        body += f'GETWORD {Register.EX}, [{Register.SP}], {self._get_field_offset(field)}\n'
        body += f'{Stack.replace(Register.EX)}\n\n'
        return body
