from src.sym_table.symbol import Symbol


class PartialSymbolTable:
    """
    Represents current context e.g.: function or {} block
    """

    def __init__(self):
        self.symbols = {}

    def add_symbol(self, symbol: Symbol):
        if symbol.name in [s.name for s in self.symbols.values()]:
            raise ValueError(f"Symbol {symbol.name} already exists")
        self.symbols[symbol.name] = symbol

    def get_symbol(self, name: str) -> Symbol:
        if name not in [s.name for s in self.symbols.values()]:
            raise ValueError(f"Symbol {name} not found")
        return self.symbols.get(name)

    def get_symbols(self):
        return self.symbols.keys()

    def __str__(self):
        if not self.symbols:
            return "{}"
        return "{" + str([str(symbol) for symbol in self.symbols.values()]) + "}"
