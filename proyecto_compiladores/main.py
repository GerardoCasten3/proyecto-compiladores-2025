# Importar clases y funciones del lexer
from lexer import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS
from lexer.lexer import Lexer, LexerError


def test_lexer(source_code, test_name="Test"):
    """Función auxiliar para probar el lexer"""
    print(f"\n{'='* 70}")
    print(f" {test_name}")
    print(f"{'='* 70}")
    print("Código fuente:")
    print("-" * 70)
    print(source_code)
    print("-" * 70)

    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        print("\nANÁLISIS LÉXICO EXITOSO")
        Lexer.print_tokens(tokens)
        return tokens
    except LexerError as e:
        # El error ya fue impreso por el lexer
        return None


def main():
    """Programa principal con casos de prueba"""

    # Test 1: Declaraciones simples
    # test_lexer(
    #     """
    #     let x = 10;
    #     const PI = 3.14159;
    #     """,
    #     "Test 1: Declaraciones simples"
    # )
    test_lexer(
        """ let mensaje = "Hola mundo"
        let x = 10; """,
        "Test 9: Error - String no cerrado"
    )
    
if __name__ == "__main__":
    print("ANALIZADOR LÉXICO - SUITE DE PRUEBAS")
    print("="*70)
    main()
    print("\n" + "="*70)
    print("Pruebas completadas")
    print("="*70)