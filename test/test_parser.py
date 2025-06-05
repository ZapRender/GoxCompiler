
import unittest
from lexer.scanner import Scanner
from parse.parse import Parser
from parse.model import Variable, Print, Assignment, If, While, Function, TypeCast, UnaryOp, FunctionCall

class ParserToken:
    def __init__(self, token):
        self.type = token.token_type.name
        self.value = token.literal if token.literal is not None else token.lexeme
        self.lineno = token.line

def error_handler(line, message):
    raise SyntaxError(f"[line {line}] Error: {message}")

def parse_source(source_code):
    scanner = Scanner(source_code, error_handler)
    tokens = scanner.scan_tokens()
    wrapped_tokens = [ParserToken(t) for t in tokens]
    parser = Parser(wrapped_tokens)
    return parser.parse()

class TestParser(unittest.TestCase):
    # ----------------------------
    # success cases
    # ----------------------------

    def test_variable_declaration(self):
        source = "var x int = 10;"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        var = ast[0]
        self.assertIsInstance(var, Variable)
        self.assertEqual(var.name, "x")
        self.assertEqual(var.type, "INT")
        self.assertEqual(var.expression.value, 10)
        self.assertFalse(var.is_const)

    def test_print_statement(self):
        source = "var x int = 5; print x;"
        ast = parse_source(source)
        self.assertEqual(len(ast), 2)
        self.assertIsInstance(ast[1], Print)
        self.assertEqual(ast[1].expression.name_or_expr, "x")

    def test_assignment(self):
        source = "x = 42;"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        assign = ast[0]
        self.assertIsInstance(assign, Assignment)
        self.assertEqual(assign.location.name_or_expr, "x")
        self.assertEqual(assign.expression.value, 42)

    def test_if_else(self):
        source = "if true { print 1; } else { print 2; }"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        node = ast[0]
        self.assertIsInstance(node, If)
        self.assertEqual(len(node.then_branch), 1)
        self.assertEqual(len(node.else_branch), 1)

    def test_while_loop(self):
        source = "while true { print 1; }"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        node = ast[0]
        self.assertIsInstance(node, While)
        self.assertEqual(len(node.body), 1)

    def test_function_declaration(self):
        source = "func sum(a int, b int) int { return a; }"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        func = ast[0]
        self.assertIsInstance(func, Function)
        self.assertEqual(func.name, "sum")
        self.assertEqual(len(func.params), 2)
        self.assertEqual(func.return_type, "INT")

    # ----------------------------
    # Error cases
    # ----------------------------

    def test_missing_semicolon_in_assignment(self):
        source = "x = 42"
        with self.assertRaises(SyntaxError) as cm:
            parse_source(source)
        self.assertIn("Se esperaba ';' al final de la asignación", str(cm.exception))

    def test_missing_semicolon_after_print(self):
        source = "print 42"
        with self.assertRaises(SyntaxError) as cm:
            parse_source(source)
        self.assertIn("Se esperaba ';' después de print", str(cm.exception))

    def test_invalid_token(self):
        source = "var x int = $;"
        with self.assertRaises(Exception) as cm:
            parse_source(source)
        self.assertIn("Unexpected character", str(cm.exception))

    def test_if_without_else_block(self):
        source = "if true { print 1; } else print 2;"
        with self.assertRaises(SyntaxError) as cm:
            parse_source(source)
        self.assertIn("Se esperaba '{' después de 'else'", str(cm.exception))

    def test_unclosed_function(self):
        source = "func foo() int { return 1;"
        with self.assertRaises(SyntaxError) as cm:
            parse_source(source)
        self.assertIn("Se esperaba '}'", str(cm.exception))
    # ----------------------------
    # Extras
    # ----------------------------
    def test_const_declaration(self):
        source = "const PI = 3.14;"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        const = ast[0]
        self.assertIsInstance(const, Variable)
        self.assertTrue(const.is_const)
        self.assertEqual(const.name, "PI")
        self.assertEqual(const.expression.value, 3.14)

    def test_import_function(self):
        source = "import func external(a int) int {}"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        func = ast[0]
        self.assertIsInstance(func, Function)
        self.assertEqual(func.name, "external")
        self.assertEqual(len(func.params), 1)
        self.assertEqual(func.return_type, "INT")

    def test_type_cast_expression(self):
        source = "print int(3.5);"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        pr = ast[0]
        self.assertIsInstance(pr, Print)
        self.assertIsInstance(pr.expression, TypeCast)
        self.assertEqual(pr.expression.type, "INT")

    def test_unary_expression(self):
        source = "print -x;"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        pr = ast[0]
        self.assertIsInstance(pr.expression, UnaryOp)
        self.assertEqual(pr.expression.op, "MINUS")

    def test_function_call_expression(self):
        source = "print sum(1, 2);"
        ast = parse_source(source)
        self.assertEqual(len(ast), 1)
        pr = ast[0]
        self.assertIsInstance(pr, Print)
        self.assertIsInstance(pr.expression, FunctionCall)  
        self.assertEqual(len(pr.expression.args), 2)      

if __name__ == '__main__':
    unittest.main()
