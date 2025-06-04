
# model.py

# -------------------------------
# Statements
# -------------------------------

class Assignment:
    def __init__(self, location, expression):
        self.location = location
        self.expression = expression

    def __repr__(self):
        return f"Assignment({self.location}, {self.expression})"


class Print:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Print({self.expression})"


class If:
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"If({self.condition}, {self.then_branch}, {self.else_branch})"


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition}, {self.body})"


class Break:
    def __repr__(self):
        return "Break()"


class Continue:
    def __repr__(self):
        return "Continue()"


class Return:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Return({self.expression})"


# -------------------------------
# Declarations
# -------------------------------

class Variable:
    def __init__(self, name, type_, expression, is_const):
        self.name = name
        self.type = type_
        self.expression = expression
        self.is_const = is_const

    def __repr__(self):
        return f"Variable({self.name}, {self.type}, {self.expression}, const={self.is_const})"


class Parameter:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_

    def __repr__(self):
        return f"Parameter({self.name}: {self.type})"


class Function:
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body

    def __repr__(self):
        return f"Function({self.name}, params={self.params}, returns={self.return_type}, body={self.body})"


# -------------------------------
# Expressions
# -------------------------------

class Integer:
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"Integer({self.value})"


class Float:
    def __init__(self, value):
        self.value = float(value)

    def __repr__(self):
        return f"Float({self.value})"


class Char:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Char({self.value})"


class Bool:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Bool({self.value})"


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"


class UnaryOp:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f"UnaryOp({self.op} {self.expr})"


class TypeCast:
    def __init__(self, type_, expr):
        self.type = type_
        self.expr = expr

    def __repr__(self):
        return f"TypeCast({self.type}, {self.expr})"


# -------------------------------
# Locations
# -------------------------------

class NamedLocation:
    def __init__(self, name_or_expr):
        self.name_or_expr = name_or_expr

    def __repr__(self):
        return f"NamedLocation({self.name_or_expr})"
