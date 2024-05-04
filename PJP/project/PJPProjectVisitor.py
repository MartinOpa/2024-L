# Generated from PJPProject.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .PJPProjectParser import PJPProjectParser
else:
    from PJPProjectParser import PJPProjectParser

# This class defines a complete generic visitor for a parse tree produced by PJPProjectParser.

class PJPProjectVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PJPProjectParser#program.
    def visitProgram(self, ctx:PJPProjectParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#statement.
    def visitStatement(self, ctx:PJPProjectParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#emptyStatement.
    def visitEmptyStatement(self, ctx:PJPProjectParser.EmptyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#declarationStatement.
    def visitDeclarationStatement(self, ctx:PJPProjectParser.DeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#type.
    def visitType(self, ctx:PJPProjectParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#expressionStatement.
    def visitExpressionStatement(self, ctx:PJPProjectParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#readStatement.
    def visitReadStatement(self, ctx:PJPProjectParser.ReadStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#writeStatement.
    def visitWriteStatement(self, ctx:PJPProjectParser.WriteStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#blockStatement.
    def visitBlockStatement(self, ctx:PJPProjectParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#ifStatement.
    def visitIfStatement(self, ctx:PJPProjectParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#whileStatement.
    def visitWhileStatement(self, ctx:PJPProjectParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#expression.
    def visitExpression(self, ctx:PJPProjectParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#literalExpression.
    def visitLiteralExpression(self, ctx:PJPProjectParser.LiteralExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#variableExpression.
    def visitVariableExpression(self, ctx:PJPProjectParser.VariableExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#unaryExpression.
    def visitUnaryExpression(self, ctx:PJPProjectParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PJPProjectParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:PJPProjectParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)



del PJPProjectParser