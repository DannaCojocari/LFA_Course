import re

TOKEN_TYPES = {
    'NUMBER': r'\d+(\.\d+)?',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',

    'AND': r'&&', 'OR': r'\|\|', 'EQUALS': r'==', 'GREATER_EQUAL': r'>=', 'LESS_EQUAL': r'<=',
    'GREATER_THAN': r'>', 'LESS_THAN': r'<',

    'PLUS': r'\+', 'MINUS': r'-', 'MULTIPLY': r'\*', 'DIVIDE': r'/',

    'ASSIGN': r'=',

    'LPAREN': r'\(', 'RPAREN': r'\)', 'LBRACE': r'\{', 'RBRACE': r'\}', 'SEMICOLON': r';',

    'KEYWORD': r'\b(if|else|while|return)\b'
}

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())

def lexer(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        token_type = match.lastgroup
        value = match.group(token_type)
        if token_type == "IDENTIFIER" and value in ["if", "else", "while", "return"]:
            token_type = "KEYWORD"
        tokens.append((token_type, value))
    return tokens


code = """
while (x <= 10.3) {
    y = y + 5.5;
}
"""


tokens = lexer(code)
for token in tokens:
    print(token)

