from scanner import *

class Gox:
    def __init__(self):
        #This argument indicate that found an error in the code.
        self.hadError = False

    def _run(self, content: str):
        scanner = Scanner(content)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token.toString())

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