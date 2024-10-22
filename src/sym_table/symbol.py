from enum import Enum


class SymbolTypes(Enum):
    INT = 'int'
    STR = 'str'


class Symbol:
    """
    Represents a symbol of a program ( var, fun, class)
    """

    def __init__(self, name: str, var_type=SymbolTypes.INT, value=None):
        self.name = name
        if var_type not in SymbolTypes:
            raise ValueError(f"Unknown type {var_type}")
        self.var_type = var_type
        self.value = value

    def __str__(self):
        return f"{self.var_type} {self.name}"
