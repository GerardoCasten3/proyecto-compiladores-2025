from lexer import Token, TokenType
from .ast_nodes import *
from typing import List, Optional


class ParserError(Exception):
    """Excepción para errores sintácticos"""
    def __init__(self, message, token):
        self.message = message
        self.token = token
        super().__init__(
            f"Error sintáctico en línea {token.line}, columna {token.column}: {message}\n"
            f"Token inesperado: {token.type.name} ('{token.value}')"
        )


class Parser:
    """Analizador sintáctico descendente recursivo"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if self.tokens else None
    
    def advance(self):
        """Avanza al siguiente token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def peek(self, offset=1):
        """Mira el token a 'offset' posiciones adelante sin avanzar"""
        peek_pos = self.pos + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None
    
    def expect(self, token_type: TokenType) -> Token:
        """Verifica que el token actual sea del tipo esperado y avanza"""
        if self.current_token is None:
            raise ParserError(
                f"Se esperaba {token_type.name} pero se llegó al final del archivo",
                Token(TokenType.EOF, "", 0, 0)
            )
        
        if self.current_token.type != token_type:
            raise ParserError(
                f"Se esperaba {token_type.name}",
                self.current_token
            )
        
        token = self.current_token
        self.advance()
        return token
    
    def match(self, *token_types: TokenType) -> bool:
        """Verifica si el token actual coincide con alguno de los tipos dados"""
        if self.current_token is None:
            return False
        return self.current_token.type in token_types
    
    # ========================================================================
    # PROGRAMA Y MÓDULO
    # ========================================================================
    
    def parse(self) -> Program:
        """Punto de entrada: Program → ModuleDecl ImportList TopList EOF"""
        try:
            module_decl = self.parse_module_decl()
            imports = self.parse_import_list()
            top_declarations = self.parse_top_list()
            self.expect(TokenType.EOF)
            
            return Program(module_decl, imports, top_declarations)
        except ParserError as e:
            raise e
        
    
    def parse_module_decl(self) -> ModuleDecl:
        """ModuleDecl → module QualID ';'"""
        self.expect(TokenType.MODULE)
        qualified_id = self.parse_qual_id()
        self.expect(TokenType.SEMICOLON)
        return ModuleDecl(qualified_id)
    
    def parse_qual_id(self) -> QualID:
        """QualID → ID ('.' ID)*"""
        identifiers = []
        identifiers.append(self.expect(TokenType.ID).value)
        
        while self.match(TokenType.DOT):
            self.advance()  # consumir '.'
            identifiers.append(self.expect(TokenType.ID).value)
        
        return QualID(identifiers)
    
    # ========================================================================
    # IMPORTS
    # ========================================================================
    
    def parse_import_list(self) -> List[ImportDecl]:
        """ImportList → ImportDecl ImportList | ε"""
        imports = []
        while self.match(TokenType.IMPORT):
            imports.append(self.parse_import_decl())
        return imports
    
    def parse_import_decl(self) -> ImportDecl:
        """ImportDecl → import QualID AsOpt ';'"""
        self.expect(TokenType.IMPORT)
        qualified_id = self.parse_qual_id()
        alias = self.parse_as_opt()
        self.expect(TokenType.SEMICOLON)
        return ImportDecl(qualified_id, alias)
    
    def parse_as_opt(self) -> Optional[str]:
        """AsOpt → as ID | ε"""
        if self.match(TokenType.AS):
            self.advance()
            return self.expect(TokenType.ID).value
        return None
    
    # ========================================================================
    # DECLARACIONES DE NIVEL SUPERIOR
    # ========================================================================
    
    def parse_top_list(self) -> List[TopDecl]:
        """TopList → TopDecl TopList | ε"""
        declarations = []
        while not self.match(TokenType.EOF):
            declarations.append(self.parse_top_decl())
        return declarations
    
    def parse_top_decl(self) -> TopDecl:
        """TopDecl → TypeDecl | StructDecl | ConstDecl | FunDecl | LetDecl"""
        if self.match(TokenType.TYPE):
            return self.parse_type_decl()
        elif self.match(TokenType.STRUCT):
            return self.parse_struct_decl()
        elif self.match(TokenType.CONST):
            return self.parse_const_decl()
        elif self.match(TokenType.FN):
            return self.parse_fun_decl()
        elif self.match(TokenType.LET):
            return self.parse_let_decl()
        else:
            raise ParserError(
                "Se esperaba una declaración (type, struct, const, fn, let)",
                self.current_token
            )
    
    def parse_type_decl(self) -> TypeDecl:
        """TypeDecl → type ID '=' Type ';'"""
        self.expect(TokenType.TYPE)
        name = self.expect(TokenType.ID).value
        self.expect(TokenType.ASSIGN)
        type_expr = self.parse_type()
        self.expect(TokenType.SEMICOLON)
        return TypeDecl(name, type_expr)
    
    def parse_struct_decl(self) -> StructDecl:
        """StructDecl → struct ID '{' FieldList '}' ';'"""
        self.expect(TokenType.STRUCT)
        name = self.expect(TokenType.ID).value
        self.expect(TokenType.LBRACE)
        fields = self.parse_field_list()
        self.expect(TokenType.RBRACE)
        self.expect(TokenType.SEMICOLON)
        return StructDecl(name, fields)
    
    def parse_field_list(self) -> List[Field]:
        """FieldList → Field FieldListTail | ε"""
        fields = []
        if self.match(TokenType.ID):
            fields.append(self.parse_field())
            while self.match(TokenType.COMMA):
                self.advance()  # consumir ','
                fields.append(self.parse_field())
        return fields
    
    def parse_field(self) -> Field:
        """Field → ID ':' Type"""
        name = self.expect(TokenType.ID).value
        self.expect(TokenType.COLON)
        field_type = self.parse_type()
        return Field(name, field_type)
    
    def parse_const_decl(self) -> ConstDecl:
        """ConstDecl → const ID ':' Type '=' Expr ';'"""
        self.expect(TokenType.CONST)
        name = self.expect(TokenType.ID).value
        self.expect(TokenType.COLON)
        const_type = self.parse_type()
        self.expect(TokenType.ASSIGN)
        value = self.parse_expr()
        self.expect(TokenType.SEMICOLON)
        return ConstDecl(name, const_type, value)
    
    def parse_fun_decl(self) -> FunDecl:
        """FunDecl → fn ID '(' ParamListOpt ')' RetType Block"""
        self.expect(TokenType.FN)
        name = self.expect(TokenType.ID).value
        self.expect(TokenType.LPAREN)
        parameters = self.parse_param_list_opt()
        self.expect(TokenType.RPAREN)
        return_type = self.parse_ret_type()
        body = self.parse_block()
        return FunDecl(name, parameters, return_type, body)
    
    def parse_param_list_opt(self) -> List[Param]:
        """ParamListOpt → ParamList | ε"""
        if self.match(TokenType.ID):
            return self.parse_param_list()
        return []
    
    def parse_param_list(self) -> List[Param]:
        """ParamList → Param ParamListTail"""
        params = [self.parse_param()]
        while self.match(TokenType.COMMA):
            self.advance()  # consumir ','
            params.append(self.parse_param())
        return params
    
    def parse_param(self) -> Param:
        """Param → ID ':' Type"""
        name = self.expect(TokenType.ID).value
        self.expect(TokenType.COLON)
        param_type = self.parse_type()
        return Param(name, param_type)
    
    def parse_ret_type(self) -> Optional[Type]:
        """RetType → '->' Type | ε"""
        if self.match(TokenType.ARROW):
            self.advance()
            return self.parse_type()
        return None
    
    def parse_let_decl(self) -> LetDecl:
        """LetDecl → let ID ':' Type LetTail"""
        self.expect(TokenType.LET)
        name = self.expect(TokenType.ID).value
        self.expect(TokenType.COLON)
        var_type = self.parse_type()
        initial_value = self.parse_let_tail()
        return LetDecl(name, var_type, initial_value)
    
    def parse_let_tail(self) -> Optional[Expr]:
        """LetTail → '=' Expr ';' | ';'"""
        if self.match(TokenType.ASSIGN):
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenType.SEMICOLON)
            return expr
        else:
            self.expect(TokenType.SEMICOLON)
            return None
    
    # ========================================================================
    # TIPOS
    # ========================================================================
    
    def parse_type(self) -> Type:
        """Type → SimpleType ArrOrFunType"""
        simple_type = self.parse_simple_type()
        return self.parse_arr_or_fun_type(simple_type)
    
    def parse_simple_type(self) -> Type:
        """SimpleType → int | bool | string | QualID | '(' Type ')'"""
        if self.match(TokenType.INT):
            self.advance()
            return SimpleType("int")
        elif self.match(TokenType.BOOL):
            self.advance()
            return SimpleType("bool")
        elif self.match(TokenType.STRING):
            self.advance()
            return SimpleType("string")
        elif self.match(TokenType.ID):
            qual_id = self.parse_qual_id()
            return SimpleType(str(qual_id))
        elif self.match(TokenType.LPAREN):
            self.advance()
            type_expr = self.parse_type()
            self.expect(TokenType.RPAREN)
            return type_expr
        else:
            raise ParserError("Se esperaba un tipo (int, bool, string, ID, o '(')", self.current_token)
    
    def parse_arr_or_fun_type(self, base_type: Type) -> Type:
        """ArrOrFunType → '[' ']' ArrOrFunType | ε"""
        if self.match(TokenType.LBRACKET):
            self.advance()
            self.expect(TokenType.RBRACKET)
            # El tipo base se convierte en el tipo de elemento del array
            array_type = ArrayType(base_type)
            # Recursión para manejar arrays multidimensionales
            return self.parse_arr_or_fun_type(array_type)
        return base_type
    
    # ========================================================================
    # STATEMENTS
    # ========================================================================
    
    def parse_block(self) -> Block:
        """Block → '{' StmtList '}'"""
        self.expect(TokenType.LBRACE)
        statements = self.parse_stmt_list()
        self.expect(TokenType.RBRACE)
        return Block(statements)
    
    def parse_stmt_list(self) -> List[Stmt]:
        """StmtList → Stmt StmtList | ε"""
        statements = []
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            statements.append(self.parse_stmt())
        return statements
    
    def parse_stmt(self) -> Stmt:
        """Stmt → LetDecl | ExprStmt | IfStmt | WhileStmt | ReturnStmt | Block"""
        if self.match(TokenType.LET):
            return self.parse_let_decl()
        elif self.match(TokenType.IF):
            return self.parse_if_stmt()
        elif self.match(TokenType.WHILE):
            return self.parse_while_stmt()
        elif self.match(TokenType.RETURN):
            return self.parse_return_stmt()
        elif self.match(TokenType.LBRACE):
            return self.parse_block()
        else:
            return self.parse_expr_stmt()
    
    def parse_expr_stmt(self) -> ExprStmt:
        """ExprStmt → Expr ';'"""
        expr = self.parse_expr()
        self.expect(TokenType.SEMICOLON)
        return ExprStmt(expr)
    
    def parse_if_stmt(self) -> IfStmt:
        """IfStmt → if '(' Expr ')' Stmt ElseOpt"""
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expr()
        self.expect(TokenType.RPAREN)
        then_stmt = self.parse_stmt()
        else_stmt = self.parse_else_opt()
        return IfStmt(condition, then_stmt, else_stmt)
    
    def parse_else_opt(self) -> Optional[Stmt]:
        """ElseOpt → else Stmt | ε"""
        if self.match(TokenType.ELSE):
            self.advance()
            return self.parse_stmt()
        return None
    
    def parse_while_stmt(self) -> WhileStmt:
        """WhileStmt → while '(' Expr ')' Stmt"""
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expr()
        self.expect(TokenType.RPAREN)
        body = self.parse_stmt()
        return WhileStmt(condition, body)
    
    def parse_return_stmt(self) -> ReturnStmt:
        """ReturnStmt → return Expr ';' | return ';'"""
        self.expect(TokenType.RETURN)
        if self.match(TokenType.SEMICOLON):
            self.advance()
            return ReturnStmt(None)
        else:
            value = self.parse_expr()
            self.expect(TokenType.SEMICOLON)
            return ReturnStmt(value)
    
    # ========================================================================
    # EXPRESIONES (con precedencia de operadores)
    # ========================================================================
    
    def parse_expr(self) -> Expr:
        """Expr → Assign"""
        return self.parse_assign()
    
    def parse_assign(self) -> Expr:
        """Assign → Or AssignTail"""
        expr = self.parse_or()
        
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_assign()  # Asociatividad derecha
            return Assignment(expr, value)
        
        return expr
    
    def parse_or(self) -> Expr:
        """Or → And OrTail"""
        left = self.parse_and()
        
        while self.match(TokenType.OR):
            op = self.current_token.value
            self.advance()
            right = self.parse_and()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_and(self) -> Expr:
        """And → Eq AndTail"""
        left = self.parse_eq()
        
        while self.match(TokenType.AND):
            op = self.current_token.value
            self.advance()
            right = self.parse_eq()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_eq(self) -> Expr:
        """Eq → Rel EqTail"""
        left = self.parse_rel()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.current_token.value
            self.advance()
            right = self.parse_rel()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_rel(self) -> Expr:
        """Rel → Add RelTail"""
        left = self.parse_add()
        
        while self.match(TokenType.LESS_THAN, TokenType.LESS_EQUAL,
                         TokenType.GREATER_THAN, TokenType.GREATER_EQUAL):
            op = self.current_token.value
            self.advance()
            right = self.parse_add()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_add(self) -> Expr:
        """Add → Mul AddTail"""
        left = self.parse_mul()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            self.advance()
            right = self.parse_mul()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_mul(self) -> Expr:
        """Mul → Unary MulTail"""
        left = self.parse_unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.current_token.value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_unary(self) -> Expr:
        """Unary → '!' Unary | '-' Unary | Postfix"""
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> Expr:
        """Postfix → Primary PostfixTail"""
        expr = self.parse_primary()
        return self.parse_postfix_tail(expr)
    
    def parse_postfix_tail(self, expr: Expr) -> Expr:
        """PostfixTail → '(' ArgListOpt ')' PostfixTail | '[' Expr ']' PostfixTail | '.' ID PostfixTail | ε"""
        while True:
            if self.match(TokenType.LPAREN):
                # Llamada a función
                self.advance()
                args = self.parse_arg_list_opt()
                self.expect(TokenType.RPAREN)
                
                # El expr debe ser un identificador para llamadas a función
                if isinstance(expr, Identifier):
                    expr = FunctionCall(expr.name, args)
                else:
                    raise ParserError("Solo los identificadores pueden ser llamados como funciones", self.current_token)
            
            elif self.match(TokenType.LBRACKET):
                # Acceso a array
                self.advance()
                index = self.parse_expr()
                self.expect(TokenType.RBRACKET)
                expr = ArrayAccess(expr, index)
            
            elif self.match(TokenType.DOT):
                # Acceso a miembro
                self.advance()
                member = self.expect(TokenType.ID).value
                expr = MemberAccess(expr, member)
            
            else:
                break
        
        return expr
    
    def parse_arg_list_opt(self) -> List[Expr]:
        """ArgListOpt → ArgList | ε"""
        if not self.match(TokenType.RPAREN):
            return self.parse_arg_list()
        return []
    
    def parse_arg_list(self) -> List[Expr]:
        """ArgList → Expr ArgListTail"""
        args = [self.parse_expr()]
        while self.match(TokenType.COMMA):
            self.advance()
            args.append(self.parse_expr())
        return args
    
    def parse_primary(self) -> Expr:
        """Primary → ID | NUM | STRING | true | false | '(' Expr ')'"""
        if self.match(TokenType.ID):
            name = self.current_token.value
            self.advance()
            return Identifier(name)
        
        elif self.match(TokenType.NUM):
            value = self.current_token.value
            self.advance()
            return NumLiteral(value)
        
        elif self.match(TokenType.STRING_LIT):
            value = self.current_token.value
            self.advance()
            return StringLiteral(value)
        
        elif self.match(TokenType.TRUE):
            self.advance()
            return BoolLiteral(True)
        
        elif self.match(TokenType.FALSE):
            self.advance()
            return BoolLiteral(False)
        
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenType.RPAREN)
            return ParenExpr(expr)
        
        else:
            raise ParserError("Se esperaba una expresión primaria (ID, número, string, true, false, o '(')", self.current_token)