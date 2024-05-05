grammar PJPProject;

BOOL_LITERAL    : 'true' | 'false';
INT             : 'int';
FLOAT           : 'float';
BOOL            : 'bool';
STRING          : 'string';
ID              : [a-zA-Z][a-zA-Z0-9]*;
INT_LITERAL     : [0-9]+;
FLOAT_LITERAL   : [0-9]+ '.' [0-9]+;
STRING_LITERAL  : '"' ( ~["\r\n] | '\\"' )* '"';
WS              : [ \t\r\n]+ -> skip;
COMMENT         : '//' ~[\r\n]* -> skip;

ADD         : '+';
SUB         : '-';
MUL         : '*';
DIV         : '/';
MOD         : '%';
CONCAT      : '.';
AND         : '&&';
OR          : '||';
GT          : '>';
LT          : '<';
EQ          : '==';
NOTEQ       : '!=';
NOT         : '!';

program : statement* EOF;

statement : 
    emptyStatement
    | declarationStatement
    | expressionStatement
    | readStatement
    | writeStatement
    | blockStatement
    | ifStatement
    | whileStatement;

emptyStatement : ';';

declarationStatement : type ID (',' ID)* ';';

type : INT | FLOAT | BOOL | STRING;

expressionStatement : expression ';';

readStatement : 'read' ID (',' ID)* ';';

writeStatement : 'write' expression (',' expression)* ';';

blockStatement : '{' statement* '}';

ifStatement : 'if' '(' expression ')' statement ('else' statement)?;

whileStatement : 'while' '(' expression ')' statement;

expression :
    literalExpression
    | variableExpression
    | unaryExpression
    | expression op=(MUL|DIV|MOD) expression
    | expression op=(ADD|SUB|CONCAT) expression
    | expression op=(EQ|NOTEQ) expression
    | expression op=(LT|GT) expression
    | expression op=AND expression
    | expression op=OR expression
    | assignmentExpression
    | '(' expression ')';

literalExpression :
    INT_LITERAL
    | FLOAT_LITERAL
    | BOOL_LITERAL
    | STRING_LITERAL;

variableExpression : ID;

unaryExpression :
    '-' expression
    | '!' expression;

assignmentExpression : ID '=' expression;

