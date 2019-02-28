from src.Lexer import *


class AST:
    pass


class Number(AST):
    def __init__(self, token):
        self.value = token.value


class BinOp(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOp(AST):
    def __init__(self, operand, operator):
        self.operand = operand
        self.operator = operator


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        print(self.current_token)
        raise Exception("Unexpected token.")

    def consume(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def paren_expr(self):
        if self.current_token.type == LPAREN:
            self.consume(LPAREN)

            result = self.expr()

            self.consume(RPAREN)
            return result

        else:
            self.error()

    def atom(self):
        current_token = self.current_token

        if current_token.type == INT:
            self.consume(INT)
            return Number(current_token)

        elif current_token.type == REAL:
            self.consume(REAL)
            return Number(current_token)

        elif current_token.type == LPAREN:
            return self.paren_expr()
            
        else:
            self.error()

    def factor(self):
        return self.atom()

    def term(self):
        if self.current_token.type == PLUS:
            self.consume(PLUS)

            result = self.factor()

            return UnaryOp(result, Token(PLUS, '+'))
        elif self.current_token.type == MINUS:
            self.consume(MINUS)

            result = self.factor()

            return UnaryOp(result, Token(MINUS, '-'))

        tree = self.factor()

        if self.current_token.type in (LPAREN, MUL, DIV):
            while self.current_token.type in (LPAREN, MUL, DIV):
                if self.current_token.type == LPAREN:
                    result = self.paren_expr()
                    tree = BinOp(tree, Token(MUL, '*'), result)

                elif self.current_token.type == MUL:
                    self.consume(MUL)
                    other = self.factor()

                    tree = BinOp(tree, Token(MUL, '*'), other)
                elif self.current_token.type == DIV:
                    self.consume(DIV)
                    other = self.factor()

                    tree = BinOp(tree, Token(DIV, '/'), other)

        return tree

    def expr(self):
        tree = self.term()

        while self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == PLUS:
                self.consume(PLUS)
                other = self.term()

                tree = BinOp(tree, Token(PLUS, '+'), other)
            elif self.current_token.type == MINUS:
                self.consume(MINUS)
                other = self.term()

                tree = BinOp(tree, Token(MINUS, '-'), other)

        return tree

    def parse(self):
        tree = self.expr()

        if self.current_token.type != EOF:
            self.error()

        return tree
