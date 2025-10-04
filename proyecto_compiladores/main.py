# Importar clases y funciones del lexer
from lexer import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS

# Prueba rápida
token = Token(TokenType.ID, "variable", 1, 1)
print(token)
print(f"Keywords disponibles: {len(KEYWORDS)}")
