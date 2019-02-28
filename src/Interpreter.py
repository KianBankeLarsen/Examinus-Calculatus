from src.Parser import *
from graphviz import Graph


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
        self.graph.node(str(self.nodes), label)

        self.nodes += 1

        return str(self.nodes - 1)

    def add_edge(self, start, end):
        self.graph.edge(start, end)

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


# Creates a stream of characters for the lexer
source = InputStream("3(2)(3)")
# Creates a lexer and passes the character stream to the lexer which functions as a stream of tokens
lex = Lexer(source)
# Creates a parser and passes the token stream from the lexer to the parser
parser = Parser(lex)
# Parses the stream from the lexer and creates an AST
result = parser.parse()
# Creates a DOTGenerator, which visits every node and creates a graph of the AST.
graph_generator = DOTGenerator()
graph_generator.visit(result)
graph_generator.graph.format = 'png'
graph_generator.graph.render()


class Interpreter(NodeVisitor):
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

    def visit_UnaryOp(self, node):
        operator = node.operator.type
        factor = self.visit(node.operand)

        if operator == PLUS:
            return factor
        elif operator == MINUS:
            return - factor

    def visit_Number(self, node):
        return node.value


interpreter = Interpreter()
print(interpreter.visit(result))