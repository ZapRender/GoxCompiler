import unittest
from lexer.scanner import Scanner
from lexer.tokenType import TokenType

class TestLexer(unittest.TestCase):
    @staticmethod
    def error_callback(line, message):
        print(f"Error on line {line}: {message}")

    def test_single_tokens(self):
        lexer = Scanner("+ - * / ; ( ) { }", None)
        tokens = lexer.scan_tokens()
        expected = [
            TokenType.PLUS, TokenType.MINUS, TokenType.TIMES, TokenType.DIVIDE,
            TokenType.SEMI, TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACE, TokenType.RBRACE
        ]
        self.assertEqual([t.token_type for t in tokens], expected)
    
    def test_numbers(self):
        lexer = Scanner("123 3.14 -42", self.error_callback)
        tokens = lexer.scan_tokens()
        expected = [TokenType.INTEGER, TokenType.FLOAT, TokenType.MINUS, TokenType.INTEGER]
        values = [123, 3.14, None, 42]
        
        self.assertEqual([t.token_type for t in tokens], expected)
        self.assertEqual([t.literal for t in tokens], values)

    def test_identifiers_and_keywords(self):
        lexer = Scanner("var x = 10;", None)
        tokens = lexer.scan_tokens()
        expected = [TokenType.VAR, TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.INTEGER, TokenType.SEMI]
        
        self.assertEqual([t.token_type for t in tokens], expected)
    
    def test_operators(self):
        lexer = Scanner("<= >= == != < >", None)
        tokens = lexer.scan_tokens()
        expected = [TokenType.LE, TokenType.GE, TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.GT]
        
        self.assertEqual([t.token_type for t in tokens], expected)
    
    def test_comments(self):
        lexer = Scanner("// this is a comment\nvar x = 10;", None)
        tokens = lexer.scan_tokens()
        expected = [TokenType.VAR, TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.INTEGER, TokenType.SEMI]
        
        self.assertEqual([t.token_type for t in tokens], expected)
    
    def test_unexpected_character(self):
        lexer = Scanner("@", self.error_callback)
        tokens = lexer.scan_tokens()
        self.assertEqual(len(tokens), 0)

if __name__ == '__main__':
    unittest.main()

