"""
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
"""

from code_gen.function import Function
from code_gen.register import Register
from code_gen.stack import Stack
from sym_table.class_symbol import ClassSymbol


class ClassCodeGenerator:
    VMT_HEADER = 3  # VMT, parent, classname

    def __init__(self, cls: ClassSymbol):
        self.cls = cls

    def _get_field_offset(self, field_name):
        return self.cls.get_field_offset(field_name.name) + ClassCodeGenerator.VMT_HEADER

    def VMT(self):
        """VMT goes before functions"""
        _m = [m.name for m in self.cls.getVMT().values()]
        methods = self.cls.getVMT().keys()
        body = f'# VMT for {self.cls.name}\n'
        body += f'CREATE {Register.AX} {len(methods)}\n'
        for i, method in enumerate(methods):
            body += f'SETWORD {Register.AX} {i} "{self.cls.getVMT().get(method).name}"\n'

        # exception so we start from 0
        body += f'{Stack.replace(Register.AX)}\n'
        body += f'{Stack.push()}\n'

        body += '\n'
        return body

    def create_cls_instance(self, ordered_classes_all: list):
        """allocate memory for fields and VMT* and call constructor"""

        vmt_loc = ordered_classes_all.index(self.cls)
        vmt_prt = ordered_classes_all.index(self.cls.parent) if self.cls.parent else 0

        body = f'# new {self.cls.name}\n'
        # VMT, prt, fields
        body += f'CREATE {Register.AX} {len(self.cls.get_all_fields()) + ClassCodeGenerator.VMT_HEADER}\n'
        body += f'SETWORD {Register.AX} 0 [{vmt_loc}]\n'
        body += f'SETWORD {Register.AX} 1 [{vmt_prt}]\n'
        body += f'SETWORD {Register.AX} 2 "{self.cls.name}"\n'
        # init fields to 0
        for i, field in enumerate(self.cls.get_all_fields().values(), start=2):
            def_val = '0' if field.data_type == 'int' else '""'
            body += f'SETWORD {Register.AX} {i + 1} {def_val}\n'
        # available as self param for constructors
        body += f'{Stack.push(Register.AX)}\n\n'

        """call constructors from outmost parent* to child - omit if default"""
        prts_const = []
        prt = self.cls
        while prt:
            cons = prt.get_constructor()
            if cons:
                prts_const.insert(0, cons)
            prt = prt.parent

        for cons in prts_const:
            f = Function(cons)
            body += f.call(["no_space_retval"])

        return body

    def assign_cls_field(self, field_name: str):
        body = f'# assign field {field_name}\n'
        body += f'SETWORD [{Register.SP}-1] {self._get_field_offset(field_name)} [{Register.SP}]\n'
        body += f'{Stack.pops(2)}\n\n'
        return body

    def field_expr_gen(self, field):
        """get field ref to stack"""
        body = f'# field expr {field}\n'
        body += f'GETWORD {Register.EX} [{Register.SP}] {self._get_field_offset(field)}\n'
        body += f'{Stack.replace(Register.EX)}\n\n'
        return body

    def cls_fun_call(self, fun: Function, super_call):
        # cls fun is called via VMT reference, 1st argument is always class, like python self
        # assume current object is in {Register.OBJ}
        body = f'# class function call {fun.f_name}\n'
        method_name = fun.f_name.split(":")[1]
        method_idx = list(self.cls.getVMT().keys()).index(method_name)

        relevant_vmt = 1 if super_call else 0

        # no need for space for return value, we can overwrite obj
        body += f'GETWORD {Register.AX} {Register.OBJ} {relevant_vmt} # GET VMT\n'
        body += f'GETWORD {Register.AX} {Register.AX} {method_idx} # GET DYNAMIC FUN REF\n'
        body += f'CALL [{Register.SP}+1] {Register.AX} # CALL DYNAMIC FUN\n\n'
        return body
