
# Gox Parser – Influencias, Decisiones y Pruebas

Este proyecto implementa el analizador sintáctico (parser) para el lenguaje **GoxLang**, inspirado en técnicas formales de construcción de compiladores y con fuerte énfasis en **estructuración por gramática PEG**. A continuación se explica cómo fue diseñado, estructurado, y qué retos surgieron durante su construcción.

---

## Influencia de la Gramática PEG

El parser se construyó tomando como base una **gramática PEG específica para GoxLang**, sin alterarla en ningún momento. Esto significó que el diseño del parser debía respetar al 100% la estructura impuesta por dicha gramática, incluyendo la obligatoriedad de llaves `{}` en funciones, el uso explícito del tipo de retorno, y la necesidad de `;` en cada instrucción.

---

## Estructura y Lógica del Parser

### `parse.py`

Este archivo contiene la clase principal `Parser`, la cual toma una lista de tokens generados por el lexer y construye el árbol de sintaxis abstracta (AST) según la estructura del lenguaje.

### Principales métodos implementados

- `parse()`: Punto de entrada general. Itera sobre los tokens y recolecta todas las sentencias del programa.
- `statement()`: Determina el tipo de sentencia que sigue según el token actual (asignación, declaración, flujo, etc.)
- `expression()`: Maneja expresiones binarias y unarias, con respeto estricto a la precedencia de operadores.
- `factor()`: Interpreta valores literales, castings, llamadas a función y ubicaciones.
- `vardecl()`, `funcdecl()`, `if_stmt()`, `while_stmt()`: Métodos dedicados para cada estructura de control o declaración.

---

## Modelo AST

Las clases del AST están definidas en el archivo `model.py`. Estas clases representan:

- Literales: `Integer`, `Float`, `Char`, `Bool`
- Operaciones: `BinOp`, `UnaryOp`
- Sentencias: `Assignment`, `Print`, `Return`, `Break`, `Continue`, `If`, `While`, `Function`, `Variable`, etc.
- Accesos: `NamedLocation`, `TypeCast`, `Function` (llamada)

---

## Problemas encontrados durante el desarrollo

### Precedencia y errores de factor

Inicialmente, al no validar bien los tokens en `factor()`, se generaban errores crípticos cuando un cast o llamada era ambigua. Se resolvió dando prioridad al reconocimiento de tipos antes que a funciones.

### Manejo de negativos

El parser originalmente esperaba que los números negativos fueran entregados como `INTEGER -1`. Pero eso contradice la PEG. Se corrigió el lexer para emitir `MINUS` + `INTEGER`, y el parser ahora los analiza correctamente como operadores unarios (`UnaryOp(MINUS, Integer(1))`).

### Llamadas sin punto y coma

Una fuente común de errores fue olvidar el `;` después de expresiones como `funcCall();`. El parser detecta estas situaciones y lanza errores explícitos, como `Se esperaba ';' después de la expresión`.

### Importación de funciones

La gramática exige que toda declaración de función, incluso las externas con `import`, contenga llaves `{}`. Esto se mantuvo aunque contradiga las convenciones de otros lenguajes.

---

## Pruebas y Estado Actual

El parser ha sido probado exhaustivamente con funciones unitarias usando `unittest`, incluyendo:

✅ Declaraciones `var` y `const`  
✅ Asignaciones  
✅ Operadores binarios y unarios  
✅ Casting de tipos  
✅ Sentencias de control (`if`, `while`, `break`, `continue`, `return`)  
✅ Funciones con y sin parámetros  
✅ Detección de errores sintácticos precisos

---

## Conclusión

Este parser es un módulo sólido y estricto conforme a la gramática de GoxLang. Fue construido cuidadosamente para generar un AST usable y compatible con futuras etapas del compilador, como el análisis semántico o la generación de código.

ejecutar parser: python -m parse.parse .\samples\factorize.gox
ejecutar prueba unitaria:  python -m unittest .\test\test_parser.py