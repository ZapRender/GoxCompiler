import sys
import json
from semantic.check import Checker
from parse.parse import generate_ast_json
import rich

def main():
    if len(sys.argv) != 2:
        print("Uso: python main_semantic.py archivo.gox")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo: {filename}")
        sys.exit(1)

    try:
        # Generar AST y archivo JSON
        ast = generate_ast_json(source_code)
        rich.print("[bold green]AST generado en 'ast_output.json'")
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")
        sys.exit(66)

    # Ejecutar análisis semántico
    Checker.check(ast)

if __name__ == "__main__":
    main()
