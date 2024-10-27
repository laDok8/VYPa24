from enum import Enum


class SymbolTypes(Enum):
    INT = 'int'
    STR = 'string'
    VOID = 'void'
    FNC = 'function'
    CLS = 'class'


class Symbol:
    """
    Represents a symbol of a program (var, fun, class)
    """

    def __init__(self, name: str, var_type=SymbolTypes.INT, value=None, f_args=None, f_ret=SymbolTypes.VOID,
                 class_parent=None):
        self.name = name
        if var_type not in SymbolTypes:
            raise ValueError(f"Unknown type {var_type}")
        self.var_type = var_type
        self.value = value
        self.f_args = f_args
        self.f_ret = f_ret
        self.class_parent = class_parent

    def __str__(self):
        return f"{self.var_type} {self.name}"
