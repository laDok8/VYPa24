from src.sym_table import Symbol, FunctionSymbol
from src.sym_table.symbol import SymbolTypes
from collections import OrderedDict



class ClassSymbol(Symbol):
    """
    Represents a class
    """

    def __init__(self, name: str, prt: None | Symbol):
        super().__init__(name, SymbolTypes.CLASS, "foo")
        self.name = name
        self.parent = prt
        self.methods = OrderedDict()
        self.fields = {}

    def set_parent(self, parent: Symbol):
        """set at the end of the 1st pass"""
        self.parent = parent

    def add_method(self, method: FunctionSymbol):
        self.methods[method.name] = method

    def get_methods(self):
        return self.methods

    def get_self_methods(self):
        return {nm.split(':')[-1]: sym for nm, sym in self.methods.items() if nm.startswith(self.name)}
        #return {nm: sym for nm, sym in self.methods.items() if nm.startswith(self.name)}

    def get_constructor(self):
        return self.get_methods().get(f'{self.name}:{self.name}')

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
        return self.methods.get(name)

    def add_field(self, field: Symbol):
        self.fields[field.name] = field

    def get_fields(self):
        return self.fields

    def get_all_fields(self, recursion_check=[]):
        if self.parent is None:
            return self.fields

        if self.name in recursion_check:
            raise ValueError("TODO: semantic error: Circular inheritance")

        fields = self.fields.copy()
        prt_fields = self.parent.get_all_fields(recursion_check + [self.name])
        fields = {**prt_fields, **fields}
        return fields

    def get_field_offset(self, field_name: str):
        fields = self.get_all_fields()
        return list(fields.keys()).index(field_name)

    def __str__(self):
        return f"class {self.name}({', '.join([str(arg) for arg in self.methods.values()])})"
