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

    def get_params(self):
        return self.f_args

    def get_return_type(self):
        return self.data_type

    def __str__(self):
        return f"{self.data_type} {self.name}({', '.join([str(arg) for arg in self.f_args])})"

    def __eq__(self, other):
        _name = self.name.split(':')[-1]
        _other = other.name.split(':')[-1]
        return _name == _other and self.data_type == other.data_type and self.f_args == other.f_args
