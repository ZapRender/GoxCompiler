from scanner import Scanner

class Gox:
    def __init__(self):
        # Indica si se encontró un error en el código.
        self.hadError = False

    def _run(self, content: str):
        # Se pasa self.errorHandler para que el Scanner notifique errores.
        scanner = Scanner(content, self.errorHandler)
        tokens = scanner.scanTokens()
        
        for token in tokens:
            print(token.toString())
        
        # Si se detectó un error en el escaneo, lo marcamos aquí.
        if scanner.hadError:
            self.hadError = True

    def _runFile(self, path):
        try:
            with open(path, 'rb') as file:
                bytes_content = file.read()
            content = bytes_content.decode()
            self._run(content)
            
            if self.hadError:
                exit(65)
        except (TypeError, ValueError) as e:
            print(f"Error: {e}")
            exit(1)

    def errorHandler(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        self.hadError = True

if __name__ == "__main__":
    gox = Gox()
    gox._runFile("factorize.gox")
