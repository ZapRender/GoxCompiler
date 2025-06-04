import unittest
from parse.model import Variable, Assignment, NamedLocation, Integer, Float, Bool, Function, Parameter, Print, FunctionCall, Return, Break, Continue, If, While, BinOp, UnaryOp, TypeCast
from semantic.check import Checker
from semantic.symtab import Symtab

class TestSemanticChecker(unittest.TestCase):

    def check_program(self, stmts):
        """ Helper para correr el checker sobre lista de nodos """
        return Checker.check(stmts)

    def test_variable_declaration_and_assignment(self):
        var = Variable("x", "int", Integer(10), False)
        assign = Assignment(NamedLocation("x"), Integer(20))
        stmts = [var, assign]
        checker = self.check_program(stmts)
        self.assertEqual(len(checker.errors), 0)

    def test_assignment_to_undeclared_variable(self):
        assign = Assignment(NamedLocation("y"), Integer(5))
        stmts = [assign]
        checker = self.check_program(stmts)
        self.assertIn("Variable 'y' no declarada", checker.errors[0])

    def test_const_assignment_error(self):
        const_var = Variable("c", "int", Integer(1), True)
        assign = Assignment(NamedLocation("c"), Integer(2))
        stmts = [const_var, assign]
        checker = self.check_program(stmts)
        self.assertIn("No se puede asignar a constante o parámetro 'c'", checker.errors[0])

    def test_type_mismatch_assignment(self):
        var = Variable("x", "int", Integer(1), False)
        assign = Assignment(NamedLocation("x"), Bool(True))
        stmts = [var, assign]
        checker = self.check_program(stmts)
        self.assertIn("No se puede asignar tipo 'bool' a 'int'", checker.errors[0])

    def test_function_definition_and_call_correct(self):
        param1 = Parameter("a", "int")
        param2 = Parameter("b", "int")
        body = [Return(BinOp(NamedLocation("a"), "PLUS", NamedLocation("b")))]
        func = Function("sum", [param1, param2], "int", body)
        call = Print(FunctionCall("sum", [Integer(1), Integer(2)]))
        stmts = [func, call]
        checker = self.check_program(stmts)
        self.assertEqual(len(checker.errors), 0)

    def test_function_call_with_wrong_arg_count(self):
        param1 = Parameter("a", "int")
        func = Function("foo", [param1], "int", [])
        call = Print(FunctionCall("foo", [Integer(1), Integer(2)]))
        stmts = [func, call]
        checker = self.check_program(stmts)
        self.assertIn("Argumentos incorrectos para 'foo'", checker.errors[0])

    def test_function_call_with_wrong_arg_type(self):
        param1 = Parameter("a", "int")
        func = Function("foo", [param1], "int", [])
        call = Print(FunctionCall("foo", [Bool(True)]))
        stmts = [func, call]
        checker = self.check_program(stmts)
        self.assertIn("Argumento incompatible en llamada a 'foo'", checker.errors[0])

    def test_return_type_mismatch(self):
        body = [Return(Bool(True))]
        func = Function("bar", [], "int", body)
        stmts = [func]
        checker = self.check_program(stmts)
        self.assertIn("La función debe retornar 'int', pero retorna 'bool'", checker.errors[0])

    def test_break_continue_outside_loop(self):
        break_stmt = Break()
        continue_stmt = Continue()
        stmts = [break_stmt, continue_stmt]
        checker = self.check_program(stmts)
        errors_text = " ".join(checker.errors)
        self.assertIn("'break' fuera de un ciclo", errors_text)


    def test_break_continue_inside_loop(self):
        while_stmt = While(Bool(True), [Break(), Continue()])
        stmts = [while_stmt]
        checker = self.check_program(stmts)
        self.assertEqual(len(checker.errors), 0)

    def test_if_condition_type(self):
        if_stmt = If(Integer(1), [], [])
        stmts = [if_stmt]
        checker = self.check_program(stmts)
        self.assertIn("La condición del if debe ser booleana", checker.errors[0])

    def test_while_condition_type(self):
        while_stmt = While(Integer(0), [])
        stmts = [while_stmt]
        checker = self.check_program(stmts)
        self.assertIn("La condición del while debe ser booleana", checker.errors[0])

    def test_unary_operator_invalid(self):
        unary = UnaryOp('!', Integer(1))
        stmts = [Print(unary)]
        checker = self.check_program(stmts)
        self.assertIn("Operador unario inválido", checker.errors[0])

    def test_binop_invalid(self):
        binop = BinOp(Integer(1), 'LAND', Integer(0))
        stmts = [Print(binop)]
        checker = self.check_program(stmts)
        self.assertIn("Operación binaria inválida", checker.errors[0])

    def test_type_cast(self):
        cast = TypeCast("int", Float(3.14))
        stmts = [Print(cast)]
        checker = self.check_program(stmts)
        self.assertEqual(len(checker.errors), 0)

if __name__ == "__main__":
    unittest.main()
