from Lexer import *


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


class FuncCall(AST):
    def __init__(self, function, args):
        self.function = function
        self.args = args


class String(AST):
    def __init__(self, text):
        self.text = text


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

    def argument_list(self):
        self.consume(LPAREN)

        result = [self.expr()]

        while self.current_token.type == SEPERATOR:
            self.consume(SEPERATOR)

            result.append(self.expr())

        self.consume(RPAREN)

        return result

    def function_call(self):
        function_name = self.current_token.value.lower()

        self.consume(IDENTIFIER)

        args = self.argument_list()

        return FuncCall(function_name, args)

    def atom(self):
        current_token = self.current_token

        if current_token.type == INT:
            self.consume(INT)
            tree = Number(current_token)
            if self.current_token.type == FACTORIAL:
                self.consume(FACTORIAL)
                tree = UnaryOp(tree, Token(FACTORIAL, '!'))

            return tree

        elif current_token.type == REAL:
            self.consume(REAL)
            tree = Number(current_token)
            if self.current_token.type == FACTORIAL:
                self.consume(FACTORIAL)
                tree = UnaryOp(tree, Token(FACTORIAL, '!'))

            return tree

        elif current_token.type == LPAREN:
            tree = self.paren_expr()
            if self.current_token.type == FACTORIAL:
                self.consume(FACTORIAL)
                tree = UnaryOp(tree, Token(FACTORIAL, '!'))

            return tree
            
        elif current_token.type == IDENTIFIER:
            return self.function_call()

        else:
            self.error()

    def factor(self):
        operator = None

        if self.current_token.type == PLUS:
            self.consume(PLUS)
            operator = PLUS

        elif self.current_token.type == MINUS:
            self.consume(MINUS)
            operator = MINUS

        tree = self.atom()


        while self.current_token.type == POW:
            self.consume(POW)
            result = self.factor()
            tree = BinOp(tree, Token(POW, '^'), result)

        if operator == PLUS:
            return UnaryOp(tree, Token(PLUS, '+'))
        elif operator == MINUS:
            return UnaryOp(tree, Token(MINUS, '-'))
        else:
            return tree

    def term(self):
        tree = self.factor()

        while self.current_token.type in (LPAREN, MUL, DIV):
            if self.current_token.type == LPAREN:
                result = self.paren_expr()

                while self.current_token.type == POW:
                    self.consume(POW)
                    factor = self.factor()
                    result = BinOp(result, Token(POW, '^'), factor)

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
        print(self.current_token)
        if self.current_token.type == STRING:
            result = self.current_token.value

            self.consume(STRING)
            return String(result)


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
