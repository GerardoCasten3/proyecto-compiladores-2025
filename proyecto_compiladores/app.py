# Importar clases y funciones del lexer, flask
from lexer import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS
from lexer.lexer import Lexer, LexerError
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def tokenize():
    data = request.json
    source_code = data.get('source_code', '')

    lexer = Lexer(source_code)
    try:
        tokens = lexer.tokenize()
        token_list = [
            {'value': t.value, 'type': t.type.name, 'line': t.line, 'column': t.column}
            for t in tokens
        ]
        return jsonify({'success': True, 'tokens': token_list})

    except LexerError as e:
        # Recuperar tokens válidos acumulados dentro del lexer
        token_list = [
            {'value': t.value, 'type': t.type.name, 'line': t.line, 'column': t.column}
            for t in getattr(lexer, 'tokens', [])
        ]
        return jsonify({
            'success': False,
            'error': str(e),
            'partial_tokens': token_list
        }), 400
    
if __name__ == "__main__":
    app.run(debug=True)