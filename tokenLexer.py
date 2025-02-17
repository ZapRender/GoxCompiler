from tokenType import TokenType

class Token:
    def __init__(self, tokenType: TokenType, lexeme: str, literal, line: int):
        self.tokenType = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def toString(self):
        return f"{self.tokenType.name} {self.lexeme} {self.literal}"