from antlr4 import *
from PJPProjectLexer import PJPProjectLexer
from PJPProjectListener import PJPProjectListener
from PJPProjectParser import PJPProjectParser

from error_listener import VerboseErrorListener
from type_checker_listener import TypeChecker
from type_checker_visitor import TypeCheckerVisitor
from code_generator import CodeGenerator
from interpreter import Interpreter

def try_execute(file_name):
    input_file = open(f'inputs/{file_name}.in', 'r').read()
    input_stream = InputStream(input_file)

    lexer = PJPProjectLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PJPProjectParser(stream)

    error_listener = VerboseErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.program()
    if error_listener.error_count > 0:
        return

    type_checker = TypeChecker()
    walker = ParseTreeWalker()
    walker.walk(type_checker, tree)
    if type_checker.error_count > 0:
        return
    
    # type_checker_visitor = TypeCheckerVisitor()
    # type_checker_visitor.visit(tree)
    # if type_checker_visitor.error_count > 0:
    #     return

    code_generator = CodeGenerator()
    walker = ParseTreeWalker()
    walker.walk(code_generator, tree)
    with open(f'outputs/{file_name}.out', 'w') as file:
        for line in code_generator.lines:
            file.write(line + '\n')

    interpreter = Interpreter()
    with open(f'outputs/{file_name}.out', 'r') as file:
        for line in file:
            interpreter.lines.append(line.strip())

    interpreter.process()

try_execute('PLC_t1')
#try_execute('PLC_t2')
#try_execute('PLC_t3')