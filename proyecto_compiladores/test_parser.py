from lexer import Lexer
from parser import Parser


def print_ast(node, indent=0):
    """Imprime el AST de forma jerárquica"""
    spacing = "  " * indent
    print(f"{spacing}{node.__class__.__name__}: {node}")


def test_parser(source_code):
    """Prueba el parser con código fuente"""
    print("=" * 80)
    print("CÓDIGO FUENTE:")
    print("=" * 80)
    print(source_code)
    print()
    
    # Análisis léxico
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    print("=" * 80)
    print("TOKENS:")
    print("=" * 80)
    Lexer.print_tokens(tokens)
    
    # Análisis sintáctico
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("=" * 80)
    print("AST (Árbol de Sintaxis Abstracta):")
    print("=" * 80)
    print_ast(ast)
    print()
    
    return ast


# ============================================================================
# EJEMPLOS DE PRUEBA
# ============================================================================

# Ejemplo 1: Programa simple con función
example1 = """
module Main;

fn suma(a: int, b: int) -> int {
    return a + b;
}
"""

# Ejemplo 2: Programa con struct y constante
example2 = """
module Geometria;

struct Punto {
    x: int,
    y: int
};

const PI: int = 3;

fn distancia(p1: Punto, p2: Punto) -> int {
    let dx: int = p2.x - p1.x;
    let dy: int = p2.y - p1.y;
    return dx * dx + dy * dy;
}
"""

# Ejemplo 3: Programa con control de flujo
example3 = """
module Control;

fn factorial(n: int) -> int {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

fn cuenta(limite: int) {
    let i: int = 0;
    while (i < limite) {
        i = i + 1;
    }
}
"""

# Ejemplo 4: Programa con imports y tipos
example4 = """
module Utils;

import Math.Avanzado as MA;
import Sistema;

type Entero = int;
type Vector = []int;

let global: int = 42;
"""


if __name__ == "__main__":
    print("PRUEBA 1: Función simple")
    try:
        test_parser(example1)
    except Exception as e:
        print(f"Error: {e}")
    
    print("PRUEBA 2: Struct y constante")
    try:
        test_parser(example2)
    except Exception as e:
        print(f"Error: {e}")
    
    print("PRUEBA 3: Control de flujo")
    try:
        test_parser(example3)
    except Exception as e:
        print(f"Error: {e}")
    print("PRUEBA 4: Imports y tipos")
    try:
        test_parser(example4)
    except Exception as e:
        print(f"Error: {e}")