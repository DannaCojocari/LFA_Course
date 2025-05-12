import re
from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    AND = auto()
    OR = auto()
    EQUALS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    KEYWORD = auto()


TOKEN_REGEX = {
    TokenType.NUMBER: r'\d+(\.\d+)?',
    TokenType.IDENTIFIER: r'[a-zA-Z_][a-zA-Z0-9_]*',
    TokenType.AND: r'&&',
    TokenType.OR: r'\|\|',
    TokenType.EQUALS: r'==',
    TokenType.GREATER_EQUAL: r'>=',
    TokenType.LESS_EQUAL: r'<=',
    TokenType.GREATER_THAN: r'>',
    TokenType.LESS_THAN: r'<',
    TokenType.PLUS: r'\+',
    TokenType.MINUS: r'-',
    TokenType.MULTIPLY: r'\*',
    TokenType.DIVIDE: r'/',
    TokenType.ASSIGN: r'=',
    TokenType.LPAREN: r'\(',
    TokenType.RPAREN: r'\)',
    TokenType.LBRACE: r'\{',
    TokenType.RBRACE: r'\}',
    TokenType.SEMICOLON: r';',
    TokenType.KEYWORD: r'\b(if|else|while|return)\b'
}

token_regex = '|'.join(f'(?P<{tok.name}>{pattern})' for tok, pattern in TOKEN_REGEX.items())

def lexer(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        token_type = match.lastgroup
        value = match.group(token_type)
        # Identifier or keyword
        if token_type == 'IDENTIFIER' and value in ['if', 'else', 'while', 'return']:
            token_type = 'KEYWORD'
        tokens.append((TokenType[token_type], value))
    return tokens