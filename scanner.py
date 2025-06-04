from tokenLexer import Token
from tokenType import TokenType, SINGLE_CHAR_TOKENS, KEYWORDS, TOKEN_LITERALS
import re

class Scanner:
    def __init__(self, source: str, error_callback):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_callback = error_callback
        self.had_error = False

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self):
        c: str = self.peek()

        # Handle comments
        if c == '/':
            self.advance()
            if self.match('/'):
                self.ignore_single_line_comment()
                return
            elif self.match('*'):
                self.ignore_multi_line_comment()
                return
            else:
                self.add_token(TokenType.DIVIDE)
                return

        # Two-character tokens
        if c == '!' and self.peek_next() == '=':
            self.advance(); self.advance()
            self.add_token(TokenType.NE)
            return
        elif c == '=' and self.peek_next() == '=':
            self.advance(); self.advance()
            self.add_token(TokenType.EQ)
            return
        elif c == '<' and self.peek_next() == '=':
            self.advance(); self.advance()
            self.add_token(TokenType.LE)
            return
        elif c == '>' and self.peek_next() == '=':
            self.advance(); self.advance()
            self.add_token(TokenType.GE)
            return
        elif c == '&' and self.peek_next() == '&':
            self.advance(); self.advance()
            self.add_token(TokenType.LAND)
            return
        elif c == '|' and self.peek_next() == '|':
            self.advance(); self.advance()
            self.add_token(TokenType.LOR)
            return

        # One-character tokens
        if c in SINGLE_CHAR_TOKENS:
            self.advance()
            self.add_token(SINGLE_CHAR_TOKENS[c])
            return
        elif c == '\n':
            self.advance()
            self.line += 1
            return
        elif c in (' ', '\r', '\t'):
            self.advance()
            return
        elif c == '"':
            self.advance()
            self.string()
            return

        # Identifiers and keywords
        identifier = self.match_regex(TOKEN_LITERALS[TokenType.IDENTIFIER])
        if identifier:
            token_type = KEYWORDS.get(identifier, TokenType.IDENTIFIER)
            self.add_token(token_type)
            return

        # Numbers
        number = self.match_regex(TOKEN_LITERALS[TokenType.FLOAT]) or self.match_regex(TOKEN_LITERALS[TokenType.INTEGER])
        if number:
            token_type = TokenType.FLOAT if '.' in number else TokenType.INTEGER
            try:
                value = float(number) if '.' in number else int(number)
            except ValueError:
                self.error(self.line, f"Malformed number '{number}'")
                value = None
            self.add_token(token_type, value)
            return

        # Characters
        char = self.match_regex(TOKEN_LITERALS[TokenType.CHAR])
        if char:
            try:
                value = eval(char)
                self.add_token(TokenType.CHAR, value)
            except Exception:
                self.error(self.line, f"Invalid character literal: {char}")
            return

        # If no rule matched, report unexpected character
        self.advance()
        self.error(self.line, f"Unexpected character '{c}'")

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.error(self.line, "Unterminated string")
            return
        self.advance()  # Consume closing quotation marks
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.CHAR, value)

    def match_regex(self, regex: str) -> str:
        match = re.match(regex, self.source[self.start:])
        if match:
            self.current = self.start + len(match.group(0))
            return match.group(0)
        return ''

    def ignore_single_line_comment(self):
        while self.peek() != '\n' and not self.is_at_end():
            self.advance()

    def ignore_multi_line_comment(self):
        while not (self.peek() == '*' and self.peek_next() == '/') and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.error(self.line, "Unterminated multiline comment")
            return
        self.advance()  # Consume '*'
        self.advance()  # Consume '/'

    def error(self, line, message):
        self.error_callback(line, message)
        self.had_error = True
