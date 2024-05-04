from antlr4 import *
from PJPProjectParser import PJPProjectParser
from PJPProjectVisitor import PJPProjectVisitor

class TypeCheckerVisitor(PJPProjectVisitor):
    def __init__(self):
        super().__init__()
        self.symbol_table = {}
        self.error_count = 0

    def type_error(self, ctx, message):
        self.error_count += 1
        print(f"Type error at line {ctx.start.line}:{ctx.start.column}: {message}")

    def visitProgram(self, ctx:PJPProjectParser.ProgramContext):
        for statement in ctx.statement():
            self.visit(statement)

    def visitDeclarationStatement(self, ctx:PJPProjectParser.DeclarationStatementContext):
        data_type = ctx.type_().getText()
        for var_id in ctx.ID():
            var_name = var_id.getText()
            if var_name in self.symbol_table:
                self.type_error(var_id, f"Variable '{var_name}' was already declared.")
            else:
                self.symbol_table[var_name] = data_type

    def visitAssignmentExpression(self, ctx:PJPProjectParser.AssignmentExpressionContext):
        var_name = ctx.ID().getText()
        assigned_type = self.visit(ctx.expression())
        if var_name in self.symbol_table:
            expected_type = self.symbol_table[var_name]
            if assigned_type != expected_type:
                if not (expected_type == 'float' and assigned_type == 'int'):
                    self.type_error(ctx, f"Type mismatch for variable '{var_name}'. Expected {expected_type}, got {assigned_type}.")
        else:
            self.type_error(ctx.ID(), f"Variable '{var_name}' is not declared.")
        
    def visitLiteralExpression(self, ctx:PJPProjectParser.LiteralExpressionContext):
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
        
    def visitExpression(self, ctx: PJPProjectParser.ExpressionContext):
        if ctx.literalExpression():
            return self.visit(ctx.literalExpression())
        elif ctx.variableExpression():
            return self.visit(ctx.variableExpression())
        elif ctx.op:
            left_type = self.visit(ctx.expression(0))
            right_type = self.visit(ctx.expression(1))
            if left_type == right_type:
                return left_type
            elif (left_type == 'float' and right_type == 'int') or (left_type == 'int' and right_type == 'float'):
                return 'float'
            else:
                self.type_error(ctx, f"Type mismatch in expression. Left: {left_type}, Right: {right_type}")
                return None
        else:
            return None

    def visitVariableExpression(self, ctx:PJPProjectParser.VariableExpressionContext):
        var_name = ctx.ID().getText()
        if var_name in self.symbol_table:
            return self.symbol_table[var_name]
        else:
            self.type_error(ctx.ID(), f"Variable '{var_name}' is not declared.")
            return None