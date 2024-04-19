grammar PJPProject;

INT             : 'int';
FLOAT           : 'float';
BOOL            : 'bool';
STRING          : 'string';
TRUE            : 'true';
FALSE           : 'false';
ID              : [a-zA-Z][a-zA-Z0-9]*;
INT_LITERAL     : [0-9]+;
FLOAT_LITERAL   : [0-9]+ '.' [0-9]+;
BOOL_LITERAL    : TRUE | FALSE;
STRING_LITERAL  : '"' ( ~["\r\n] | '\\"' )* '"';
WS              : [ \t\r\n]+ -> skip;
COMMENT         : '//' ~[\r\n]* -> skip;

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
    | binaryExpression
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

binaryExpression : 
    expression ('*'|'/'|'%') expression
    | expression ('+'|'-'|'.') expression
    | expression ('<'|'>') expression
    | expression ('=='|'!=') expression
    | expression '&&' expression
    | expression '||' expression;

assignmentExpression : ID '=' expression;
