from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

class VerboseErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.error_count = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.error_count += 1
        print(f"Syntax error at line {line}:{column} {msg}")
        
