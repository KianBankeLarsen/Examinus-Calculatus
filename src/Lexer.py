from src.Streams import *

PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
INT = 'INT'
EOF = 'EOF'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return '<{}, {}>'.format(self.type, self.value)


class Lexer:
    def __init__(self, stream):
        self.text = stream

    # LEXER HELPER FUNCTIONS #
    def error(self):
        lines = self.text.text.split("\n")

        error_line = lines[self.text.row - 1]

        error_string =\
        """Unexpected character '{}' at [{}:{}]:
        {}
        {}^
        """.format(self.text.current_char, self.text.row, self.text.col, error_line, " " * (self.text.col - 1), " " * (self.text.col - 1), 2)


        raise ValueError(error_string)

    def consume_whitespace(self):
        while self.text.current_char is not None and self.text.current_char.isspace():
            self.text.advance()

    def integer(self):
        result = ''

        while self.text.current_char is not None and self.text.current_char.isdigit():
            result += self.text.current_char
            self.text.advance()

        return int(result)


    # MAIN LEXER FUNCTION #
    def get_next_token(self):
        while self.text.current_char is not None:

            if self.text.current_char.isspace():
                self.consume_whitespace()
                continue

            if self.text.current_char.isdigit():
                result = self.integer()
                return Token(INT, result)

            if self.text.current_char == '+':
                self.text.advance()
                return Token(PLUS, '+')

            if self.text.current_char == '-':
                self.text.advance()
                return Token(MINUS, '-')

            if self.text.current_char == '*':
                self.text.advance()
                return Token(MUL, '*')

            if self.text.current_char == '/':
                self.text.advance()
                return Token(DIV, '/')

            if self.text.current_char == '(':
                self.text.advance()
                return Token(LPAREN, '(')

            if self.text.current_char == ')':
                self.text.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, 'EOF')


source = InputStream("2+   345  -  2323 + 4 - 4\n4+4+4+4+4+sqrt")
lex = Lexer(source)
token = lex.get_next_token()


while token.type != EOF:
    print(token)
    token = lex.get_next_token()