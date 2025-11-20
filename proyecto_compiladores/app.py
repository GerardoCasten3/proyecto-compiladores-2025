# Importar clases y funciones del lexer, flask
from lexer import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS
from lexer.lexer import Lexer, LexerError
from parser import Parser, ParserError
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
        parser = Parser(tokens)
        ast = parser.parse()
        
        token_list = [
            {'value': t.value, 'type': t.type.name, 'line': t.line, 'column': t.column}
            for t in tokens
        ]

        ast_representation = format_ast(ast)
        ast_representation = "Todo salió bien. Árbol AST generado correctamente." + "\n" + ast_representation

        return jsonify({'success': True, 'tokens': token_list, 'ast': ast_representation})

    except (LexerError, ParserError) as e:
    # Recuperar tokens válidos acumulados dentro del lexer
        token_list = [
            {'value': t.value, 'type': t.type.name, 'line': t.line, 'column': t.column}
            for t in getattr(lexer, 'tokens', [])
        ]
        ast_representation = "No se pudo generar el AST debido a errores, revisa el código." + "\n" + str(e) 
        return jsonify({
            'success': False,
            'error': str(e),
            'partial_tokens': token_list,
            'ast': ast_representation

        }), 400
    
# Imprimir el AST de forma jerárquica
def format_ast(node, indent=0):
    """Imprime el AST de forma jerárquica"""
    spacing = "  " * indent
    return f"{spacing}{node.__class__.__name__}: {node}"


if __name__ == "__main__":
    app.run(debug=True)