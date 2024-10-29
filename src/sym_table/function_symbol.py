from src.sym_table.symbol import SymbolTypes, Symbol


class FunctionSymbol(Symbol):
    """
    Represents a function
    """

    def __init__(self, name: str, data_type="void"):
        super().__init__(name, SymbolTypes.FUN, data_type)
        self.f_args = []

    def add_param(self, param: Symbol):
        self.f_args.append(param)

    def __str__(self):
        return f"{self.data_type} {self.name}({', '.join([str(arg) for arg in self.f_args])})"
