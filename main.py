import sys
from parse.parse import generate_ast_json  # tu función para parsear
from semantic.check import Checker
from ircode import IRCode
from stack_machine import StackMachine
from rich import print

def main():
    try:
        if len(sys.argv) != 2:
            print("Uso: python main.py archivo.gox")
            sys.exit(1)

        filename = sys.argv[1]

        with open(filename, encoding='utf-8') as f:
            source_code = f.read()

        # Parse y análisis semántico
        ast = generate_ast_json(source_code)
        checker = Checker.check(ast)
        if checker.errors:
            print("Errores semánticos detectados, no se genera código intermedio.")
            sys.exit(1)

        # Generar IR
        module = IRCode.gencode(ast)
        module.dump()

        # Ejecutar máquina de pila
        print("[green]========================================")
        machine = StackMachine(module)
        machine.run_function('main')
    except SyntaxError as e:
        print(f"[red]Error de sintaxis: {e}")
        sys.exit(66)

if __name__ == '__main__':
    main()
