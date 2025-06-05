# Proyecto Compilador GoxLang

## Descripción General

Este proyecto es un compilador para el lenguaje de programación **GoxLang**. El compilador convierte el código fuente escrito en GoxLang en un código intermedio (IR) y lo ejecuta sobre una máquina virtual basada en una máquina de pila (stack machine).

---

## Estructura del Proyecto

```
GoxCompiler/
├── parse/                # Analizador sintáctico (parser) y modelo AST
│   ├── __init__.py
│   ├── model.py          # Definición de nodos AST
│   ├── parse.py          # Generación del AST desde código fuente
│   └── parse_test.py
│
├── semantic/             # Análisis semántico y reglas de chequeo
│   ├── __init__.py
│   ├── check.py          # Chequeo semántico y tabla de símbolos
│   └── error.py
│
├── ircode.py             # Generador de código intermedio (IR)
├── stack_machine.py      # Máquina virtual de pila para ejecutar IR
├── main.py               # Entrada principal para ejecutar el compilador
├── tests/                # Casos de prueba para el compilador
│   └── ...
└── README.md             # Documentación general del proyecto
```

---
## Componentes Principales

### 1. **Análisis Sintáctico y Semántico**

- **Generación del AST**: El compilador primero transforma el código fuente en un Árbol de Sintaxis Abstracta (AST).
- **Chequeo Semántico**: Se realiza la validación semántica para asegurar que el código tenga sentido lógico y cumpla con reglas del lenguaje (tipos, variables, funciones, etc.).

### 2. **Generación de Código Intermedio (IR)**

- Se recorre el AST para generar un conjunto de instrucciones en un lenguaje de bajo nivel, el **Código Intermedio (IR)**.
- Este IR simula instrucciones simples de una máquina virtual, como operaciones aritméticas, acceso a variables, control de flujo y acceso a memoria.
- Se manejan variables locales, globales y acceso indirecto a memoria (a través de direcciones).

### 3. **Máquina de Pila (Stack Machine)**

- Ejecuta las instrucciones del IR usando una pila para gestionar operaciones, llamadas a funciones, control de flujo, y memoria.
- La máquina soporta instrucciones básicas como `CONSTI`, `ADDI`, `POKEI` (escribir en memoria), `PEEKI` (leer de memoria), y control de flujo (`LOOP`, `IF`, etc.).
- Simula un entorno de ejecución para el código generado, permitiendo correr programas GoxLang.

---

## Flujo de Ejecución del Compilador

1. **Lectura del Código Fuente**  
   El programa lee el archivo `.gox` con código en GoxLang.

2. **Generación del AST**  
   Se construye la representación interna (AST) del código.

3. **Chequeo Semántico**  
   Se verifican tipos, variables, declaraciones y otros errores semánticos.

4. **Generación del Código Intermedio (IR)**  
   Se traduce el AST a un módulo IR con funciones, variables globales y locales, y código en instrucciones.

5. **Ejecución del Código IR**  
   La máquina de pila carga el módulo IR y ejecuta la función principal (`main`).

---

## Archivos Clave

- `ircode.py`: Genera el código intermedio (IR) a partir del AST.
- `stack_machine.py`: Ejecuta el código IR simulando una máquina de pila.
- `parse/`: Código relacionado con el parser y construcción del AST.
- `semantic/`: Código para chequeo semántico.

---

## Cómo Usar

1. Escribe tu programa en GoxLang en un archivo `.gox`.
2. Ejecuta el compilador:

```bash
python main samples/program.gox
```

3. El compilador genera el IR, lo imprime para revisión y ejecuta el programa mostrando la salida por consola.

---

## Problemas actuales

- Actualmente se tiene un inconveniente con la asignación de memoria.

