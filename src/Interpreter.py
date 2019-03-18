from src.Parser import *
from graphviz import Graph
import math


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("Couldn't find a visit_{} method.".format(type(node).__name__))


class DOTGenerator(NodeVisitor):
    def __init__(self):
        self.nodes = 0
        self.graph = Graph()

    def add_node(self, label):
        self.graph.node(str(self.nodes), label, color="#c5c8c6ff", fontcolor="#c5c8c6ff")

        self.nodes += 1

        return str(self.nodes - 1)

    def add_edge(self, start, end):
        self.graph.edge(start, end, color="#c5c8c6ff")

    def visit_BinOp(self, node):
        id1 = self.add_node("BinOp")
        id2 = self.visit(node.left)
        id3 = self.add_node(node.operator.type)
        id4 = self.visit(node.right)

        self.add_edge(id1, id2)
        self.add_edge(id1, id3)
        self.add_edge(id1, id4)

        return id1

    def visit_UnaryOp(self, node):
        id1 = self.add_node("UnaryOp")
        id2 = self.add_node(node.operator.type)
        id3 = self.visit(node.operand)

        self.add_edge(id1, id2)
        self.add_edge(id1, id3)

        return id1

    def visit_Number(self, node):
        id1 = self.add_node(str(node.value))

        return id1

    def visit_FuncCall(self, node):
        id1 = self.add_node("FuncCall")
        id2 = self.add_node(node.function)
        id3 = self.add_node("Args")

        for arg in node.args:
            id_n = self.visit(arg)

            self.add_edge(id3, id_n)

        self.add_edge(id1, id2)
        self.add_edge(id1, id3)

        return id1


# Creates a stream of characters for the lexer
#source = InputStream("2!")
# Creates a lexer and passes the character stream to the lexer which functions as a stream of tokens
#lex = Lexer(source)
# Creates a parser and passes the token stream from the lexer to the parser
#parser = Parser(lex)
# Parses the stream from the lexer and creates an AST
#result = parser.parse()
# Creates a DOTGenerator, which visits every node and creates a graph of the AST.
#graph_generator = DOTGenerator()
#graph_generator.visit(result)
#graph_generator.graph.format = 'png'
#graph_generator.graph.render()


class Interpreter(NodeVisitor):
    def __init__(self, function_handler=None):
        self.function_handler = function_handler
        self.function_handler.interpreter = self

    def visit_BinOp(self, node):
        operator = node.operator.type

        left = self.visit(node.left)
        right = self.visit(node.right)

        if operator == PLUS:
            return left + right
        elif operator == MINUS:
            return left - right
        elif operator == MUL:
            return left * right
        elif operator == DIV:
            return left / right
        elif operator == POW:
            return left ** right

    def visit_UnaryOp(self, node):
        operator = node.operator.type
        factor = self.visit(node.operand)

        if operator == PLUS:
            return factor
        elif operator == MINUS:
            return - factor
        elif operator == FACTORIAL:
            return self.function_handler.call('factorial', [node.operand])

    def visit_Number(self, node):
        if isinstance(node.value, int) or node.value.is_integer():
            return IntegerResult(int(node.value))
        else:
            return FloatResult(node.value)

    def visit_FuncCall(self, node):
        result = self.function_handler.call(node.function, node.args)

        if result.type == "integer" or result.type == "float":
            return result
        elif result.type == "image":
            return result
        return

# Handles return-values from built-in functions
class Result:
    def __init__(self, type):
        self.type = type

    def handle_operation(self, other, func):
        if isinstance(other, IntegerResult) or isinstance(other, FloatResult):
            result = func(self.value, other.value)

            if isinstance(result, int):
                return IntegerResult(result)
            elif result.is_integer():
                return IntegerResult(int(result))
            else:
                return FloatResult(result)

        elif isinstance(other, int) or isinstance(other, float):
            result = func(self.value, other)

            if isinstance(result, int):
                return IntegerResult(result)
            elif result.is_integer():
                return IntegerResult(int(result))
            else:
                return FloatResult(result)


class IntegerResult(Result):
    def __init__(self, value):
        super().__init__("integer")
        self.value = value

    def __add__(self, other):
        return self.handle_operation(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self.handle_operation(other, lambda a, b: a - b)

    def __mul__(self, other):
        return self.handle_operation(other, lambda a, b: a * b)

    def __truediv__(self, other):
        return self.handle_operation(other, lambda a, b: a / b)

    def __neg__(self):
        return IntegerResult(-self.value)

    def __pow__(self, power, modulo=None):
        return self.handle_operation(power, lambda a, b: a ** b)

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)


class FloatResult(Result):
    def __init__(self, value, precision=15):
        super().__init__("float")
        self.value = value

    def __add__(self, other):
        return self.handle_operation(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self.handle_operation(other, lambda a, b: a - b)

    def __mul__(self, other):
        return self.handle_operation(other, lambda a, b: a * b)

    def __truediv__(self, other):
        return self.handle_operation(other, lambda a, b: a / b)

    def __neg__(self):
        return FloatResult(-self.value)

    def __pow__(self, power, modulo=None):
        return self.handle_operation(power, lambda a, b: a ** b)

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return self.value


class RationalResult(Result):
    def __init__(self):
        super().__init__("rational")


class ImageResult(Result):
    def __init__(self, image):
        super().__init__("image")
        self.image = image


class FunctionHandler:
    def __init__(self):
        self.interpreter = None
        self.graph_generator = DOTGenerator()

    def call(self, func_name, args):
        to_call = getattr(self, func_name, self.generic_call)
        return to_call(args)

    def generic_call(self, function):
        raise Exception("Error: function called '{}' not defined.".format("UNKOWN"))

    def check_args(self, amount, min_args, max_args=None):
        if not max_args and amount >= min_args:
            return None

        if not (max_args >= amount >= min_args):
            raise Exception("Unexpected amount of arguments.")

    def make_number(self, value):
        if isinstance(value, int):
            return IntegerResult(value)
        elif isinstance(value, float):
            if value.is_integer():
                return IntegerResult(int(value))
            else:
                return FloatResult(value)

    def sqrt(self, args):
        self.check_args(len(args), 1, 1)

        value = self.interpreter.visit(args[0])

        result = value ** (1/2)

        return result

    def sin(self, args):
        self.check_args(len(args), 1, 1)

        value = self.interpreter.visit(args[0])

        result = math.sin(math.radians(value))

        return self.make_number(round(result, 15))

    def cos(self, args):
        self.check_args(len(args), 1, 1)

        value = self.interpreter.visit(args[0])

        result = math.cos(math.radians(value))

        return self.make_number(round(result, 15))

    def tan(self, args):
        self.check_args(len(args), 1, 1)

        value = self.interpreter.visit(args[0])

        result = math.tan(math.radians(value))

        return self.make_number(round(result, 15))

    def factorial(self, args):
        self.check_args(len(args), 1, 1)

        value = self.interpreter.visit(args[0])

        result = math.factorial(value)

        return self.make_number(result)

    def parse(self, args):
        self.check_args(len(args), 1, 1)

        expression = args[0]

        self.graph_generator.visit(expression)
        self.graph_generator.graph.format = 'png'
        self.graph_generator.graph.attr(bgcolor='#ffffff00', fontcolor="blue")

        result = self.graph_generator.graph.pipe()

        return ImageResult(result)




#print(interpreter.visit(result).value)