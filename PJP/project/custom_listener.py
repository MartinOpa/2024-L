from antlr4 import *
from PJPProjectParser import PJPProjectParser
from PJPProjectListener import PJPProjectListener

class CustomListener(PJPProjectListener):

    def get_expression_type(self, ctx):
        if ctx.literalExpression():
            return self.get_literal_expression_type(ctx.literalExpression())
        elif ctx.variableExpression():
            return self.get_variable_expression_type(ctx.variableExpression())
        elif ctx.unaryExpression():
            return self.get_expression_type(ctx.unaryExpression().expression())
        elif ctx.assignmentExpression():
            return self.get_expression_type(ctx.assignmentExpression().expression())
        elif ctx.op:
            left_type = self.get_expression_type(ctx.expression(0))
            right_type = self.get_expression_type(ctx.expression(1))
            if left_type == right_type:
                return left_type
            else:
                return None
        else:
            return None

    def get_literal_expression_type(self, ctx):
        if ctx.INT_LITERAL():
            return 'int'
        elif ctx.FLOAT_LITERAL():
            return 'float'
        elif ctx.BOOL_LITERAL():
            return 'bool'
        elif ctx.STRING_LITERAL():
            return 'string'
        else:
            return None

    def get_variable_expression_type(self, ctx):
        var_name = ctx.ID().getText()
        if var_name in self.symbol_table:
            return self.symbol_table[var_name]
        else:
            print(var_name)
            return None
        