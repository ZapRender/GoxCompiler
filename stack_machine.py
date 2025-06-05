class StackMachine:
    def __init__(self, module):
        self.module = module
        self.stack = []
        self.globals = {name: 0 for name in module.globals}
        self.locals = {}
        self.pc = 0
        self.current_func = None
        self.running = False
        self.call_stack = []
        self.memory = {}  # Simulación de memoria para POKEI y PEEKI

    def prepare_labels(self):
        self.labels = {
            'IF': [],
            'ELSE': [],
            'ENDIF': [],
            'LOOP': [],
            'ENDLOOP': [],
            'CBREAK': [],
            'CONTINUE': []
        }
        for i, instr in enumerate(self.current_func.code):
            op = instr[0]
            if op in self.labels:
                self.labels[op].append(i)

    def run_function(self, func_name, args=None):
        if args is None:
            args = []

        # Guardar contexto actual sólo si hay función activa
        if self.current_func is not None:
            self.call_stack.append((self.current_func, self.locals, self.pc))

        # Iniciar nuevo contexto
        self.current_func = self.module.functions[func_name]
        self.locals = {}
        for name, val in zip(self.current_func.parmnames, args):
            self.locals[name] = val
        self.pc = 0
        self.running = True
        self.prepare_labels()

        while self.running and self.pc < len(self.current_func.code):
            instr = self.current_func.code[self.pc]
            self.execute(instr)
            self.pc += 1

        # Restaurar contexto anterior si existe
        if self.call_stack:
            self.current_func, self.locals, self.pc = self.call_stack.pop()
            self.running = True
        else:
            self.running = False  # Fin del programa


    def execute(self, instr):
        op = instr[0]
        args = instr[1:] if len(instr) > 1 else []

        if op == 'CONSTI':
            self.stack.append(args[0])

        elif op == 'LOCAL_GET':
            self.stack.append(self.locals[args[0]])

        elif op == 'GLOBAL_GET':
            self.stack.append(self.globals[args[0]])

        elif op == 'LOCAL_SET':
            val = self.stack.pop()
            self.locals[args[0]] = val

        elif op == 'GLOBAL_SET':
            val = self.stack.pop()
            self.globals[args[0]] = val

        elif op == 'ADDI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)

        elif op == 'SUBI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)

        elif op == 'MULI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a * b)

        elif op == 'DIVI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a // b if b != 0 else 0)

        elif op == 'LTI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a < b else 0)

        elif op == 'LEI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a <= b else 0)

        elif op == 'GTI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a > b else 0)

        elif op == 'GEI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a >= b else 0)

        elif op == 'EQI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a == b else 0)

        elif op == 'NEI':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a != b else 0)

        elif op == 'CALL':
            func_name = args[0]
            func = self.module.functions[func_name]
            nargs = len(func.parmnames)
            call_args = [self.stack.pop() for _ in range(nargs)][::-1]
            self.run_function(func_name, call_args)

        elif op == 'RET':
            self.running = False

        elif op == 'PRINTI':
            val = self.stack.pop()
            print(val, end='\n')

        elif op == 'PRINTB':
            val = self.stack.pop()
            print(chr(val), end='')

        elif op == 'GROW':
            addr = self.stack.pop()
            self.stack.append(addr + 1)

        elif op == 'POKEI':
            val = self.stack.pop()
            addr = self.stack.pop()
            self.memory[addr] = val

        elif op == 'PEEKI':
            addr = self.stack.pop()
            val = self.memory.get(addr, 0)
            self.stack.append(val)

        elif op == 'IF':
            cond = self.stack.pop()
            if cond == 0:
                self.pc = self.find_next('ELSE', self.pc)

        elif op == 'ELSE':
            self.pc = self.find_next('ENDIF', self.pc)

        elif op == 'ENDIF':
            pass

        elif op == 'LOOP':
            self.loop_start = self.pc

        elif op == 'ENDLOOP':
            self.pc = self.loop_start - 1

        elif op == 'CBREAK':
            cond = self.stack.pop()
            if cond == 0:
                self.pc = self.find_next('ENDLOOP', self.pc)

        elif op == 'CONTINUE':
            self.pc = self.loop_start - 1

        else:
            raise Exception(f"Instrucción no soportada: {op}")

    def find_next(self, label, from_idx):
        for i in range(from_idx + 1, len(self.current_func.code)):
            if self.current_func.code[i][0] == label:
                return i
        raise Exception(f"No se encontró la etiqueta {label}")
