from src.Lexer import *


class AST:
    pass


class Number(AST):
    def __init__(self, token):
        self.value = token.value


class BinOp(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator.value
        self.right = right


class UnaryOp(AST):
    def __init__(self, token, operator):
        self.token = token
        self.operator = operator


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Unexpected token.")

    def consume(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def atom(self):
        current_token = self.current_token

        if current_token.type == INT:
            self.consume(INT)
            return Number(current_token)

        elif self.current_token.type == LPAREN:
            self.consume(LPAREN)

            result = self.expr()

            self.error()

            self.consume(RPAREN)
            return result
            
        else:
            self.error()


    def factor(self):
        pass

    def term(self):
        pass

    def expr(self):
        tree = self.term()

    def parse(self):
        tree = self.expr()

        return tree
