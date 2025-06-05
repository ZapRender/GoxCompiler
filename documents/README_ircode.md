# Generador de Código Intermedio (IRCode) para GoxLang

## Descripción general
------------------

El archivo ircode.py contiene una implementación de un generador de código intermedio para el lenguaje GoxLang. Convierte el Árbol de Sintaxis Abstracta (AST) del programa en instrucciones de bajo nivel que serán ejecutadas por una máquina virtual de pila (StackMachine).

## Componentes principales
-----------------------

- IRModule: Representa el módulo completo, conteniendo funciones y variables globales.
- IRGlobal: Representa variables globales con nombre y tipo.
- IRFunction: Representa una función con nombre, argumentos, tipo de retorno, variables locales y cuerpo de instrucciones IR.

### Mapeo de tipos (_typemap)
-------------------------

Traduce los tipos del lenguaje GoxLang a tipos IR básicos: entero (I), flotante (F), booleano y carácter a entero.

### Clase principal: IRCode
----------------------

Hereda de un visitante genérico para recorrer el AST. Para cada tipo de nodo AST, genera la secuencia de instrucciones IR correspondiente.

### Métodos importantes

- gencode(node: List)
  Función principal para generar el módulo IR completo desde el AST:  
  1. Registra variables globales.  
  2. Crea una función main donde genera todo el código.  
  3. Inserta instrucciones para inicializar variables globales.  
  4. Genera código para funciones y demás sentencias globales.  
  5. Añade instrucción RET para terminar main.

- visit_Assignment
  Genera código para asignaciones, diferenciando si la asignación es directa (variable local o global) o indirecta (a una dirección de memoria).

- visit_Print
  Genera instrucciones para imprimir valores. Si la expresión es una dirección de memoria (MemoryLocation), primero genera código para cargar el valor apuntado (PEEKI), luego imprime el valor (PRINTI o PRINTB).

- visit_If, visit_While, visit_Break, visit_Continue, visit_Return
  Genera instrucciones para control de flujo y manejo de ciclos.

- visit_Variable
  Diferencia variables locales y globales, generando instrucciones para inicializar y asignar valores.

- visit_Function
  Crea un objeto IRFunction para cada función, registra variables locales y genera instrucciones para el cuerpo.

- visit_Integer, visit_Float, visit_Char, visit_Bool
  Genera instrucciones para literales.

- visit_BinOp
  Genera instrucciones aritméticas y lógicas basadas en operadores binarios.

- visit_UnaryOp
  Genera instrucciones para operadores unarios.

- visit_TypeCast
  Maneja conversiones entre tipos (entero a flotante y viceversa).

- visit_FunctionCall
  Genera llamadas a funciones, apilando argumentos y emitiendo la instrucción CALL.

- visit_NamedLocation
  Para acceder a variables locales o globales.

- visit_MemoryLocation
  Genera instrucciones para acceso indirecto a memoria (PEEKI).

Consideraciones específicas
----------------------------

- Acceso a memoria: El generador genera la dirección primero (apilándola) y luego el valor, para usar instrucciones POKEI o PEEKI según corresponda.
- Diferenciación entre variables locales y globales: Variables globales usan instrucciones GLOBAL_GET/GLOBAL_SET, locales usan LOCAL_GET/LOCAL_SET.
- Control de flujo: Usa instrucciones IR específicas (IF, ELSE, ENDIF, LOOP, CBREAK, etc.) para implementar estructuras if y while.

## Flujo típico
-----------

1. Recibe AST generado por el parser.
2. Registra variables globales.
3. Crea la función main y otras funciones definidas por el usuario.
4. Para cada nodo del AST, genera las instrucciones IR correspondientes.
5. Devuelve el módulo IR listo para ser ejecutado por la máquina virtual.

### Ejemplo
-------

Para la instrucción GoxLang:

    print `(base + i);

El generador emitirá algo como:

    GLOBAL_GET base
    GLOBAL_GET i
    ADDI
    PEEKI
    PRINTI

Donde primero calcula la dirección base + i, luego obtiene el valor en memoria (PEEKI), y finalmente imprime el valor (PRINTI).
