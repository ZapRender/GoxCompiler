from tokenLexer import Token
from tokenType import *

import re

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self) -> list[Token]:
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()
        
        return self.tokens
    
    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)
    
    def scanToken(self):
        c: str = self.advance()

        #Operators simple maping
        if c in SINGLE_CHAR_TOKENS:
            self.addToken(SINGLE_CHAR_TOKENS[c])
        
        #Operators with two characters
        elif c == '!':
                self.addToken(TokenType.NE if self.match('=') else TokenType.N)
        elif c == '=':
                self.addToken(TokenType.EQ if self.match('=') else TokenType.ASSIGN)
        elif c == '<':
                self.addToken(TokenType.LE if self.match('=') else TokenType.LT)
        elif c == '>':
                self.addToken(TokenType.GE if self.match('=') else TokenType.GT)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.DIVIDE)
        

        elif c == '\n':
            self.line += 1
        elif c in (' ', '\r', '\t'):
            pass
        elif c == '"':
            self.string()
        else:
            #Identifiers and keywords
            identifier = self.matchRegex(TOKEN_LITERALS[TokenType.IDENTIFIER])
            if identifier:
                tokenType = KEYWORDS.get(identifier, TokenType.IDENTIFIER)
                self.addToken(tokenType)
                return
            
            #Numeros enteros y flotantes
            number = self.matchRegex(TOKEN_LITERALS[TokenType.FLOAT]) or self.matchRegex(TOKEN_LITERALS[TokenType.INTEGER])
            if number:
                tokenType = TokenType.FLOAT if '.' in number else TokenType.INTEGER
                self.addToken(tokenType, float(number) if '.' in number else int(number))
                return
            
            #Individual characters
            char = self.matchRegex(TOKEN_LITERALS[TokenType.CHAR])
            if char:
                self.addToken(TokenType.CHAR, char[1])  # Extrae el carácter sin las comillas
                return
            
            #Gox.errorHandler(self.line, f"Unexpected character '{c}'")

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]
    
    def addToken(self, type: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if(self.isAtEnd()):
            return False
        if(self.source[self.current] != expected):
            return False
        
        self.current += 1
        return True

    def peek(self) -> str:
        if(self.isAtEnd()):
            return '\0'
        return self.source[self.current]
    
    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.isAtEnd():
            #Gox.errorHandler(self.line, "Unterminated string")
            pass
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.addToken(TokenType.CHAR, value)
    
    def matchRegex(self, regex: str) -> str:
        match = re.match(regex, self.source[self.current:])
        if match:
            self.current += len(match.group(0))
            return match.group(0)
        return None