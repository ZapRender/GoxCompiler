from tokenLexer import Token
from tokenType import *
import re

class Scanner:
    def __init__(self, source: str, errorCallback):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.errorCallback = errorCallback
        self.hadError = False

    def scanTokens(self) -> list[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        return self.tokens

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def scanToken(self):
        c: str = self.advance()

        # Manejo de comentarios
        if c == '/':
            if self.match('/'):
                self.ignoreSingleLineComment()
                return
            elif self.match('*'):
                self.ignoreMultiLineComment()
                return
            else:
                self.addToken(TokenType.DIVIDE)
                return
        # Tokens de dos caracteres
        elif c == '!' and self.match('='):
            self.addToken(TokenType.NE)
            return

        elif c == '=' and self.match('='):
            self.addToken(TokenType.EQ)
            return

        elif c == '<' and self.match('='):
            self.addToken(TokenType.LE)
            return

        elif c == '>' and self.match('='):
            self.addToken(TokenType.GT)
            return 

        elif c == '&' and self.match('&'):
            self.addToken(TokenType.LAND)
            return 

        elif c == '|' and self.match('|'):
            self.addToken(TokenType.LOR)
            return

        # Tokens de un solo carácter
        if c in SINGLE_CHAR_TOKENS:
            self.addToken(SINGLE_CHAR_TOKENS[c])
            return

        elif c == '\n':
            self.line += 1
        elif c in (' ', '\r', '\t'):
            pass
        elif c == '"':
            self.string()
        else:
            # Intenta reconocer identificadores y palabras clave
            identifier = self.matchRegex(TOKEN_LITERALS[TokenType.IDENTIFIER])
            if identifier:
                tokenType = KEYWORDS.get(identifier, TokenType.IDENTIFIER)
                self.addToken(tokenType)
                return

            # Números (flotantes o enteros)
            number = self.matchRegex(TOKEN_LITERALS[TokenType.FLOAT]) or self.matchRegex(TOKEN_LITERALS[TokenType.INTEGER])
            if number:
                tokenType = TokenType.FLOAT if '.' in number else TokenType.INTEGER
                try:
                    value = float(number) if '.' in number else int(number)
                except ValueError:
                    self.error(self.line, f"Malformed number '{number}'")
                    value = None
                self.addToken(tokenType, value)
                return

            # Literales de carácter
            char = self.matchRegex(TOKEN_LITERALS[TokenType.CHAR])
            if char:
                # Extrae el carácter entre las comillas
                self.addToken(TokenType.CHAR, char[1])
                return

            # Si no se reconoce el carácter, se reporta un error léxico.
            self.error(self.line, f"Unexpected character '{c}'")

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def addToken(self, type: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def peekNext(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.isAtEnd():
            self.error(self.line, "Unterminated string")
            return
        self.advance()  # Consume la comilla de cierre
        value = self.source[self.start + 1:self.current - 1]
        self.addToken(TokenType.CHAR, value)

    def matchRegex(self, regex: str) -> str:
        # Importante: se hace match desde self.start para incluir el primer carácter ya consumido.
        match = re.match(regex, self.source[self.start:])
        if match:
            # Actualiza current a partir de self.start para reflejar el lexema completo.
            self.current = self.start + len(match.group(0))
            return match.group(0)
        return None

    def ignoreSingleLineComment(self):
        while self.peek() != '\n' and not self.isAtEnd():
            self.advance()

    def ignoreMultiLineComment(self):
        while not (self.peek() == '*' and self.peekNext() == '/') and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.isAtEnd():
            self.error(self.line, "Unterminated multiline comment")
            return
        self.advance()  # Consume '*'
        self.advance()  # Consume '/'

    def error(self, line, message):
        self.errorCallback(line, message)
        self.hadError = True
