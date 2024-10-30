from src.sym_table import Symbol
from src.sym_table.symbol import SymbolTypes


class ClassSymbol(Symbol):
    """
    Represents a class
    """

    def __init__(self, name: str):
        super().__init__(name, SymbolTypes.CLASS, "foo")
        self.methods = {}
        self.fields = {}

    def add_method(self, method: Symbol):
        self.methods[method.name] = method

    def get_methods(self):
        return self.methods

    def get_method(self, name: str):
        return self.methods.get(name)

    def add_field(self, field: Symbol):
        self.fields[field.name] = field

    def get_fields(self):
        return self.fields

    def __str__(self):
        return f"class {self.name}({', '.join([str(arg) for arg in self.methods.values()])})"
