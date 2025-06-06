import sys
from lexer.scanner import Scanner

class Gox:
    def __init__(self):
        self.had_error = False

    def _run(self, content: str):
        scanner = Scanner(content, self.error_handler)
        tokens = scanner.scan_tokens()

        # print the tokens
        for token in tokens:
            print(token.to_string())

        if scanner.had_error:
            self.had_error = True

    def _run_file(self, path):
        try:
            with open(path, 'rb') as file:
                bytes_content = file.read()
            content = bytes_content.decode()
            self._run(content)
        except (TypeError, ValueError) as e:
            print(f"Error: {e}")
            exit(1)


    def error_handler(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        self.had_error = True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit(1)
    file_path = sys.argv[1]
    gox = Gox()
    gox._run_file(file_path)
    
    if gox.had_error:
        exit(65)
