# Importar clases y funciones del lexer, flask
from lexer import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS
from lexer.lexer import Lexer, LexerError
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def tokenize ():
    data=request.json
    source_code = data.get('source_code', '')
    
    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        token_list = [{'value': token.value, 'type': token.type.name, 'line': token.line, 'column': token.column} for token in tokens]
        return jsonify({'success':True,'tokens': token_list})
    except LexerError as e:
        return jsonify({'success':False,'error': str(e)}), 400
    
if __name__ == "__main__":
    app.run(debug=True)