# Importar clases y funciones del lexer, flask
from lexer import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS
from lexer.lexer import Lexer, LexerError
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)