
import sys
import json
from lexer.scanner import Scanner
from parse.parse import Parser


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

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.gox")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo: {filename}")
        sys.exit(1)

    scanner = Scanner(source_code, error_handler)
    tokens = scanner.scan_tokens()

    if scanner.had_error:
        sys.exit(65)

    wrapped_tokens = [ParserToken(tok) for tok in tokens]
    parser = Parser(wrapped_tokens)

    try:
        ast = parser.parse()
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")
        sys.exit(66)

    ast_json = json.dumps(ast_to_dict(ast), indent=4)

    with open("ast_output.json", "w", encoding="utf-8") as out_file:
        out_file.write(ast_json)

    print("AST generado en 'ast_output.json'")

if __name__ == "__main__":
    main()
