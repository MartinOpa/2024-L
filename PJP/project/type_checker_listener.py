from antlr4 import *
from PJPProjectParser import PJPProjectParser
from custom_listener import CustomListener

class TypeChecker(CustomListener):
    def __init__(self):
        super().__init__()
        self.symbol_table = {}
        self.error_count = 0

    def type_error(self, line, column, message):
        self.error_count += 1
        print(f"Type error at line {line}:{column}: {message}")

    def expr_type_error(self, line, column, operand, type_left, type_right):
        self.error_count += 1
        print(f"Unsupported operand '{operand}' at line {line}:{column} for types {type_left}, {type_right}.")

    def unary_expr_type_error(self, line, column, operand, type_unary):
        self.error_count += 1
        print(f"Unsupported operand '{operand}' at line {line}:{column} for type {type_unary}.")

    def bool_expected(self, statement, line, column):
        self.error_count += 1
        print(f"{statement} condition: boolean statement expected at line {line}:{column}.")

    def exitIfStatement(self, ctx:PJPProjectParser.IfStatementContext):
        if not (self.get_expression_type(ctx.expression()) == 'bool'):
            self.bool_expected('If', ctx.expression().start.line, ctx.expression().start.column)

    def exitWhileStatement(self, ctx:PJPProjectParser.WhileStatementContext):
        if not (self.get_expression_type(ctx.expression()) == 'bool'):
            self.bool_expected('While', ctx.expression().start.line, ctx.expression().start.column)

    def exitUnaryExpression(self, ctx:PJPProjectParser.UnaryExpressionContext):
        unary_type = self.get_expression_type(ctx.expression())
        if ctx.SUB():
            if not (unary_type in ['int', 'float']):
                self.unary_expr_type_error(ctx.SUB().symbol.line, ctx.SUB().symbol.column, '-', unary_type)
        elif ctx.NOT():
            if not (unary_type == 'bool'):
                self.unary_expr_type_error(ctx.NOT().symbol.line, ctx.NOT().symbol.column, '!', unary_type)

    def exitExpression(self, ctx:PJPProjectParser.ExpressionContext):
        if ctx.op:
            left_type = self.get_expression_type(ctx.expression(0))
            right_type = self.get_expression_type(ctx.expression(1))
            if ctx.MUL() or ctx.DIV() or ctx.ADD() or ctx.SUB():
                if not (left_type in ['int', 'float'] and right_type in ['int', 'float']):
                    self.expr_type_error(ctx.op.line, ctx.op.column, ctx.op.text, left_type, right_type)
            elif ctx.MOD():
                if not (left_type == right_type == 'int'):
                    self.expr_type_error(ctx.op.line, ctx.op.column, ctx.op.text, left_type, right_type)
            elif ctx.CONCAT():
                if not (left_type == right_type == 'string'):
                    self.expr_type_error(ctx.op.line, ctx.op.column, ctx.op.text, left_type, right_type)
            elif ctx.EQ() or ctx.NOTEQ():
                if not (left_type == right_type):
                    self.expr_type_error(ctx.op.line, ctx.op.column, ctx.op.text, left_type, right_type)
            elif ctx.LT() or ctx.GT():
                if not ((left_type in ['int', 'float'] and right_type in ['int', 'float']) or
                        (left_type == right_type == 'string')):
                    self.expr_type_error(ctx.op.line, ctx.op.column, ctx.op.text, left_type, right_type)
            elif ctx.AND() or ctx.OR():
                if not (left_type == right_type == 'bool'):
                    self.expr_type_error(ctx.op.line, ctx.op.column, ctx.op.text, left_type, right_type)

    def exitAssignmentExpression(self, ctx:PJPProjectParser.AssignmentExpressionContext):
        var_name = ctx.ID().getText()
        if var_name not in self.symbol_table:
            self.type_error(ctx.ID().symbol.line, ctx.ID().symbol.column, f"Found variable '{var_name}' without a previous declaration.")
        else:
            expected_type = self.symbol_table[var_name]
            expr_type = self.get_expression_type(ctx.expression())
            if expr_type != expected_type:
                if not (expected_type == 'float' and expr_type == 'int'):
                    self.type_error(ctx.ID().symbol.line, ctx.ID().symbol.column, 
                                  f"Type mismatch for variable '{var_name}'. Expected {expected_type}, got {expr_type}.")

    def exitDeclarationStatement(self, ctx:PJPProjectParser.DeclarationStatementContext):
        data_type = ctx.type_().getText()
        for var_id in ctx.ID():
            var_name = var_id.getText()
            if var_name in self.symbol_table:
                self.type_error(var_id.symbol.line, var_id.symbol.column, f"Variable '{var_name}' was already declared.")
            else:
                self.symbol_table[var_name] = data_type
                