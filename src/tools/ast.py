class Node:
    def __str__(self):
        self._type = 'Object'
        return "<Node>"
    def type_of(self):
        return 'Object'
    def set_type(self,newtype):
        self._type = newtype

class TypeAnotationNode(Node):
    def __init__(self, type):
        self.type = type
    def __str__(self):
        return "<TypeAnotationNode>"
    def type_of(self):
        return self.type

class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements
    def __str__(self):
        ret = "<ProgramNode>"
        for statem in self.statements:
            ret+=str(statem)
        return ret

class StatementNode(Node):
    def __str__(self):
        return "<StatementNode>"

class ExpNode(Node):
    def __str__(self):
        return "<ExpNode>"

class VarsDeclListNode(StatementNode):
    def __init__(self, decls, body):
        self.decls = decls
        self.body = body
    def __str__(self):
        return f"<VarsDeclListNode>: {str(self.decls)} in {str(self.body)}"

class VarDeclNode(StatementNode):
    def __init__(self, idx, expr , forced_type = 'Object'):
        self.id = idx
        self.expr = expr

    def __str__(self):
        return f"<VarDeclNode>: let {self.id} = { str(self.expr) }"

    def type_of(self):
        if self.expr.typeof() is not None:
            return self.expr.typeof()
        else:
            return 'Object'

class VarAssign(StatementNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr
    def __str__(self):
        return f"<VarAssign> {self.id} := {str(self.expr)}"
    def type_of(self):
        if self.expr.typeof() is not None:
            return self.expr.typeof()
        else:
            return 'Object'

class FuncFullDeclNode(StatementNode):
    def __init__(self, idx, params, body):
        self.id = idx
        self.params = params
        self.body = body
    def __str__(self):
        return f"<FuncFullDeclNode> {self.id} ({str(self.params)}) {str(self.body)}"

    def type_of(self):
        if self.body.type_of() is not None:
            return self.body.type_of()
        else:
            return 'Void'

class FuncInlineDeclNode(StatementNode):
    def __init__(self, idx, params, body):
        self.id = idx
        self.params = params
        self.body = body
    def __str__(self):
        return f"<FuncInlineDeclNode> {self.id}{str(self.params)} => {str(self.body)}"

    def type_of(self):
        if self.body.typeof() is not None:
            return self.body.typeof()
        else:
            return 'Void'

class TypeDeclNode(StatementNode):
    def __init__(self, idx, args, features, inherit=None):
        self.id = idx
        self.args = args
        self.features = features
        self.inherit = inherit
    def __str__(self):
        return f"<TypeDeclNode> type {self.id} {self.features}"

    def type_of(self):
        return "Void"

class TypeInheritNode(StatementNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args
    def __str__(self):
        return "<TypeInheritNode>"

class AttrDeclNode(StatementNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr
    def __str__(self):
        return f"<AttrDeclNode> {self.id} {str(self.expr)}"

    def type_of(self):
        return self.expr.typeof()
    

class VecDecExplSyntaxNode(StatementNode):
    def __init__(self, args):
        self.args = args
    def __str__(self):
        return f"<VecDecExplSyntaxNode> {str(self.args)}"

    def type_of(self):
        return "Vector"
class VecDecImplSyntaxNode(ExpNode):
    def __init__(self, expr, var, in_):
        self.expr = expr
        self.var = var
        self.in_ = in_
    def __str__(self):
        return "<VecDecImplSyntaxNode>"

    def type_of(self):
        return "Vector"

class VecInstNode(ExpNode):
    def __init__(self, var, index):
        self.var = var
        self.index = index
    def __str__(self):
        return "<VecInstNode>"

    def type_of(self):
        return "Vector"
class ProtocolNode(ExpNode):
    def __init__(self, idx, methods, extends=None):
        self.id = idx
        self.extends = extends
        self.methods = methods
    def __str__(self):
        return "<ProtocolNode>"

class ProtocolMethod(ExpNode):
    def __init__(self, idx, typex, params , reType ="Object"):
        self.id = idx
        self.type = typex
        self.params = params
    def __str__(self):
        return "<ProtocolMethod>"
    def type_of(self):
        return self.retType

class AtomicNode(ExpNode):
    def __init__(self, lex):
        self.lex = lex
    def __str__(self):
        return "<AtomicNode>"

class BinaryNode(ExpNode):
    def __init__(self, lnode, rnode):
        self.left = lnode
        self.right = rnode
    def __str__(self):
        return "<BinaryNode>"
    def type_of(self):
        try:
            return self.lnode.type_of()
        except:
            return 'Object'

class BlockNode(ExpNode):
    def __init__(self, exprs):
        self.exprs = exprs
    def __str__(self):
        return "<BlockNode>"
    def type_of(self):
        return self.exprs[-1].type_of()

class CallNode(ExpNode):
    def __init__(self, idx, args, obj=None, typex=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex
    def __str__(self):
        return "<CallNode>"
    def type_of(self):
        return self._type

class CallTypeAttr(ExpNode):
    def __init__(self, type_id, attr):
        self.type_id = type_id
        self.attr = attr
    def __str__(self):
        return "<CallTypeAttr>"

    def type_of(self):
        return "Object"

class CallTypeFunc(ExpNode):
    def __init__(self, type_id, func):
        self.type_id = type_id
        self.func = func
    def __str__(self):
        return "<CallTypeFunc>"

    def type_of(self):
        return self.func.type_of()

class NumberNode(AtomicNode):
    def type_of(self):
        return "Number"

class StringNode(AtomicNode):
    def type_of(self):
        return "String"

class BooleanNode(AtomicNode):
    def type_of(self):
        return "Bool"

class VarNode(AtomicNode):
    def __init__(self, id, type='Object'):
        self.id = id
        self.type = type
    def __str__(self):
        return "<VarNode>"
    def type_of(self):
        return self.type

class InstantiateTypeNode(ExpNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args
    def __str__(self):
        return "<InstantiateTypeNode>"
    def type_of(self):
        return self.idx

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass

class PowNode(BinaryNode):
    pass

class AndNode(BinaryNode):
    pass

class OrNode(BinaryNode):
    pass

class NotNode(AtomicNode):
    pass

class GreaterThatNode(BinaryNode):
    pass

class LessThatNode(BinaryNode):
    pass

class GreaterOrEqualThatNode(BinaryNode):
    pass

class LessOrEqualThatNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
    pass

class NotEqualNode(BinaryNode):
    pass

class StringSimpleConcatNode(BinaryNode):
    pass

class StringSpaceConcatNode(BinaryNode):
    pass

class WhileLoopNode(ExpNode):
    def __init__(self, expr, body):
        self.expr = expr
        self.body = body
    def __str__(self):
        return "<WhileLoopNode>"
    def type_of(self):
        return self.body.type_of()

class ForLoopNode(ExpNode):
    def __init__(self, var, expr, body):
        self.var = var
        self.expr = expr
        self.body = body
    def __str__(self):
        return "<ForLoopNode>"
    def type_of(self):
        return self.body.type_of()

class IfNode(ExpNode):
    def __init__(self, if_expr, then_expr, else_expr) -> None:
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr
    def __str__(self):
        return "<IfNode>"
    def type_of(self):
        return self.body.type_of()

class ParamNode(StatementNode):
    def __init__(self, idx, typex=None):
        self.id = idx
        self.type = typex
    def __str__(self):
        return "<ParamNode>"
    def type_of(self):
        return self.typex

class ParenthesisExpr(ExpNode): #Exp between parenthesis
    def __init__(self, expr):
        self.expr = expr
    def __str__(self):
        return "<ParenthesisExpr>"
    
