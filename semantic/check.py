from rich import print
from typing import Union

from parse.model import *
from semantic.symtab import Symtab
from semantic.typesys import check_binop, check_unaryop

class Checker:
    def __init__(self):
        self.errors = []
        self.current_function = None
        self.inside_loop = 0

    @classmethod
    def check(cls, program: list):
        checker = cls()
        env = Symtab("global")

        try:
            # Primera pasada: registrar funciones y variables globales
            for stmt in program:
                if isinstance(stmt, Function) or isinstance(stmt, Variable):
                    stmt.accept(checker, env)

            # Segunda pasada: validar todas las sentencias restantes (llamadas, prints, etc.)
            for stmt in program:
                if not isinstance(stmt, Function) and not isinstance(stmt, Variable):
                    stmt.accept(checker, env)

        except Exception as e:
            checker.errors.append(str(e))

        if checker.errors:
            print("[bold red]Errores semánticos encontrados:")
            for err in checker.errors:
                print(f"  [red]- {err}")
        else:
            print("[bold green]Análisis semántico completado exitosamente. Tabla de símbolos:")
            env.print()

        return checker

    def visit(self, node, env):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def generic_visit(self, node, env):
        raise Exception(f'No visit method defined for {node.__class__.__name__}')

    # Statements

    def visit_Assignment(self, n: Assignment, env: Symtab):
        var = env.get(n.location.name_or_expr)
        if var is None:
            raise NameError(f"Variable '{n.location.name_or_expr}' no declarada")

        if (hasattr(var, 'is_const') and var.is_const) or isinstance(var, Parameter):
            raise TypeError(f"No se puede asignar a constante o parámetro '{var.name}'")

        expr_type = n.expression.accept(self, env).lower()
        var_type = var.type.lower()
        if var_type != expr_type:
            raise TypeError(f"No se puede asignar tipo '{expr_type}' a '{var_type}'")


    def visit_Print(self, n: Print, env: Symtab):
        n.expression.accept(self, env)

    def visit_If(self, n: If, env: Symtab):
        cond_type = n.condition.accept(self, env).lower()
        if cond_type != 'bool':
            raise TypeError("La condición del if debe ser booleana")
        for stmt in n.then_branch:
            stmt.accept(self, env)
        for stmt in n.else_branch:
            stmt.accept(self, env)

    def visit_While(self, n: While, env: Symtab):
        cond_type = n.condition.accept(self, env).lower()
        if cond_type != 'bool':
            raise TypeError("La condición del while debe ser booleana")
        self.inside_loop += 1
        for stmt in n.body:
            stmt.accept(self, env)
        self.inside_loop -= 1

    def visit_Break(self, n: Break, env: Symtab):
        if self.inside_loop <= 0:
            raise SyntaxError("'break' fuera de un ciclo")

    def visit_Continue(self, n: Continue, env: Symtab):
        if self.inside_loop <= 0:
            raise SyntaxError("'continue' fuera de un ciclo")

    def visit_Return(self, n: Return, env: Symtab):
        if self.current_function is None:
            raise SyntaxError("'return' fuera de una función")
        expr_type = n.expression.accept(self, env).lower()
        func_return_type = self.current_function.return_type.lower()
        if expr_type != func_return_type:
            raise TypeError(f"La función debe retornar '{self.current_function.return_type}', pero retorna '{expr_type}'")

    # Declarations

    def visit_Variable(self, n: Variable, env: Symtab):
        if n.expression:
            expr_type = n.expression.accept(self, env).lower()
            if n.type and n.type.lower() != expr_type:
                raise TypeError(f"Tipo incompatible en inicialización de variable '{n.name}'")
            elif n.type is None:
                n.type = expr_type
        env.add(n.name, n)

    def visit_Function(self, n: Function, env: Symtab):
        env.add(n.name, n)
        func_env = Symtab(n.name, env)
        for param in n.params:
            func_env.add(param.name, param)
        old_function = self.current_function
        self.current_function = n
        for stmt in n.body:
            stmt.accept(self, func_env)
        self.current_function = old_function

    def visit_Parameter(self, n: Parameter, env: Symtab):
        env.add(n.name, n)

    # Expressions

    def visit_Integer(self, n: Integer, env: Symtab):
        return 'int'

    def visit_Float(self, n: Float, env: Symtab):
        return 'float'

    def visit_Char(self, n: Char, env: Symtab):
        return 'char'

    def visit_Bool(self, n: Bool, env: Symtab):
        return 'bool'

    def visit_BinOp(self, n: BinOp, env: Symtab):
        OP_MAP = {
            'PLUS': '+',
            'MINUS': '-',
            'TIMES': '*',
            'DIVIDE': '/',
            'LT': '<',
            'LE': '<=',
            'GT': '>',
            'GE': '>=',
            'EQ': '==',
            'NE': '!=',
            'LAND': '&&',
            'LOR': '||',
        }
        left = n.left.accept(self, env).lower()
        right = n.right.accept(self, env).lower()
        opr = OP_MAP.get(n.op, n.op)
        result = check_binop(opr, left, right)
        if not result:
            raise TypeError(f"Operación binaria inválida: {left} {opr} {right}")
        return result

    def visit_UnaryOp(self, n: UnaryOp, env: Symtab):
        expr = n.expr.accept(self, env).lower()
        result = check_unaryop(n.op, expr)
        if not result:
            raise TypeError(f"Operador unario inválido: {n.op} {expr}")
        return result

    def visit_TypeCast(self, n: TypeCast, env: Symtab):
        n.expr.accept(self, env)
        return n.type.lower()

    def visit_NamedLocation(self, n: NamedLocation, env: Symtab):
        symbol = env.get(n.name_or_expr)
        if symbol is None:
            raise NameError(f"Nombre no declarado: {n.name_or_expr}")
        return symbol.type.lower()

    def visit_FunctionCall(self, n: FunctionCall, env: Symtab):
        func = env.get(n.name)
        if func is None:
            raise NameError(f"Función no definida: {n.name}")
        if len(n.args) != len(func.params):
            raise TypeError(f"Argumentos incorrectos para '{n.name}': esperados {len(func.params)}, recibidos {len(n.args)}")
        for arg, param in zip(n.args, func.params):
            arg_type = arg.accept(self, env).lower()
            if arg_type != param.type.lower():
                raise TypeError(f"Argumento incompatible en llamada a '{n.name}': se esperaba '{param.type}', se recibió '{arg_type}'")
        return func.return_type.lower()
