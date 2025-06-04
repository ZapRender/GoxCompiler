# ircode.py
'''
Una Máquina Intermedia "Virtual"
================================

Una CPU real generalmente consta de registros y un pequeño conjunto de
códigos de operación básicos para realizar cálculos matemáticos,
cargar/almacenar valores desde memoria y controlar el flujo básico
(ramas, saltos, etc.). Aunque puedes hacer que un compilador genere
instrucciones directamente para una CPU, a menudo es más sencillo
dirigirse a un nivel de abstracción más alto. Una de esas abstracciones
es la de una máquina de pila (stack machine).

Por ejemplo, supongamos que deseas evaluar una operación como esta:

    a = 2 + 3 * 4 - 5

Para evaluar la expresión anterior, podrías generar pseudo-instrucciones
como esta:

    CONSTI 2      ; stack = [2]
    CONSTI 3      ; stack = [2, 3]
    CONSTI 4      ; stack = [2, 3, 4]
    MULI          ; stack = [2, 12]
    ADDI          ; stack = [14]
    CONSTI 5      ; stack = [14, 5]
    SUBI          ; stack = [9]
    LOCAL_SET "a" ; stack = []

Observa que no hay detalles sobre registros de CPU ni nada por el estilo
aquí. Es mucho más simple (un módulo de nivel inferior puede encargarse
del mapeo al hardware más adelante si es necesario).

Las CPUs usualmente tienen un pequeño conjunto de tipos de datos como
enteros y flotantes. Existen instrucciones dedicadas para cada tipo. El
código IR seguirá el mismo principio, admitiendo operaciones con enteros
y flotantes. Por ejemplo:

    ADDI   ; Suma entera
    ADDF   ; Suma flotante

Aunque el lenguaje de entrada podría tener otros tipos como `bool` y
`char`, esos tipos deben ser mapeados a enteros o flotantes. Por ejemplo,
un bool puede representarse como un entero con valores {0, 1}. Un char
puede representarse como un entero cuyo valor sea el mismo que el código
del carácter (es decir, un código ASCII o código Unicode).

Con eso en mente, aquí hay un conjunto básico de instrucciones para
nuestro Código IR:

    ; Operaciones enteras
    CONSTI value             ; Apilar un literal entero
    ADDI                     ; Sumar los dos elementos superiores de la pila
    SUBI                     ; Restar los dos elementos superiores de la pila
    MULI                     ; Multiplicar los dos elementos superiores de la pila
    DIVI                     ; Dividir los dos elementos superiores de la pila
    ANDI                     ; AND bit a bit
    ORI                      ; OR bit a bit
    LTI                      : <
    LEI                      : <=
    GTI                      : >
    GEI                      : >=
    EQI                      : ==
    NEI                      : !=
    PRINTI                   ; Imprimir el elemento superior de la pila
    PEEKI                    ; Leer entero desde memoria (dirección en la pila)
    POKEI                    ; Escribir entero en memoria (valor, dirección en la pila)
    ITOF                     ; Convertir entero a flotante

    ; Operaciones en punto flotante
    CONSTF value             ; Apilar un literal flotante
    ADDF                     ; Sumar los dos elementos superiores de la pila
    SUBF                     ; Restar los dos elementos superiores de la pila
    MULF                     ; Multiplicar los dos elementos superiores de la pila
    DIVF                     ; Dividir los dos elementos superiores de la pila
    LTF                      : <
    LEF                      : <=
    GTF                      : >
    GEF                      : >=
    EQF                      : ==
    NEF                      : !=
    PRINTF                   ; Imprimir el elemento superior de la pila
    PEEKF                    ; Leer flotante desde memoria (dirección en la pila)
    POKEF                    ; Escribir flotante en memoria (valor, dirección en la pila)
    FTOI                     ; Convertir flotante a entero

    ; Operaciones orientadas a bytes (los valores se presentan como enteros)
    PRINTB                   ; Imprimir el elemento superior de la pila
    PEEKB                    ; Leer byte desde memoria (dirección en la pila)
    POKEB                    ; Escribir byte en memoria (valor, dirección en la pila)

    ; Carga/almacenamiento de variables.
    ; Estas instrucciones leen/escriben variables locales y globales. Las variables
    ; son referenciadas por algún tipo de nombre que las identifica. La gestión
    ; y declaración de estos nombres también debe ser manejada por tu generador de código.
    ; Sin embargo, las declaraciones de variables no son una instrucción normal. En cambio,
    ; es un tipo de dato que debe asociarse con un módulo o función.
    LOCAL_GET name           ; Leer una variable local a la pila
    LOCAL_SET name           ; Guardar una variable local desde la pila
    GLOBAL_GET name          ; Leer una variable global a la pila
    GLOBAL_SET name          ; Guardar una variable global desde la pila

    ; Llamadas y retorno de funciones.
    ; Las funciones se referencian por nombre. Tu generador de código deberá
    ; encontrar alguna manera de gestionar esos nombres.
    CALL name                ; Llamar función. Todos los argumentos deben estar en la pila
    RET                      ; Retornar de una función. El valor debe estar en la pila

    ; Control estructurado de flujo
    IF                       ; Comienza la parte "consecuencia" de un "if". Prueba en la pila
    ELSE                     ; Comienza la parte "alternativa" de un "if"
    ENDIF                    ; Fin de una instrucción "if"

    LOOP                     ; Inicio de un ciclo
    CBREAK                   ; Ruptura condicional. Prueba en la pila
    CONTINUE                 ; Regresa al inicio del ciclo
    ENDLOOP                  ; Fin del ciclo

    ; Memoria
    GROW                     ; Incrementar memoria (tamaño en la pila) (retorna nuevo tamaño)

Una palabra sobre el acceso a memoria... las instrucciones PEEK y POKE
se usan para acceder a direcciones de memoria cruda. Ambas instrucciones
requieren que una dirección de memoria esté en la pila *primero*. Para
la instrucción POKE, el valor a almacenar se apila después de la dirección.
El orden es importante y es fácil equivocarse. Así que presta mucha
atención a eso.

Su tarea
=========
Su tarea es la siguiente: Escribe código que recorra la estructura del
programa y la aplane a una secuencia de instrucciones representadas como
tuplas de la forma:

       (operation, operands, ...)

Por ejemplo, el código del principio podría terminar viéndose así:

    code = [
       ('CONSTI', 2),
       ('CONSTI', 3),
       ('CONSTI', 4),
       ('MULI',),
       ('ADDI',),
       ('CONSTI', 5),
       ('SUBI',),
       ('LOCAL_SET', 'a'),
    ]

Funciones
=========
Todo el código generado está asociado con algún tipo de función. Por
ejemplo, con una función definida por el usuario como esta:

    func fact(n int) int {
        var result int = 1;
        var x int = 1;
        while x <= n {
            result = result * x;
            x = x + 1;
        }
     }

Debes crear un objeto `Function` que contenga el nombre de la función,
los argumentos, el tipo de retorno, las variables locales y un cuerpo
que contenga todas las instrucciones de bajo nivel. Nota: en este nivel,
los tipos representarán tipos IR de bajo nivel como Integer (I) y Float (F).
No son los mismos tipos usados en el código GoxLang de alto nivel.

Además, todo el código que se define *fuera* de una función debe ir
igualmente en una función llamada `_init()`. Por ejemplo, si tienes
declaraciones globales como esta:

     const pi = 3.14159;
     const r = 2.0;
     print pi*r*r;

Tu generador de código debería en realidad tratarlas así:

     func _init() int {
         const pi = 3.14159;
         const r = 2.0;
         print pi*r*r;
         return 0;
     }

En resumen: todo el código debe ir dentro de una función.

Módulos
=======
La salida final de la generación de código debe ser algún tipo de
objeto `Module` que contenga todo. El módulo incluye objetos de función,
variables globales y cualquier otra cosa que puedas necesitar para
generar código posteriormente.
'''
from rich   import print
from typing import List

