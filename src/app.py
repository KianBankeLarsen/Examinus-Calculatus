from flask import Flask, render_template, jsonify, make_response
from src.Interpreter import *
import base64


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
    function_handler = FunctionHandler()
    interpreter = Interpreter(function_handler)

    result = interpreter.visit(tree)

    if result.type == 'image':
        response = make_response(base64.b64encode(result.image))
        response.headers.set('Content-Type', 'image/jpeg')
        return response
    elif result.type == 'float' or result.type == 'integer':
        response = make_response(str(result.value))
        response.headers.set('Content-Type', 'text/plain')
        return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
