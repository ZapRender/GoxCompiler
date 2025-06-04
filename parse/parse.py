
from typing import List
from dataclasses import dataclass
from parse.model import (
    Integer, Float, Char, Bool, TypeCast, BinOp, 
    UnaryOp, Assignment, Variable, NamedLocation, 
    Break, Continue, Return, Print, If, While, 
    Function, Parameter, FunctionCall, MemoryLocation
)
import sys
import json
from lexer.scanner import Scanner
class Parser:
    EXPECTED_RPAREN_MSG = "Se esperaba ')'"
    EXPECTED_LBRACE_MSG = "Se esperaba '{'"
    EXPECTED_RBRACE_MSG = "Se esperaba '}'"

    def __init__(self, tokens: List):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List:
        statements = []
        while self.peek() and self.peek().type != "EOF":
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.match("IDENTIFIER") and self.peek().type == "ASSIGN":
            self.current -= 1
            return self.assignment()
        elif self.check("DEREF"):
            return self.assignment()
        elif self.match("VAR") or self.match("CONST"):
            self.current -= 1
            return self.vardecl()
        elif self.check("IMPORT") or self.check("FUNC"):
            return self.funcdecl()
        elif self.match("IF"):
            self.current -= 1
            return self.if_stmt()
        elif self.match("WHILE"):
            self.current -= 1
            return self.while_stmt()
        elif self.match("BREAK"):
            self.consume("SEMI", "Se esperaba ';' después de break")
            return Break()
        elif self.match("CONTINUE"):
            self.consume("SEMI", "Se esperaba ';' después de continue")
            return Continue()
        elif self.match("RETURN"):
            expr = self.expression()
            self.consume("SEMI", "Se esperaba ';' después de return")
            return Return(expr)
        elif self.match("PRINT"):
            expr = self.expression()
            self.consume("SEMI", "Se esperaba ';' después de print")
            return Print(expr)
        else:
            expr = self.expression()
            self.consume("SEMI", "Se esperaba ';' después de la expresión")
            return expr


    def check(self, token_type):
        token = self.peek()
        return token and token.type == token_type

    def assignment(self):
        location = self.location()
        self.consume("ASSIGN", "Se esperaba '=' en asignación")
        expr = self.expression()
        self.consume("SEMI", "Se esperaba ';' al final de la asignación")
        return Assignment(location, expr)

    def vardecl(self):
        is_const = self.match("CONST")
        if not is_const:
            self.consume("VAR", "Se esperaba 'var' o 'const'")
        id_token = self.consume("IDENTIFIER", "Se esperaba nombre de variable")
        type_ = None
        if self.match("INT") or self.match("FLOAT_TYPE") or self.match("CHAR_TYPE") or self.match("BOOL_TYPE"):
            type_ = self.tokens[self.current - 1].type
        expr = None
        if self.match("ASSIGN"):
            expr = self.expression()
        self.consume("SEMI", "Se esperaba ';' al final de la declaración")
        return Variable(id_token.value, type_, expr, is_const)

    def expression(self):
        return self.binary_op(["LOR"], self.orterm)

    def orterm(self):
        return self.binary_op(["LAND"], self.andterm)

    def andterm(self):
        return self.binary_op(["LT", "GT", "LE", "GE", "EQ", "NE"], self.relterm)

    def relterm(self):
        return self.binary_op(["PLUS", "MINUS"], self.addterm)

    def addterm(self):
        return self.binary_op(["TIMES", "DIVIDE"], self.factor)

    def binary_op(self, operators, next_rule):
        expr = next_rule()
        while self.peek() and self.peek().type in operators:
            op_token = self.advance()
            right = next_rule()
            expr = BinOp(expr, op_token.type, right)
        return expr

    def factor(self):
        token = self.peek()

        if token.type in ["INTEGER", "FLOAT", "CHAR", "TRUE", "FALSE"]:
            self.advance()
            if token.type == "INTEGER":
                return Integer(token.value)
            elif token.type == "FLOAT":
                return Float(token.value)
            elif token.type == "CHAR":
                return Char(token.value)
            else:
                return Bool(token.type == "TRUE")
            
        elif token.type in ["PLUS", "MINUS", "GROW"]:
            self.advance()
            return UnaryOp(token.type, self.expression())
        
        elif token.type == "LPAREN":
            self.advance()
            expr = self.expression()
            self.consume("RPAREN", self.EXPECTED_RPAREN_MSG)
            return expr
        
        elif token.type in ["INT", "FLOAT_TYPE", "CHAR_TYPE", "BOOL_TYPE", "INT", "FLOAT", "CHAR", "BOOL"]:
            type_token = self.advance()
            self.consume("LPAREN", "Se esperaba '(' para cast")
            expr = self.expression()
            self.consume("RPAREN", "Se esperaba ')' en cast")
            return TypeCast(type_token.type, expr)

        elif token.type == "IDENTIFIER":
            if self.current + 1 < len(self.tokens) and self.tokens[self.current + 1].type == "LPAREN":
                return self.func_call()
            else:
                return self.location()
            
        elif token.type == "DEREF":
            self.advance()
            return NamedLocation(self.expression())
        
        raise SyntaxError(f"Línea {token.lineno}: Factor no reconocido")

    def func_call(self):
        id_token = self.consume("IDENTIFIER", "Se esperaba nombre de función")
        self.consume("LPAREN", "Se esperaba '('")
        args = self.arguments()
        self.consume("RPAREN", self.EXPECTED_RPAREN_MSG)
        return FunctionCall(id_token.value, args)

    def location(self):
        if self.match("DEREF"):
            expr = self.expression()
            return MemoryLocation(expr)
        else:
            id_token = self.consume("IDENTIFIER", "Se esperaba identificador")
            return NamedLocation(id_token.value)

    def arguments(self):
        args = []
        if not self.peek() or self.peek().type == "RPAREN":
            return args
        args.append(self.expression())
        while self.match("COMMA"):
            args.append(self.expression())
        return args

    def peek(self):
        return self.tokens[self.current] if self.current < len(self.tokens) else None

    def advance(self):
        token = self.peek()
        self.current += 1
        return token

    def match(self, token_type):
        if self.peek() and self.peek().type == token_type:
            self.advance()
            return True
        return False

    def consume(self, token_type, message):
        if self.match(token_type):
            return self.tokens[self.current - 1]
        token = self.peek()
        lineno = token.lineno if token else "EOF"
        raise SyntaxError(f"Línea {lineno}: {message}")

    def funcdecl(self):
        TOKEN_TO_TYPE = {
            "INT": "int",
            "FLOAT_TYPE": "float",
            "CHAR_TYPE": "char",
            "BOOL_TYPE": "bool"
        }

        import_stmt = None
        if self.match("IMPORT"):
            import_stmt = True
        self.consume("FUNC", "Se esperaba 'func'")
        id_token = self.consume("IDENTIFIER", "Se esperaba nombre de la función")
        self.consume("LPAREN", "Se esperaba '('")
        params = self.parameters()
        self.consume("RPAREN", self.EXPECTED_RPAREN_MSG)
        type_ = None
        type_token = self.peek()
        if type_token and type_token.type in TOKEN_TO_TYPE:
            type_ = TOKEN_TO_TYPE[type_token.type]
            self.consume(type_token.type, "Se esperaba tipo de retorno")
        else:
            raise SyntaxError(f"Línea {type_token.lineno if type_token else 'EOF'}: Se esperaba tipo de retorno explícito después de los parámetros de la función")

        self.consume("LBRACE", self.EXPECTED_LBRACE_MSG)
        body = []
        while self.peek() and self.peek().type != "RBRACE":
            body.append(self.statement())
        self.consume("RBRACE", self.EXPECTED_RBRACE_MSG)
        return Function(id_token.value, params, type_, body)


    def parameters(self):
        params = []
        if self.peek() and self.peek().type == "IDENTIFIER":
            while True:
                id_token = self.consume("IDENTIFIER", "Se esperaba nombre del parámetro")
                if self.peek() and self.peek().type in ["INT", "FLOAT_TYPE", "CHAR_TYPE", "BOOL_TYPE"]:
                    type_token = self.consume(self.peek().type, "Se esperaba tipo")
                else:
                    raise SyntaxError(f"Línea {self.peek().lineno if self.peek() else 'EOF'}: Se esperaba tipo para el parámetro")
                params.append(Parameter(id_token.value, type_token.type))
                if not self.match("COMMA"):
                    break
        return params


    def if_stmt(self):
        self.consume("IF", "Se esperaba 'if'")
        condition = self.expression()
        self.consume("LBRACE", self.EXPECTED_LBRACE_MSG)
        then_branch = []
        while self.peek() and self.peek().type != "RBRACE":
            then_branch.append(self.statement())
        self.consume("RBRACE", self.EXPECTED_RBRACE_MSG)

        else_branch = []
        if self.match("ELSE"):
            self.consume("LBRACE", "Se esperaba '{' después de 'else'")
            while self.peek() and self.peek().type != "RBRACE":
                else_branch.append(self.statement())
            self.consume("RBRACE", "Se esperaba '}' en bloque else")

        return If(condition, then_branch, else_branch)

    def while_stmt(self):
        self.consume("WHILE", "Se esperaba 'while'")
        condition = self.expression()
        self.consume("LBRACE", self.EXPECTED_LBRACE_MSG)
        body = []
        while self.peek() and self.peek().type != "RBRACE":
            body.append(self.statement())
        self.consume("RBRACE", self.EXPECTED_RBRACE_MSG)
        return While(condition, body)

class ParserToken:
    def __init__(self, token):
        self.type = token.token_type.name
        self.value = token.literal if token.literal is not None else token.lexeme
        self.lineno = token.line

def error_handler(line, message):
    print(f"[line {line}] Error: {message}")

def ast_to_dict(node):
    if isinstance(node, list):
        return [ast_to_dict(item) for item in node]
    elif hasattr(node, "__dict__"):
        return {key: ast_to_dict(value) for key, value in node.__dict__.items()}
    else:
        return node

def generate_ast_json(self: str, output_path: str = "ast_output.json") -> List:
        scanner = Scanner(self, error_handler)
        tokens = scanner.scan_tokens()
        if scanner.had_error:
            raise SyntaxError("Errores léxicos encontrados")
        wrapped_tokens = [ParserToken(tok) for tok in tokens]
        parser = Parser(wrapped_tokens)
        ast = parser.parse()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(ast_to_dict(ast), f, indent=4)
        return ast


def main():
    if len(sys.argv) != 2:
        print("Uso: python parse.py archivo.gox")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo: {filename}")
        sys.exit(1)
        

    try:
        generate_ast_json(source_code)
        print("AST generado en 'ast_output.json'")
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")
        sys.exit(66)

if __name__ == "__main__":
    main()