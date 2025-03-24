# Topic: Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Daniela Cojocari

----
## Objectives:

* Understand what lexical analysis is.
* Get familiar with the inner workings of a lexer/scanner/tokenizer.
* Implement a sample lexer and show how it works.


## Implementation description

* For my lexer, I chose to implement a lexical analyzer that can handle arithmetic expressions and basic control structures. The lexer is responsible for tokenizing a given source code input by identifying meaningful elements such as numbers, operators, keywords, and punctuation symbols.

* The first part of the implementation of a lexer is to define what tokens will there be to identify. For my program, the tokens will be as follows:
```
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
```

* Then I construct a single regular expression by joining multiple token patterns from the TOKEN_TYPES dictionary.

```
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())
```

* The lexer function scans the input code and breaks it into tokens based on predefined patterns. It uses re.finditer() to find matches and extracts the token type and value. If an identifier matches a keyword (if, else, while, return), it is reclassified as a KEYWORD. Each token is then stored in a list and returned. This process helps convert raw code into structured data for further processing.

```
def lexer(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        token_type = match.lastgroup
        value = match.group(token_type)
        if token_type == "IDENTIFIER" and value in ["if", "else", "while", "return"]:
            token_type = "KEYWORD"
        tokens.append((token_type, value))
    return tokens
```

* Here is an example of code and it's output: \
Code: 
```
code = """
while (x <= 10.3) {
    y = y + 5.5;
}
"""
```

Output: 
```
('KEYWORD', 'while')
('LPAREN', '(')
('IDENTIFIER', 'x')
('LESS_EQUAL', '<=')
('NUMBER', '10.3')
('RPAREN', ')')
('LBRACE', '{')
('IDENTIFIER', 'y')
('ASSIGN', '=')
('IDENTIFIER', 'y')
('PLUS', '+')
('NUMBER', '5.5')
('SEMICOLON', ';')
('RBRACE', '}')
```

## Conclusions 
In this project, I implemented a lexer capable of handling arithmetic expressions and basic control structures.
I defined a set of token types, including numbers, identifiers, operators, and keywords, and constructed a regular expression to match them.
Using re.finditer(), the lexer scans the input code, extracts tokens, and correctly classifies keywords. 
The implementation was tested with sample code, demonstrating its ability to break down statements into structured tokens.
This project provided valuable insight into lexical analysis, showcasing how a lexer transforms raw code into a structured format for further processing in a compiler or interpreter.