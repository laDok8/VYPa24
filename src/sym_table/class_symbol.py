from src.sym_table import Symbol
from src.sym_table.symbol import SymbolTypes


class ClassSymbol(Symbol):
    """
    Represents a class
    """

    def __init__(self, name: str, prt: None | Symbol):
        super().__init__(name, SymbolTypes.CLASS, "foo")
        self.name = name
        self.parent = prt
        self.methods = {}
        self.fields = {}

    def set_parent(self, parent: Symbol):
        """set at the end of the 1st pass"""
        self.parent = parent

    def add_method(self, method: Symbol):
        self.methods[method.name] = method

    def get_methods(self):
        return self.methods

    def getVMT(self) -> dict:
        # it's okay to have recursion_check just for fields
        self_methods = {f"{self.name}:{name}": symbol for name, symbol in self.methods.items()}

        if self.parent is None:
            return self_methods

        prt_methods = self.parent.getVMT()
        # prefer overridden methods
        return {**self_methods, **{nm: sym for nm, sym in prt_methods.items() if sym not in self_methods.values()}}

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
        fields.update(self.parent.get_all_fields(recursion_check + [self.name]))
        return fields

    def __str__(self):
        return f"class {self.name}({', '.join([str(arg) for arg in self.methods.values()])})"
