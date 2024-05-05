from antlr4 import *
from PJPProjectParser import PJPProjectParser
from custom_listener import CustomListener

class CodeGenerator(CustomListener):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.symbol_table = {}
        self.current_label = 0
        self.declare_label = 0

    def exitStatement(self, ctx:PJPProjectParser.StatementContext):
        if isinstance(ctx.parentCtx, PJPProjectParser.IfStatementContext):
            if (ctx is ctx.parentCtx.statement(0)):
                self.add_label_current('jmp')
                self.add_label_declare() 

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
            
            self.symbol_table[id_] = ctx.type_().getText()

    def exitReadStatement(self, ctx:PJPProjectParser.ReadStatementContext):
        for id in ctx.ID():
            id_ = id.getText()
            if self.symbol_table[id_] == 'int':
                type_ = 'I'
            elif self.symbol_table[id_] == 'float':
                type_ = 'F'
            elif self.symbol_table[id_] == 'string':
                type_ = 'S'
            elif self.symbol_table[id_] == 'bool':
                type_ = 'B'

            self.lines.append(f"read {type_}")
            self.lines.append(f"save {id_}")

    def exitWriteStatement(self, ctx:PJPProjectParser.WriteStatementContext):
        i = len(ctx.expression())
        self.lines.append(f"print {i}")

    def exitIfStatement(self, ctx:PJPProjectParser.IfStatementContext):
        self.add_label_declare()

    def exitWhileStatement(self, ctx:PJPProjectParser.WhileStatementContext):
        self.add_label_current('jmp', -1)
        self.add_label_declare() 

    def enterWhileStatement(self, ctx:PJPProjectParser.WhileStatementContext):
        self.add_label_declare() 

    def exitExpression(self, ctx:PJPProjectParser.ExpressionContext):
        if ctx.op:
            left_type = self.get_expression_type(ctx.expression(0))
            right_type = self.get_expression_type(ctx.expression(1))

            sign = ctx.op.text
            if sign in ['+', '-', '*', '/', '%', '.']:
                if ((left_type == 'int' and right_type == 'float') or
                    (left_type == 'float' and right_type == 'int')):
                    self.lines.append('itof')

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
            else:
                if ((left_type == 'int' and right_type == 'float') or
                    (left_type == 'float' and right_type == 'int')):
                    line = self.lines[-1]
                    self.lines = self.lines[:-1]
                    self.lines.append('itof')
                    self.lines.append(line)

                if sign == '<':
                    self.lines.append('lt')
                    if self.get_is_if_statement(ctx.parentCtx):
                        self.add_label_current('fjmp')
                    elif self.get_is_while_statemept(ctx.parentCtx):
                        self.add_label_current('fjmp', +1)
                elif sign == '>':
                    self.lines.append('gt')
                    if self.get_is_if_statement(ctx.parentCtx):
                        self.add_label_current('fjmp')
                    elif self.get_is_while_statemept(ctx.parentCtx):
                        self.add_label_current('fjmp', +1)
                elif sign == '==':
                    self.lines.append('eq')
                    if self.get_is_if_statement(ctx.parentCtx):
                        self.add_label_current('fjmp')
                    elif self.get_is_while_statemept(ctx.parentCtx):
                        self.add_label_current('fjmp', +1)
                elif sign == '!=':
                    self.lines.append('eq')
                    self.lines.append('not')
                    if self.get_is_if_statement(ctx.parentCtx):
                        self.add_label_current('fjmp')
                    elif self.get_is_while_statemept(ctx.parentCtx):
                        self.add_label_current('fjmp', +1)
                elif sign == '&&':
                    self.lines.append('and')
                    if self.get_is_if_statement(ctx.parentCtx):
                        self.add_label_current('fjmp')
                    elif self.get_is_while_statemept(ctx.parentCtx):
                        self.add_label_current('fjmp', +1)
                elif sign == '||':
                    self.lines.append('or')
                    if self.get_is_if_statement(ctx.parentCtx):
                        self.add_label_current('fjmp')
                    elif self.get_is_while_statemept(ctx.parentCtx):
                        self.add_label_current('fjmp', +1)

    def exitLiteralExpression(self, ctx:PJPProjectParser.LiteralExpressionContext):
        literal = ctx.getChild(0).getText()
        if ctx.INT_LITERAL():
            self.lines.append(f"push I {literal}")
        elif ctx.FLOAT_LITERAL():
            self.lines.append(f"push F {literal}")
        elif ctx.BOOL_LITERAL():
            self.lines.append(f"push B {literal}")
            if self.get_is_if_statement(ctx.parentCtx):
                self.add_label_current('fjmp')
            elif self.get_is_while_statemept(ctx.parentCtx):
                self.add_label_current('fjmp', +1)
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
        left_type = self.symbol_table[ctx.ID().getText()]
        right_type = self.get_expression_type(ctx.expression())

        if ((left_type == 'int' and right_type == 'float') or
            (left_type == 'float' and right_type == 'int')):
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
    
    def get_is_if_statement(self, ctx):
        if ctx is None or not isinstance(ctx, RuleContext):
            return False

        if isinstance(ctx, PJPProjectParser.IfStatementContext):
            return True

        return self.get_is_if_statement(ctx.parentCtx)
    
    def get_is_while_statemept(self, ctx):
        if ctx is None or not isinstance(ctx, RuleContext):
            return False

        if isinstance(ctx, PJPProjectParser.WhileStatementContext):
            return True

        return self.get_is_while_statemept(ctx.parentCtx)

    def add_label_current(self, jump, offset=0):
        self.lines.append(f"{jump} {self.current_label + offset}")
        self.current_label += 1
    
    def add_label_declare(self):
        self.lines.append(f"label {self.declare_label}")
        self.declare_label += 1
        