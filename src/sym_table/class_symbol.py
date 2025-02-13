"""
project: VYPlanguage Compiler
author: Ladislav Dokoupil - xdokou14
"""

from collections import OrderedDict

from compiler.exceptions import SemanticDeclarationError
from sym_table.function_symbol import FunctionSymbol
from sym_table.symbol import SymbolTypes,Symbol


class ClassSymbol(Symbol):
    """
    Represents a class
    """

    def __init__(self, name: str, prt: None | Symbol):
        super().__init__(name, SymbolTypes.CLASS, name)
        self.name = name
        self.parent = prt
        self.methods = OrderedDict()
        self.fields = {}

    def set_parent(self, parent: Symbol):
        """set at the end of the 1st pass"""
        self.parent = parent

    def add_method(self, method: FunctionSymbol):
        self.methods[method.name] = method
        method.update_code_name(f'{self.name}:{method.name}')

    def get_self_methods(self):
        return self.methods

    def has_direct_parent(self, other: Symbol) -> bool:
        tmp = self
        while tmp is not None:
            if tmp == other:
                return True
            tmp = tmp.parent
        return False

    def get_constructor(self):
        return self.get_self_methods().get(self.name)

    def getVMT(self) -> dict:
        """only from this class and without prefix"""
        self_methods = self.methods.copy()

        if self.parent is None:
            return self_methods

        prt_methods = self.parent.getVMT()

        # prefer overridden methods
        for s in list(self_methods):
            for p in list(prt_methods):
                if self_methods[s].eq(prt_methods[p]):
                    prt_methods[p] = self_methods.pop(s)
                    break

        prt_methods.update(self_methods)
        return prt_methods

    def get_method(self, name: str):
        """returns method if available from current context"""
        return self.getVMT().get(name)

    def add_field(self, field: Symbol):
        self.fields[field.name] = field

    def get_fields(self):
        return self.fields

    def get_all_fields(self, recursion_check=[]):
        if self.parent is None:
            return self.fields

        if self.name in recursion_check:
            raise SemanticDeclarationError("Circular inheritance")

        fields = self.fields.copy()
        prt_fields = self.parent.get_all_fields(recursion_check + [self.name])
        fields = {**prt_fields, **fields}
        return fields

    def get_field(self, field_name: str):
        return self.get_all_fields().get(field_name)

    def get_field_offset(self, field_name: str):
        fields = self.get_all_fields()
        return list(fields.keys()).index(field_name)

    def __str__(self):
        return f"class {self.name}({', '.join([str(arg) for arg in self.methods.values()])})"
