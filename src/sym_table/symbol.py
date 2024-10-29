from enum import Enum


class SymbolTypes(Enum):
    CLASS = 'class'
    FUN = 'function'
    VAR = 'variable'
    LiT = 'literal'


class Symbol:
    """
    Represents a symbol of a program (var, fun, class)
    """

    def __init__(self, name: str, symbol_type: SymbolTypes, data_type):
        self.name = name
        self.data_type = data_type
        if symbol_type not in SymbolTypes:
            raise ValueError(f"Unknown type {symbol_type}")
        self.symbol_type = symbol_type

    def __str__(self):
        return f"{self.symbol_type} {self.name}"
