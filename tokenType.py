from enum import Enum, auto

class TokenType(Enum):
    #Single-character tokens.
    PLUS        = auto()
    MINUS       = auto()
    TIMES       = auto()
    DIVIDE      = auto() #Need to use a special case because comments use this character.
    LT          = auto()
    ASSIGN      = auto()  
    SEMI        = auto()
    LPAREN      = auto()
    RPAREN      = auto()
    LBRACE      = auto()
    RBRACE      = auto()
    COMMA       = auto()
    DEREF       = auto()
    GT          = auto()
    GROW        = auto()

    #One or two character tokens.
    LE          = auto()
    GE          = auto()
    EQ          = auto()
    NE          = auto()
    LAND        = auto()
    LOR         = auto()
    N           = auto()   

    #Literals.
    IDENTIFIER  = auto()
    INTEGER     = auto()
    FLOAT       = auto()
    CHAR        = auto()

    #Keywords.
    CONST       = auto()
    VAR         = auto() 
    PRINT       = auto() 
    RETURN      = auto() 
    BREAK       = auto() 
    CONTINUE    = auto() 
    IF          = auto() 
    ELSE        = auto() 
    WHILE       = auto() 
    FUNC        = auto() 
    IMPORT      = auto()
    TRUE        = auto()
    FALSE       = auto() 
 
SINGLE_CHAR_TOKENS = {
            '+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.TIMES,
            '/': TokenType.DIVIDE, '<': TokenType.LT, '=': TokenType.ASSIGN,
            ';': TokenType.SEMI, '(': TokenType.LPAREN, ')': TokenType.RPAREN,
            '{': TokenType.LBRACE, '}': TokenType.RBRACE, ',': TokenType.COMMA,
            '`': TokenType.DEREF, '>': TokenType.GT, '^': TokenType.GROW
        }

TOKEN_LITERALS = {
    TokenType.IDENTIFIER: r'[a-zA-Z_][a-zA-Z0-9_]*',
    TokenType.INTEGER: r'-?\d+',
    TokenType.FLOAT: r'-?\d*\.\d+',
    TokenType.CHAR: r'\'.\''
}

KEYWORDS = {
    'const': TokenType.CONST,
    'var': TokenType.VAR,
    'print': TokenType.PRINT,
    'return': TokenType.RETURN,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'func': TokenType.FUNC,
    'import': TokenType.IMPORT,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE
}