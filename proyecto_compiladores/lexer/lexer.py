from .tokens import Token, TokenType, KEYWORDS, SINGLE_CHAR_TOKENS

class LexerError(Exception):
    # Excepción para errores léxicos
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Se registró un error léxico en línea {line}, columna {column}: {message}")

class Lexer:
    # Analizador léxico de código fuente a tokens
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if self.source else None

    def advance(self):
        # Avanza al siguiente caracter en el codigo fuente
        # Si el caracter actual es un salto de linea, incrementa la linea y resetea la columna
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        # Si no, simplemente avanza la posicion y la columna
        else:
            self.column += 1
        self.pos += 1
        # Actualiza el caracter actual, o lo pone en None si se llega al final del codigo fuente
        self.current_char = self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self, offset=1):
        # Mira el siguiente caracter sin avanzar la posicion
        peek_pos = self.pos + offset
        return self.source[peek_pos] if peek_pos < len(self.source) else None
