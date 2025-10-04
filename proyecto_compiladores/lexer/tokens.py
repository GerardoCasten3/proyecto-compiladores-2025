from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Literales
    NUM = auto()           # Enteros, decimales y notación científica
    STRING_LIT = auto()    # "texto"
    TRUE = auto()          # true
    FALSE = auto()         # false
    
    # Identificadores
    ID = auto()            # Variables y nombres definidos por usuario
    
    # Palabras reservadas
    MODULE = auto()        # module
    IMPORT = auto()        # import
    AS = auto()            # as
    TYPE = auto()          # type
    STRUCT = auto()        # struct
    CONST = auto()         # const
    LET = auto()           # let
    FN = auto()            # fn
    INT = auto()           # int
    BOOL = auto()          # bool
    STRING = auto()        # string
    IF = auto()            # if
    ELSE = auto()          # else
    WHILE = auto()         # while
    RETURN = auto()        # return
    
    # Operadores aritméticos
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    MODULO = auto()        # %
    
    # Operadores relacionales
    ASSIGN = auto()        # =
    EQUAL = auto()         # ==
    NOT_EQUAL = auto()     # !=
    LESS_THAN = auto()     # <
    LESS_EQUAL = auto()    # <=
    GREATER_THAN = auto()  # >
    GREATER_EQUAL = auto() # >=
    
    # Operadores lógicos
    NOT = auto()           # !
    AND = auto()           # &&
    OR = auto()            # ||
    
    # Otros operadores
    DOT = auto()           # .
    
    # Delimitadores
    COMMA = auto()         # ,
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    LBRACKET = auto()      # [
    RBRACKET = auto()      # ]
    COLON = auto()         # :
    SEMICOLON = auto()     # ;
    
    # Especiales
    COMMENT = auto()       # //texto//
    EOF = auto()           # Fin de archivo
    ERROR = auto()         # Token de error


@dataclass
class Token:
    # Atributos del token
    type: TokenType
    value: str
    line: int
    column: int
    
    # Representa el token como una cadena legible
    def __str__(self):
        return f"{self.type.name:15} | {self.value:25} | Línea {self.line:3}, Col {self.column:3}"


# Diccionario de palabras reservadas
KEYWORDS = {
    'module': TokenType.MODULE,
    'import': TokenType.IMPORT,
    'as': TokenType.AS,
    'type': TokenType.TYPE,
    'struct': TokenType.STRUCT,
    'const': TokenType.CONST,
    'let': TokenType.LET,
    'fn': TokenType.FN,
    'int': TokenType.INT,
    'bool': TokenType.BOOL,
    'string': TokenType.STRING,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'return': TokenType.RETURN,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
}


# Operadores de un solo carácter
SINGLE_CHAR_TOKENS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '%': TokenType.MODULO,
    '.': TokenType.DOT,
    ',': TokenType.COMMA,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '{': TokenType.LBRACE,
    '}': TokenType.RBRACE,
    '[': TokenType.LBRACKET,
    ']': TokenType.RBRACKET,
    ':': TokenType.COLON,
    ';': TokenType.SEMICOLON,
}