from enum import Enum

import src.compiler.exceptions as exceptions

class SymbolTypes(Enum):
    CLASS = 'class'
    FUN = 'function'
    VAR = 'variable'
    LIT = 'literal'


class Symbol:
    """
    Represents a symbol of a program (var, fun, class)
    """

    def __init__(self, name: str, symbol_type: SymbolTypes, data_type):
        self.name = name
        self.data_type = data_type
        if symbol_type not in SymbolTypes:
            raise exceptions.SemanticDeclarationError(f"Unknown type {symbol_type}")
        self.symbol_type = symbol_type

    def __str__(self):
        return f"{self.symbol_type} {self.name}"
