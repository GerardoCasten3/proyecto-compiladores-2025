from dataclasses import dataclass
from typing import List, Optional
from abc import ABC, abstractmethod


# ============================================================================
# CLASE BASE PARA TODOS LOS NODOS DEL AST
# ============================================================================

class ASTNode(ABC):
    """Clase base abstracta para todos los nodos del AST"""
    @abstractmethod
    def __repr__(self):
        pass


# ============================================================================
# PROGRAMA Y DECLARACIONES DE NIVEL SUPERIOR
# ============================================================================

@dataclass
class Program(ASTNode):
    """Nodo raíz: module QualID ';' ImportList TopList EOF"""
    module_decl: 'ModuleDecl'
    imports: List['ImportDecl']
    top_declarations: List['TopDecl']
    
    def __repr__(self):
        return f"Program(module={self.module_decl}, imports={self.imports}, decls={self.top_declarations})"


@dataclass
class ModuleDecl(ASTNode):
    """module QualID ';'"""
    qualified_id: 'QualID'
    
    def __repr__(self):
        return f"Module({self.qualified_id})"


@dataclass
class QualID(ASTNode):
    """ID ('.' ID)*"""
    identifiers: List[str]
    
    def __repr__(self):
        return ".".join(self.identifiers)


@dataclass
class ImportDecl(ASTNode):
    """import QualID AsOpt ';'"""
    qualified_id: 'QualID'
    alias: Optional[str]
    
    def __repr__(self):
        if self.alias:
            return f"Import({self.qualified_id} as {self.alias})"
        return f"Import({self.qualified_id})"


# ============================================================================
# DECLARACIONES DE NIVEL SUPERIOR (TopDecl)
# ============================================================================

@dataclass
class TypeDecl(ASTNode):
    """type ID '=' Type ';'"""
    name: str
    type_expr: 'Type'
    
    def __repr__(self):
        return f"TypeDecl({self.name} = {self.type_expr})"


@dataclass
class StructDecl(ASTNode):
    """struct ID '{' FieldList '}' ';'"""
    name: str
    fields: List['Field']
    
    def __repr__(self):
        return f"StructDecl({self.name}, fields={self.fields})"


@dataclass
class Field(ASTNode):
    """ID ':' Type"""
    name: str
    field_type: 'Type'
    
    def __repr__(self):
        return f"{self.name}: {self.field_type}"


@dataclass
class ConstDecl(ASTNode):
    """const ID ':' Type '=' Expr ';'"""
    name: str
    const_type: 'Type'
    value: 'Expr'
    
    def __repr__(self):
        return f"Const({self.name}: {self.const_type} = {self.value})"


@dataclass
class FunDecl(ASTNode):
    """fn ID '(' ParamListOpt ')' RetType Block"""
    name: str
    parameters: List['Param']
    return_type: Optional['Type']
    body: 'Block'
    
    def __repr__(self):
        return f"Function({self.name}, params={self.parameters}, return={self.return_type})"


@dataclass
class Param(ASTNode):
    """ID ':' Type"""
    name: str
    param_type: 'Type'
    
    def __repr__(self):
        return f"{self.name}: {self.param_type}"


# ============================================================================
# TIPOS (Type)
# ============================================================================

@dataclass
class SimpleType(ASTNode):
    """int | bool | string | QualID | '(' Type ')'"""
    type_name: str  # 'int', 'bool', 'string', o un QualID
    
    def __repr__(self):
        return self.type_name


@dataclass
class ArrayType(ASTNode):
    """'[' ']' Type"""
    element_type: 'Type'
    
    def __repr__(self):
        return f"[]{self.element_type}"


@dataclass
class FunctionType(ASTNode):
    """'(' ParamTypeList ')' '->' Type"""
    param_types: List['Type']
    return_type: 'Type'
    
    def __repr__(self):
        params = ", ".join(str(p) for p in self.param_types)
        return f"({params}) -> {self.return_type}"


# Alias para facilitar el uso
Type = SimpleType | ArrayType | FunctionType


# ============================================================================
# STATEMENTS (Stmt)
# ============================================================================

