# Generated from PJPProject.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .PJPProjectParser import PJPProjectParser
else:
    from PJPProjectParser import PJPProjectParser

# This class defines a complete listener for a parse tree produced by PJPProjectParser.
class PJPProjectListener(ParseTreeListener):

    # Enter a parse tree produced by PJPProjectParser#program.
    def enterProgram(self, ctx:PJPProjectParser.ProgramContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#program.
    def exitProgram(self, ctx:PJPProjectParser.ProgramContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#statement.
    def enterStatement(self, ctx:PJPProjectParser.StatementContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#statement.
    def exitStatement(self, ctx:PJPProjectParser.StatementContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#emptyStatement.
    def enterEmptyStatement(self, ctx:PJPProjectParser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#emptyStatement.
    def exitEmptyStatement(self, ctx:PJPProjectParser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#declarationStatement.
    def enterDeclarationStatement(self, ctx:PJPProjectParser.DeclarationStatementContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#declarationStatement.
    def exitDeclarationStatement(self, ctx:PJPProjectParser.DeclarationStatementContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#type.
    def enterType(self, ctx:PJPProjectParser.TypeContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#type.
    def exitType(self, ctx:PJPProjectParser.TypeContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#expressionStatement.
    def enterExpressionStatement(self, ctx:PJPProjectParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#expressionStatement.
    def exitExpressionStatement(self, ctx:PJPProjectParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#readStatement.
    def enterReadStatement(self, ctx:PJPProjectParser.ReadStatementContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#readStatement.
    def exitReadStatement(self, ctx:PJPProjectParser.ReadStatementContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#writeStatement.
    def enterWriteStatement(self, ctx:PJPProjectParser.WriteStatementContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#writeStatement.
    def exitWriteStatement(self, ctx:PJPProjectParser.WriteStatementContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#blockStatement.
    def enterBlockStatement(self, ctx:PJPProjectParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#blockStatement.
    def exitBlockStatement(self, ctx:PJPProjectParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#ifStatement.
    def enterIfStatement(self, ctx:PJPProjectParser.IfStatementContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#ifStatement.
    def exitIfStatement(self, ctx:PJPProjectParser.IfStatementContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#whileStatement.
    def enterWhileStatement(self, ctx:PJPProjectParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#whileStatement.
    def exitWhileStatement(self, ctx:PJPProjectParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#expression.
    def enterExpression(self, ctx:PJPProjectParser.ExpressionContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#expression.
    def exitExpression(self, ctx:PJPProjectParser.ExpressionContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#literalExpression.
    def enterLiteralExpression(self, ctx:PJPProjectParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#literalExpression.
    def exitLiteralExpression(self, ctx:PJPProjectParser.LiteralExpressionContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#variableExpression.
    def enterVariableExpression(self, ctx:PJPProjectParser.VariableExpressionContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#variableExpression.
    def exitVariableExpression(self, ctx:PJPProjectParser.VariableExpressionContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#unaryExpression.
    def enterUnaryExpression(self, ctx:PJPProjectParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#unaryExpression.
    def exitUnaryExpression(self, ctx:PJPProjectParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by PJPProjectParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:PJPProjectParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by PJPProjectParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:PJPProjectParser.AssignmentExpressionContext):
        pass



del PJPProjectParser