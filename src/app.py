from flask import Flask, render_template
from src.Interpreter import *


app = Flask(__name__)


@app.route('/')
def Examinus_Calculatus():
    return render_template('index.html')


@app.route('/calc/<path:expression>')
def calc(expression):
    source = InputStream(expression)
    lexer = Lexer(source)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter()
    return str(interpreter.visit(tree))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