from parse.model  import Assignment, Print, If, While, Break, Continue, Return, Visitor , Variable, Function, Integer, Float, Char, Bool, BinOp, UnaryOp, TypeCast, FunctionCall, NamedLocation, MemoryLocation
from parse.parse import generate_ast_json
from semantic.check import Checker

class Visitor:
    def visit(self, node, env):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def generic_visit(self, node, env):
        raise Exception(f'No visit method defined for {node.__class__.__name__}')

class IRModule:
    def __init__(self):
        self.functions = {}
        self.globals = {}

    def add_global(self, name, type_):
        self.globals[name] = IRGlobal(name, type_)

    def dump(self):
        print("MODULE:::")
        for glob in self.globals.values():
            glob.dump()
        for func in self.functions.values():
            func.dump()

class IRGlobal:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def dump(self):
        print(f"GLOBAL::: {self.name}: {self.type}")

class IRFunction:
    def __init__(self, module, name, parmnames, parmtypes, return_type, imported=False):
        self.module = module
        module.functions[name] = self

        self.name = name
        self.parmnames = parmnames
        self.parmtypes = parmtypes
        self.return_type = return_type
        self.imported = imported
        self.locals = {}
        self.code = []

    def new_local(self, name, type):
        self.locals[name] = type

    def append(self, instr):
        self.code.append(instr)

    def extend(self, instructions):
        self.code.extend(instructions)

    def dump(self):
        print(f"FUNCTION::: {self.name}, {self.parmnames}, {self.parmtypes} {self.return_type}")
        print(f"locals: {self.locals}")
        for instr in self.code:
            print(instr)

