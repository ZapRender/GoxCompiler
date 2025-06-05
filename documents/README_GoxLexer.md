# Gox Lexer - Influencias, Decisiones y Pruebas

Este proyecto toma inspiración directa del capítulo **"Scanning"** del libro *Crafting Interpreters*. A continuación explico cómo fue el proceso de interpretación, adaptación y desarrollo del lexer de Gox.

---

## Influencia del Libro

El capítulo del libro está escrito en Java, lo que representó un reto inicial. Sin embargo, logré reinterpretar y traducir su enfoque a Python, respetando la lógica y estructura general del escáner.

---

## Estructura y Lógica del Lexer

### TokenType.py

Inspirado en el uso de `enum class` del libro, utilicé un enfoque similar en Python para organizar los tipos de tokens. Sin embargo, para lograr un mapeo más preciso y eficiente, incorporé diccionarios. Aquí están los tres diccionarios clave:

- **`SINGLE_CHAR_TOKENS`**:  
  Define tokens individuales, es decir, aquellos formados por un solo carácter.

- **`TOKEN_LITERALS`**:  
  Incluye literales e identificadores utilizados durante el escaneo.

- **`KEYWORDS`**:  
  Contiene las palabras clave que forman parte del lenguaje Gox.

---

### lexer.py

En este archivo se encuentra la clase principal `Gox`, encargada de iniciar y controlar el escaneo.

#### Método `_runFile`

Este método abre el archivo en **modo lectura binaria (`rb`)**, decodificando luego el contenido en una cadena de caracteres.  
Aunque inicialmente utilicé este enfoque para seguir el libro, descubrí que este modo asegura la lectura exacta de los bytes. Aun así, algunos foros recomiendan utilizar `rb` solamente con archivos binarios, no con archivos de texto. ¡Algo a considerar!

---

## Problemas que tuve durante el proceso

Durante el desarrollo de las **pruebas unitarias**, surgieron algunos problemas interesantes:

### Manejo de Números Negativos

El lexer no estaba reconociendo los números negativos correctamente. El símbolo `-` era identificado como un token separado, no como parte del número. Tuve que ajustar el código para que los números negativos fueran tratados como enteros completos.

### Manejo de Cadenas de Texto

Otro detalle surgió al probar el manejo de cadenas: el lexer las dividía **carácter por carácter** en lugar de reconocerlas como un solo *lexeme*.  
Después de corregirlo, ahora las cadenas completas son reconocidas correctamente como una sola unidad.

---

## Estado Actual

El scanner ahora es capaz de:

- Identificar correctamente los tokens simples, literales y palabras clave.
- Leer archivos en modo binario para mayor precisión.
- Tratar correctamente números negativos.
- Agrupar cadenas de texto como un solo token.

---

