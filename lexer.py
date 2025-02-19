import sys
from scanner import Scanner

class Gox:
    def __init__(self):
        self.hadError = False

    def _run(self, content: str):
        scanner = Scanner(content, self.errorHandler)
        tokens = scanner.scanTokens()

        # Imprime cada token
        for token in tokens:
            print(token.toString())

        if scanner.hadError:
            self.hadError = True

    def _runFile(self, path):
        try:
            with open(path, 'rb') as file:
                bytes_content = file.read()
            content = bytes_content.decode()
            self._run(content)
        except (TypeError, ValueError) as e:
            print(f"Error: {e}")
            exit(1)

    def errorHandler(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        self.hadError = True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit(1)
    file_path = sys.argv[1]
    gox = Gox()
    gox._runFile(file_path)
    
    if gox.hadError:
        exit(65)
