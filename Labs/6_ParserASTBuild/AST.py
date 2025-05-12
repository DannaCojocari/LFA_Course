class ASTNode: pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program({self.statements})"

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f"While({self.condition}, {self.body})"

class IfStatement(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
    def __repr__(self):
        return f"If({self.condition}, {self.body}, {self.else_body})"

class Assignment(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    def __repr__(self):
        return f"{self.identifier} = {self.expression}"

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return str(self.value)

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name


def print_ast_tree(node, prefix="", is_tail=True):
    connector = "└── " if is_tail else "├── "

    if isinstance(node, Program):
        print(prefix + connector + "Program")
        for i, stmt in enumerate(node.statements):
            print_ast_tree(stmt, prefix + ("    " if is_tail else "│   "), i == len(node.statements) - 1)

    elif isinstance(node, WhileStatement):
        print(prefix + connector + "While")
        print_ast_tree(node.condition, prefix + ("    " if is_tail else "│   "), False)
        print(prefix + ("    " if is_tail else "│   ") + "├── Body")
        for i, stmt in enumerate(node.body):
            print_ast_tree(stmt, prefix + ("    " if is_tail else "│   ") + ("    " if i == len(node.body) - 1 else "│   "), i == len(node.body) - 1)

    elif isinstance(node, IfStatement):
        print(prefix + connector + "If")
        print_ast_tree(node.condition, prefix + ("    " if is_tail else "│   "), False)
        print(prefix + ("    " if is_tail else "│   ") + "├── Body")
        for i, stmt in enumerate(node.body):
            print_ast_tree(stmt, prefix + ("    " if is_tail else "│   ") + ("    " if i == len(node.body) - 1 else "│   "), i == len(node.body) - 1)
        if node.else_body:
            print(prefix + ("    " if is_tail else "│   ") + "├── Else")
            for i, stmt in enumerate(node.else_body):
                print_ast_tree(stmt, prefix + ("    " if is_tail else "│   ") + ("    " if i == len(node.else_body) - 1 else "│   "), i == len(node.else_body) - 1)

    elif isinstance(node, Assignment):
        print(prefix + connector + f"Assign: {node.identifier.name}")
        print_ast_tree(node.expression, prefix + ("    " if is_tail else "│   "), True)

    elif isinstance(node, BinaryExpression):
        print(prefix + connector + f"Operator: {node.operator}")
        print_ast_tree(node.left, prefix + ("    " if is_tail else "│   "), False)
        print_ast_tree(node.right, prefix + ("    " if is_tail else "│   "), True)

    elif isinstance(node, Literal):
        print(prefix + connector + f"Literal: {node.value}")

    elif isinstance(node, Identifier):
        print(prefix + connector + f"Identifier: {node.name}")

    else:
        print(prefix + connector + f"Unknown node: {type(node)}")