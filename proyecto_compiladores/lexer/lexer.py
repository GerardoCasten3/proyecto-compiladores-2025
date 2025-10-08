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

    def skip_whitespace(self):
        """Ignora espacios en blanco, tabs y saltos de línea"""
        while self.current_char and self.current_char in ' \t\n\r':
            self.advance()
    
    def read_comment(self):
        """Lee un comentario //texto//"""
        start_line = self.line
        start_col = self.column
        
        # Consumir el primer //
        self.advance()  # primer /
        self.advance()  # segundo /
        
        comment_text = ""
        
        # Leer hasta encontrar el cierre //
        while self.current_char:
            if self.current_char == '/' and self.peek() == '/':
                # Encontramos el cierre
                self.advance()  # primer /
                self.advance()  # segundo /
                return Token(TokenType.COMMENT, f"//{comment_text}//", start_line, start_col)
            else:
                comment_text += self.current_char
                self.advance()
        
        # Si llegamos aquí, no se cerró el comentario
        raise LexerError("Comentario no cerrado (se esperaba ' // ')", start_line, start_col)
    
    def read_string(self):
        """Lee un string literal "texto" """
        start_line = self.line
        start_col = self.column
        
        self.advance()  # Consumir la comilla inicial "
        string_value = ""
        
        while self.current_char and self.current_char != '"':
            string_value += self.current_char
            self.advance()
        
        if self.current_char == '"':
            self.advance()  # Consumir la comilla final "
            return Token(TokenType.STRING_LIT, f'"{string_value}"', start_line, start_col)
        else:
            raise LexerError("String literal no cerrado (se esperaba ' \" ')", start_line, start_col)
    
    def read_number(self):
        """Lee un número: entero, decimal o notación científica"""
        start_line = self.line
        start_col = self.column
        num_str = ""
        
        # Parte entera
        while self.current_char and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        
        # Parte decimal (opcional)
        if self.current_char == '.':
            num_str += self.current_char
            self.advance()
            
            while self.current_char and self.current_char.isdigit():
                num_str += self.current_char
                self.advance()
        
        # Notación científica (opcional)
        if self.current_char and self.current_char in 'eE':
            num_str += self.current_char
            self.advance()
            
            # Signo opcional
            if self.current_char and self.current_char in '+-':
                num_str += self.current_char
                self.advance()
            
            # Exponente (debe tener al menos un dígito)
            if not (self.current_char and self.current_char.isdigit()):
                raise LexerError(f"Número en notación científica inválido: ' {num_str} '", start_line, start_col)
            
            while self.current_char and self.current_char.isdigit():
                num_str += self.current_char
                self.advance()
        
        return Token(TokenType.NUM, num_str, start_line, start_col)
    
    def read_identifier(self):
        """Lee un identificador o palabra reservada"""
        start_line = self.line
        start_col = self.column
        id_str = ""
        
        # Debe comenzar con letra (ya validado antes de llamar)
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        
        # Verificar si es palabra reservada
        token_type = KEYWORDS.get(id_str, TokenType.ID)
        return Token(token_type, id_str, start_line, start_col)
    
    def get_next_token(self):
        """Obtiene el siguiente token del código fuente"""
        while self.current_char:
            # Ignorar espacios en blanco
            if self.current_char in ' \t\n\r':
                self.skip_whitespace()
                continue
            
            start_line = self.line
            start_col = self.column
            
            # Comentarios //texto//
            if self.current_char == '/' and self.peek() == '/':
                return self.read_comment()
            
            # String literals "texto"
            if self.current_char == '"':
                return self.read_string()
            
            # Números
            if self.current_char.isdigit():
                return self.read_number()
            
            # Identificadores y palabras reservadas
            if self.current_char.isalpha():
                return self.read_identifier()
            
            # Operadores compuestos y de asignación
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQUAL, "==", start_line, start_col)
                return Token(TokenType.ASSIGN, "=", start_line, start_col)
            
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NOT_EQUAL, "!=", start_line, start_col)
                return Token(TokenType.NOT, "!", start_line, start_col)
            
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LESS_EQUAL, "<=", start_line, start_col)
                return Token(TokenType.LESS_THAN, "<", start_line, start_col)
            
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GREATER_EQUAL, ">=", start_line, start_col)
                return Token(TokenType.GREATER_THAN, ">", start_line, start_col)
            
            if self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    return Token(TokenType.AND, "&&", start_line, start_col)
                raise LexerError(f"Carácter inesperado: '&' (se esperaba ' && ')", start_line, start_col)
            
            if self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    return Token(TokenType.OR, "||", start_line, start_col)
                raise LexerError(f"Carácter inesperado: '|' (se esperaba ' || ')", start_line, start_col)
            
            if self.current_char == '-' and self.peek() == '>':
                self.advance()  # consumir '-'
                self.advance()  # consumir '>'
                return Token(TokenType.ARROW, "->", start_line, start_col)
            
            # Operadores y delimitadores de un solo carácter
            if self.current_char in SINGLE_CHAR_TOKENS:
                char = self.current_char
                self.advance()
                return Token(SINGLE_CHAR_TOKENS[char], char, start_line, start_col)
            
            # Carácter no reconocido
            raise LexerError(f"Carácter no reconocido: ' {self.current_char} '", start_line, start_col)
        
        # Fin del archivo
        return Token(TokenType.EOF, "", self.line, self.column)
    
    def tokenize(self):
        """Tokeniza todo el código fuente y retorna la lista de tokens"""
        self.tokens = []
        
        try:
            while self.current_char:
                token = self.get_next_token()
                
                # No almacenar comentarios en la lista de tokens
                if token.type != TokenType.COMMENT:
                    self.tokens.append(token)
                
                if token.type == TokenType.EOF:
                    break
            
            # Asegurar que siempre haya un token EOF
            if not self.tokens or self.tokens[-1].type != TokenType.EOF:
                self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
            
            return self.tokens
        
        except LexerError as e:
            print(f"\n ERROR DE ANÁLISIS LÉXICO")
            print(f"   {e}")
            print(f"\n   Tokens reconocidos antes del error:")
            if self.tokens:
                self.print_tokens(self.tokens)
            else:
                print("   (ninguno)")
            raise
    
    @staticmethod
    def print_tokens(tokens):
        """Imprime la tabla de tokens de forma formateada"""
        print("\n" + "="*70)
        print(f"{'TIPO DE TOKEN':<20} | {'LEXEMA':<25} | {'POSICIÓN':<20}")
        print("="*70)
        
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"{token.type.name:<20} | {token.value:<25} | Línea {token.line:3}, Col {token.column:3}")
        
        print("="*70)
        print(f"Total de tokens: {len([t for t in tokens if t.type != TokenType.EOF])}\n")