_typemap = {
    'int': 'I',
    'float': 'F',
    'bool': 'I',
    'char': 'I',
}

class IRCode(Visitor):
    _binop_code = {
        ('int', '+', 'int'): 'ADDI',
        ('int', '-', 'int'): 'SUBI',
        ('int', '*', 'int'): 'MULI',
        ('int', '/', 'int'): 'DIVI',
        ('int', '<', 'int'): 'LTI',
        ('int', '<=', 'int'): 'LEI',
        ('int', '>', 'int'): 'GTI',
        ('int', '>=', 'int'): 'GEI',
        ('int', '==', 'int'): 'EQI',
        ('int', '!=', 'int'): 'NEI',

        ('float', '+', 'float'): 'ADDF',
        ('float', '-', 'float'): 'SUBF',
        ('float', '*', 'float'): 'MULF',
        ('float', '/', 'float'): 'DIVF',
        ('float', '<', 'float'): 'LTF',
        ('float', '<=', 'float'): 'LEF',
        ('float', '>', 'float'): 'GTF',
        ('float', '>=', 'float'): 'GEF',
        ('float', '==', 'float'): 'EQF',
        ('float', '!=', 'float'): 'NEF',

        ('char', '<', 'char'): 'LTI',
        ('char', '<=', 'char'): 'LEI',
        ('char', '>', 'char'): 'GTI',
        ('char', '>=', 'char'): 'GEI',
        ('char', '==', 'char'): 'EQI',
        ('char', '!=', 'char'): 'NEI',
    }

    _unaryop_code = {
        ('+', 'int'): [],
        ('-', 'int'): [('CONSTI', -1), ('MULI',)],
        ('!', 'bool'): [('CONSTI', -1), ('MULI',)],
        ('^', 'int'): [('GROW',)],
    }

    _typecast_code = {
        ('int', 'float'): [('ITOF',)],
        ('float', 'int'): [('FTOI',)],
    }

    @classmethod
    def gencode(cls, node: List):
        ircode = cls()
        module = IRModule()

        # Registrar variables globales
        for item in node:
            if isinstance(item, Variable):
                module.add_global(item.name, _typemap.get(item.type, 'I'))

        # Crear función main para código global
        func_main = IRFunction(module, 'main', [], [], 'I')

        # Inicializar variables globales
        for item in node:
            if isinstance(item, Variable):
                item.accept(ircode, func_main)

        # Generar código para funciones y otras sentencias globales
        for item in node:
            if not isinstance(item, Variable):
                item.accept(ircode, func_main)

        func_main.append(('CONSTI', 0))
        func_main.append(('RET',))

        return module





    def visit_Assignment(self, n: Assignment, func: IRFunction):
        n.expression.accept(self, func)

        if isinstance(n.location, NamedLocation):
            name = n.location.name_or_expr
            if name in func.locals:
                func.append(('LOCAL_SET', name))
            elif name in func.module.globals:
                func.append(('GLOBAL_SET', name))
            else:
                func.append(('LOCAL_SET', name))
        elif isinstance(n.location, MemoryLocation):
            n.location.address.accept(self, func)
            func.append(('POKEI',))
        else:
            raise Exception(f"Ubicación de asignación no soportada: {type(n.location)}")

    def visit_Print(self, n: Print, func: IRFunction):
        n.expression.accept(self, func)
        # Diferencia impresión para chars
        if isinstance(n.expression, Char):
            func.append(('PRINTB',))
        else:
            func.append(('PRINTI',))

    def visit_If(self, n: If, func: IRFunction):
        n.condition.accept(self, func)
        func.append(('IF',))
        for stmt in n.then_branch:
            stmt.accept(self, func)
        func.append(('ELSE',))
        for stmt in n.else_branch:
            stmt.accept(self, func)
        func.append(('ENDIF',))

    def visit_While(self, n: While, func: IRFunction):
        func.append(('LOOP',))
        n.condition.accept(self, func)
        func.append(('CBREAK',))
        for stmt in n.body:
            stmt.accept(self, func)
        func.append(('ENDLOOP',))

    def visit_Break(self, n: Break, func: IRFunction):
        func.append(('CBREAK',))

    def visit_Continue(self, n: Continue, func: IRFunction):
        func.append(('CONTINUE',))

    def visit_Return(self, n: Return, func: IRFunction):
        n.expression.accept(self, func)
        func.append(('RET',))

    def visit_Variable(self, n: Variable, func: IRFunction):
        # Solo variables con var dentro de funciones como locales
        if func.name != '_actual_main':
            func.new_local(n.name, _typemap.get(n.type, 'I'))
            if n.expression:
                n.expression.accept(self, func)
                func.append(('LOCAL_SET', n.name))
        else:
            # Variables globales se inicializan en _actual_main
            if n.expression:
                n.expression.accept(self, func)
                func.append(('GLOBAL_SET', n.name))

    def visit_Function(self, n: Function, func: IRFunction):
        module = func.module
        parmnames = [p.name for p in n.params]
        parmtypes = [_typemap.get(p.type, 'I') for p in n.params]
        irfunc = IRFunction(module, n.name, parmnames, parmtypes, _typemap.get(n.return_type, 'I'))
        for stmt in n.body:
            if isinstance(stmt, Variable):
                irfunc.new_local(stmt.name, _typemap.get(stmt.type, 'I'))
        for stmt in n.body:
            stmt.accept(self, irfunc)
        irfunc.append(('CONSTI', 0))
        irfunc.append(('RET',))


    def visit_Integer(self, n: Integer, func: IRFunction):
        func.append(('CONSTI', n.value))

    def visit_Float(self, n: Float, func: IRFunction):
        func.append(('CONSTF', n.value))

    def visit_Char(self, n: Char, func: IRFunction):
        func.append(('CONSTI', ord(n.value)))

    def visit_Bool(self, n: Bool, func: IRFunction):
        func.append(('CONSTI', 1 if n.value else 0))

    def visit_BinOp(self, n: BinOp, func: IRFunction):
        OP_MAP = {
            'PLUS': '+',
            'MINUS': '-',
            'TIMES': '*',
            'DIVIDE': '/',
            'LT': '<',
            'LE': '<=',
            'GT': '>',
            'GE': '>=',
            'EQ': '==',
            'NE': '!=',
            'LAND': '&&',
            'LOR': '||',
        }
        n.left.accept(self, func)
        n.right.accept(self, func)
        left_type = 'int'  # Simplificación
        right_type = 'int'
        op = OP_MAP.get(n.op, n.op)
        ir_instr = self._binop_code.get((left_type, op, right_type))
        if ir_instr is None:
            raise Exception(f"Operación binaria no soportada: {left_type} {op} {right_type}")
        func.append((ir_instr,))

    def visit_UnaryOp(self, n: UnaryOp, func: IRFunction):
        n.expr.accept(self, func)
        if n.op == 'GROW' or n.op == '^':
            func.append(('GROW',))
            return
        ops = self._unaryop_code.get((n.op, 'int'))  # Simplificado
        if ops is None:
            raise Exception(f"Operador unario no soportado: {n.op}")
        for op in ops:
            func.append(op)

    def visit_TypeCast(self, n: TypeCast, func: IRFunction):
        n.expr.accept(self, func)
        ops = self._typecast_code.get(('int', 'float'))  # Simplificado
        if ops:
            for op in ops:
                func.append(op)

    def visit_FunctionCall(self, n: FunctionCall, func: IRFunction):
        for arg in n.args:
            arg.accept(self, func)
        func.append(('CALL', n.name))

    def visit_NamedLocation(self, n: NamedLocation, func: IRFunction):
        if isinstance(n.name_or_expr, str):
            if n.name_or_expr in func.locals:
                func.append(('LOCAL_GET', n.name_or_expr))
            elif n.name_or_expr in func.module.globals:
                func.append(('GLOBAL_GET', n.name_or_expr))
            else:
                func.append(('LOCAL_GET', n.name_or_expr))
        else:
            n.name_or_expr.accept(self, func)

    def visit_MemoryLocation(self, n: MemoryLocation, func: IRFunction):
        n.address.accept(self, func)
        func.append(('PEEKI',))





import sys

def main(filename):
    with open(filename, encoding='utf-8') as f:
        source_code = f.read()

    # Generar AST (y opcionalmente guardar JSON)
    ast = generate_ast_json(source_code)
    
    try:
        generate_ast_json(source_code)
        print("[bold green]AST generado en 'ast_output.json'")
        # Analizar semánticamente
        checker = Checker.check(ast)
        if checker.errors:
            print("Errores semánticos detectados, no se genera código intermedio.")
            return
        module = IRCode.gencode(ast)
        module.dump()
            
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")
        sys.exit(66)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.gox")
        sys.exit(1)
    main(sys.argv[1])