@dataclass
class LetDecl(ASTNode):
    """let ID ':' Type LetTail"""
    name: str
    var_type: 'Type'
    initial_value: Optional['Expr']
    
    def __repr__(self):
        if self.initial_value:
            return f"Let({self.name}: {self.var_type} = {self.initial_value})"
        return f"Let({self.name}: {self.var_type})"


@dataclass
class ExprStmt(ASTNode):
    """Expr ';'"""
    expression: 'Expr'
    
    def __repr__(self):
        return f"ExprStmt({self.expression})"


@dataclass
class IfStmt(ASTNode):
    """if '(' Expr ')' Stmt ElseOpt"""
    condition: 'Expr'
    then_stmt: 'Stmt'
    else_stmt: Optional['Stmt']
    
    def __repr__(self):
        if self.else_stmt:
            return f"If({self.condition}, then={self.then_stmt}, else={self.else_stmt})"
        return f"If({self.condition}, then={self.then_stmt})"


@dataclass
class WhileStmt(ASTNode):
    """while '(' Expr ')' Stmt"""
    condition: 'Expr'
    body: 'Stmt'
    
    def __repr__(self):
        return f"While({self.condition}, body={self.body})"


@dataclass
class ReturnStmt(ASTNode):
    """return Expr ';' | return ';'"""
    value: Optional['Expr']
    
    def __repr__(self):
        if self.value:
            return f"Return({self.value})"
        return "Return()"


@dataclass
class Block(ASTNode):
    """'{' StmtList '}'"""
    statements: List['Stmt']
    
    def __repr__(self):
        return f"Block({len(self.statements)} statements)"


# Alias para facilitar el uso
Stmt = LetDecl | ExprStmt | IfStmt | WhileStmt | ReturnStmt | Block


# ============================================================================
# EXPRESIONES (Expr)
# ============================================================================

# Expresiones Primarias
@dataclass
class NumLiteral(ASTNode):
    """NUM"""
    value: str
    
    def __repr__(self):
        return f"Num({self.value})"


@dataclass
class StringLiteral(ASTNode):
    """STRING"""
    value: str
    
    def __repr__(self):
        return f"String({self.value})"


@dataclass
class BoolLiteral(ASTNode):
    """true | false"""
    value: bool
    
    def __repr__(self):
        return f"Bool({self.value})"


@dataclass
class Identifier(ASTNode):
    """ID"""
    name: str
    
    def __repr__(self):
        return f"Id({self.name})"


@dataclass
class ParenExpr(ASTNode):
    """'(' Expr ')'"""
    expression: 'Expr'
    
    def __repr__(self):
        return f"({self.expression})"


# Expresiones Binarias
@dataclass
class BinaryOp(ASTNode):
    """Operación binaria: left op right"""
    operator: str
    left: 'Expr'
    right: 'Expr'
    
    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"


# Expresiones Unarias
@dataclass
class UnaryOp(ASTNode):
    """Operación unaria: op operand"""
    operator: str
    operand: 'Expr'
    
    def __repr__(self):
        return f"{self.operator}({self.operand})"


# Llamada a función
@dataclass
class FunctionCall(ASTNode):
    """ID '(' ArgListOpt ')'"""
    function_name: str
    arguments: List['Expr']
    
    def __repr__(self):
        args = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.function_name}({args})"


# Acceso a array
@dataclass
class ArrayAccess(ASTNode):
    """Expr '[' Expr ']'"""
    array: 'Expr'
    index: 'Expr'
    
    def __repr__(self):
        return f"{self.array}[{self.index}]"


# Acceso a miembro
@dataclass
class MemberAccess(ASTNode):
    """Expr '.' ID"""
    object: 'Expr'
    member: str
    
    def __repr__(self):
        return f"{self.object}.{self.member}"


# Asignación
@dataclass
class Assignment(ASTNode):
    """Expr '=' Expr"""
    target: 'Expr'
    value: 'Expr'
    
    def __repr__(self):
        return f"({self.target} = {self.value})"


# Alias para facilitar el uso
Expr = (NumLiteral | StringLiteral | BoolLiteral | Identifier | 
        ParenExpr | BinaryOp | UnaryOp | FunctionCall | 
        ArrayAccess | MemberAccess | Assignment)


# ============================================================================
# DECLARACIÓN DE TOP-LEVEL
# ============================================================================

TopDecl = TypeDecl | StructDecl | ConstDecl | FunDecl | LetDecl