from Parser import *
from AST import *
from Lexer import *

code1 = """
while (x <= 10.3) {
    y = y + 5.5;
    x = x + 1;
}
"""

code2 = """
if (z == 10) {
    x = z * 3;
} else {
    x = y / 4;
}
"""

code3 = """
if ( x + 10 > 100) {
    y = x + y;
}
"""

print("Code : while (x <= 10.3) { \n   y = y + 5.5;\n    x = x + 1;\n }\n")
tokens = lexer(code1)
parser = Parser(tokens)
ast = parser.parse()
print_ast_tree(ast)

print("Code : if (z == 10) {\n    x = z * 3;\n} else {\n    x = y / 4;\n}\n")
tokens = lexer(code2)
parser = Parser(tokens)
ast = parser.parse()
print_ast_tree(ast)

print("Code : if ( x + 10 > 100) {\n    y = x + y; \n}\n")
tokens = lexer(code3)
parser = Parser(tokens)
ast = parser.parse()
print_ast_tree(ast)

