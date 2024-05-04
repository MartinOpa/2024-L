from antlr4 import *
from PJPProjectParser import PJPProjectParser
from custom_listener import CustomListener

class CodeGenerator(CustomListener):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.types = {}

    def exitProgram(self, ctx:PJPProjectParser.ProgramContext):
        for line in self.lines:
            print(line)
        pass

    def exitStatement(self, ctx:PJPProjectParser.StatementContext):
        pass

    def exitEmptyStatement(self, ctx:PJPProjectParser.EmptyStatementContext):
        pass

    def exitDeclarationStatement(self, ctx:PJPProjectParser.DeclarationStatementContext):
        for id in ctx.ID():
            id_ = id.getText()
            if ctx.type_().getText() in ['int', 'float']:
                if ctx.type_().getText() == 'int':
                    self.lines.append(f"push I 0")
                else:
                    self.lines.append(f"push F 0.0")                    
                self.lines.append(f"save {id_}")
            elif ctx.type_().getText() == 'string':
                self.lines.append(f"push S \"\"")
                self.lines.append(f"save {id_}")
            elif ctx.type_().getText() == 'bool':
                self.lines.append(f"push B false")
                self.lines.append(f"save {id_}")
            
            self.types[id_] = ctx.type_().getText()

    def exitType(self, ctx:PJPProjectParser.TypeContext):
        pass

    def exitExpressionStatement(self, ctx:PJPProjectParser.ExpressionStatementContext):
        pass

    def exitReadStatement(self, ctx:PJPProjectParser.ReadStatementContext):
        for id in ctx.ID():
            id_ = id.getText()
            if self.types[id_] == 'int':
                type_ = 'I'
            elif self.types[id_] == 'float':
                type_ = 'F'
            elif self.types[id_] == 'string':
                type_ = 'S'
            elif self.types[id_] == 'bool':
                type_ = 'B'

            self.lines.append(f"read {type_}")
            self.lines.append(f"save {id_}")
            

    def exitWriteStatement(self, ctx:PJPProjectParser.WriteStatementContext):
        i = len(ctx.expression())
        self.lines.append(f"print {i}")

    def exitBlockStatement(self, ctx:PJPProjectParser.BlockStatementContext):
        pass

    def exitIfStatement(self, ctx:PJPProjectParser.IfStatementContext):
        pass

    def exitWhileStatement(self, ctx:PJPProjectParser.WhileStatementContext):
        pass

    def exitExpression(self, ctx:PJPProjectParser.ExpressionContext):
        if ctx.op:
            left_type = self.get_expression_type(ctx.expression(0))
            right_type = self.get_expression_type(ctx.expression(1))

            if ((left_type == 'float' or right_type == 'float') and
                (left_type == 'int' or right_type == 'int')):
                self.lines.append('itof')

            sign = ctx.op.text
            if sign == '+':
                self.lines.append('add')
            elif sign == '-':
                self.lines.append('sub')
            elif sign == '*':
                self.lines.append('mul')
            elif sign == '/':
                self.lines.append('div')
            elif sign == '%':
                self.lines.append('mod')
            elif sign == '.':
                self.lines.append('concat')
            elif sign == '<':
                self.lines.append('lt')
            elif sign == '>':
                self.lines.append('gt')
            elif sign == '==':
                self.lines.append('eq')
            elif sign == '!=':
                self.lines.append('noteq')
            elif sign == '&&':
                self.lines.append('and')
            elif sign == '||':
                self.lines.append('or')

    def exitLiteralExpression(self, ctx:PJPProjectParser.LiteralExpressionContext):
        literal = ctx.getChild(0).getText()
        if ctx.INT_LITERAL():
            self.lines.append(f"push I {literal}")
        elif ctx.FLOAT_LITERAL():
            self.lines.append(f"push F {literal}")
        elif ctx.BOOL_LITERAL():
            self.lines.append(f"push B {literal}")
        elif ctx.STRING_LITERAL():
            self.lines.append(f"push S {literal}")

    def exitVariableExpression(self, ctx:PJPProjectParser.VariableExpressionContext):
        self.lines.append(f"load {ctx.ID()}")

    def exitUnaryExpression(self, ctx:PJPProjectParser.UnaryExpressionContext):
        if ctx.SUB():
            self.lines.append('uminus')
        elif ctx.NOT():
            self.lines.append('not')

    def exitAssignmentExpression(self, ctx:PJPProjectParser.AssignmentExpressionContext):
        left_type = self.types[ctx.ID().getText()]
        right_type = self.get_expression_type(ctx.expression())

        if ((left_type == 'float' or right_type == 'float') and
            (left_type == 'int' or right_type == 'int')):
            self.lines.append('itof')
        
        self.lines.append(f"save {ctx.ID().getText()}")
        self.lines.append(f"load {ctx.ID().getText()}")
        if not self.get_is_root_multi_assignment(ctx.parentCtx):
            self.lines.append(f"pop")

    def get_is_root_multi_assignment(self, ctx):
        if ctx is None or not isinstance(ctx, RuleContext):
            return False

        if isinstance(ctx, PJPProjectParser.AssignmentExpressionContext):
            return True

        return self.get_is_root_multi_assignment(ctx.parentCtx)
    