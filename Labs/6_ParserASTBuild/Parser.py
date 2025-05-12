from Lexer import *
from AST import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def eat(self, token_type):
        if self.current()[0] == token_type:
            value = self.current()[1]
            self.pos += 1
            return value
        raise SyntaxError(f"Expected {token_type}, got {self.current()}")

    def parse(self):
        statements = []
        while self.current()[0] is not None:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        if self.current()[0] == TokenType.KEYWORD and self.current()[1] == 'while':
            return self.parse_while()
        elif self.current()[0] == TokenType.KEYWORD and self.current()[1] == 'if':
            return self.parse_if()
        else:
            return self.parse_assignment()

    def parse_while(self):
        self.eat(TokenType.KEYWORD)  # while
        self.eat(TokenType.LPAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        body = []
        while self.current()[0] != TokenType.RBRACE:
            body.append(self.parse_statement())
        self.eat(TokenType.RBRACE)
        return WhileStatement(condition, body)

    def parse_if(self):
        self.eat(TokenType.KEYWORD)  # if
        self.eat(TokenType.LPAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        body = []
        while self.current()[0] != TokenType.RBRACE:
            body.append(self.parse_statement())
        self.eat(TokenType.RBRACE)

        else_body = None
        if self.current()[0] == TokenType.KEYWORD and self.current()[1] == 'else':
            self.eat(TokenType.KEYWORD)  # else
            self.eat(TokenType.LBRACE)
            else_body = []
            while self.current()[0] != TokenType.RBRACE:
                else_body.append(self.parse_statement())
            self.eat(TokenType.RBRACE)

        return IfStatement(condition, body, else_body)

    def parse_assignment(self):
        identifier = self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        expr = self.parse_expression()
        self.eat(TokenType.SEMICOLON)
        return Assignment(Identifier(identifier), expr)

    # === Expression Parsing with Precedence ===
    def parse_expression(self):
        return self.parse_equality()

    def parse_equality(self):
        left = self.parse_comparison()
        while self.current()[0] == TokenType.EQUALS:
            op = self.eat(TokenType.EQUALS)
            right = self.parse_comparison()
            left = BinaryExpression(left, op, right)
        return left

    def parse_comparison(self):
        left = self.parse_term()
        while self.current()[0] in {
            TokenType.LESS_THAN, TokenType.LESS_EQUAL,
            TokenType.GREATER_THAN, TokenType.GREATER_EQUAL
        }:
            op = self.eat(self.current()[0])
            right = self.parse_term()
            left = BinaryExpression(left, op, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current()[0] in {TokenType.PLUS, TokenType.MINUS}:
            op = self.eat(self.current()[0])
            right = self.parse_factor()
            left = BinaryExpression(left, op, right)
        return left

    def parse_factor(self):
        left = self.parse_atom()
        while self.current()[0] in {TokenType.MULTIPLY, TokenType.DIVIDE}:
            op = self.eat(self.current()[0])
            right = self.parse_atom()
            left = BinaryExpression(left, op, right)
        return left

    def parse_atom(self):
        tok_type, value = self.current()
        if tok_type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Literal(float(value))
        elif tok_type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Identifier(value)
        elif tok_type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        raise SyntaxError("Unexpected token in expression")
