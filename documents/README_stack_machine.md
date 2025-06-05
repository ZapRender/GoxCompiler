# Máquina Virtual de Pila (StackMachine) para GoxLang

## Descripción general
------------------

Este archivo contiene la implementación de la máquina virtual que ejecuta el código intermedio (IR) generado por el compilador para GoxLang. La máquina funciona con una pila y un conjunto de instrucciones definidas.

## Componentes principales
-----------------------

- Pila (stack): Almacena valores temporales durante la ejecución.
- Memoria simulada (memory): Diccionario para simular acceso a memoria con POKEI y PEEKI.
- Variables locales y globales: Almacenamiento para variables de ámbito local y global.
- Programa contador (pc): Controla la ejecución de instrucciones.
- Funciones: Ejecución de funciones con pila de llamadas para contextos.

## Instrucciones soportadas
------------------------

- CONSTI: Apilar un entero literal.
- LOCAL_GET/LOCAL_SET: Leer/escribir variable local.
- GLOBAL_GET/GLOBAL_SET: Leer/escribir variable global.
- Operaciones aritméticas: ADDI, SUBI, MULI, DIVI.
- Operadores relacionales: LTI, LEI, GTI, GEI, EQI, NEI.
- PRINTI, PRINTB: Imprimir entero o carácter.
- POKEI: Escribir valor en dirección de memoria.
- PEEKI: Leer valor desde dirección de memoria.
- CALL/RET: Llamar y retornar funciones.
- Control de flujo: IF, ELSE, ENDIF, LOOP, CBREAK, CONTINUE, ENDLOOP.
- GROW: Incrementar dirección para memoria simulada.

## Funcionamiento básico
---------------------

- Cada instrucción manipula la pila, variables, memoria o controla el flujo.
- Los saltos condicionales y bucles se implementan con etiquetas y búsqueda en el código.
- Las llamadas a funciones gestionan contexto y pila de llamadas para recursión y anidación.

## Depuración y monitoreo
----------------------

- Mensajes DEBUG para POKEI y PEEKI para verificar acceso a memoria.
- Mensajes DEBUG para PRINTI para rastrear valores impresos.
- Control de errores para instrucciones no soportadas.

## Uso típico
----------

1. Se carga un módulo IR con funciones y variables globales.
2. Se ejecuta la función 'main' o cualquier función deseada.
3. La máquina procesa instrucciones secuencialmente hasta que finaliza.

## Ejemplo
-------

### La instrucción:

    POKEI

es usada para escribir un valor en memoria, tomando primero la dirección de la pila y luego el valor.

### La instrucción:

    PEEKI

toma una dirección de la pila y apila el valor almacenado en esa dirección para ser usado o impreso.
