from src.sym_table.partial_symbol_table import PartialSymbolTable
from src.sym_table.symbol import Symbol


class SymbolTable:
    """
    A class to represent a symbol.py table stack as a whole
    """

    def __init__(self):
        """
        Initialize the symbol table with a global scope
        """
        self.tables = [PartialSymbolTable()]

    def push_scope(self):
        """
        create a new scope e.g.: entering a function
        """
        self.tables.append(PartialSymbolTable())

    def pop_scope(self):
        """
        e.g.: exiting a function
        """
        assert len(self.tables) > 1, "Can't pop the global scope"
        self.tables.pop()

    def add_symbol(self, s: Symbol):
        """
        add a symbol to the current scope
        """
        assert self.tables, "No scope to add symbol to"
        self.tables[-1].add_symbol(s)

    def add_global_symbol(self, s: Symbol):
        """
        add f() or class to the global scope
        """
        assert self.tables, "No scope to add symbol to"
        self.tables[0].add_symbol(s)

    def get_symbol(self, name) -> Symbol | None:
        """
        search for a symbol within all available scopes
        """
        for table in reversed(self.tables):
            # We are looking through all tables so exception is possible
            try:
                s = table.get_symbol(name)
            except ValueError:
                continue
            if s:
                return s
        return None

    def get_current_symbols(self) -> dict:
        """
        get all symbols in the current scope
        """
        return self.tables[-1].get_symbols()

    def __str__(self):
        _str = ""
        for i, table in zip(range(len(self.tables)), self.tables):
            _str += str(table) + f" table{i} \n"
        return _str
