from antlr4.error.ErrorListener import ErrorListener


class LexicalErrorListener(ErrorListener):
    def __init__(self):
        super(LexicalErrorListener, self).__init__()
        self.has_errors = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.has_errors = True
