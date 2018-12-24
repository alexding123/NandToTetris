from tokenizer import Tokenizer
from xml.sax.saxutils import escape

class CompilationEngine:
    def __init__(self, fin, fout):
        t = Tokenizer(fin)
        self.tokens = []
        while t.has_more_tokens():
            t.advance()
            self.tokens.append((t.token_type, t.token))
        
        self._pointer = 0

        self.fout = open(fout, "w")
        self.compile_class()
        self.fout.close()
    
    def get_token(self):
        if self._pointer < len(self.tokens):
            token_type, token = self.tokens[self._pointer]
            self._pointer += 1
            return token_type, token
    
    def peek_token(self):
        if self._pointer < len(self.tokens):
            token_type, token = self.tokens[self._pointer]
            return token_type, token
    
    def write_token(self):
        token_type, token = self.get_token()
        self.fout.write("<{0}>{1}</{0}>\n".format(token_type, escape(token)))
        self.fout.flush()

    def write_start(self, token_type):
        self.fout.write("<{}>\n".format(token_type))
    
    def write_end(self, token_type):
        self.fout.write("</{}>\n".format(token_type))

    def compile_class(self):
        self.write_start("class")
        self.write_token()
        self.write_token()
        self.write_token()
        while self._is_class_var_dec():
            self.compile_class_var_dec()
        while self._is_subroutine_dec():
            self.compile_subroutine_dec()
        self.write_token()
        self.write_end("class")
    
    def _is_class_var_dec(self):
        class_var_dec = set(["static", "field"])
        return self.peek_token()[1] in class_var_dec
        
    def _is_subroutine_dec(self):
        subroutine_var_dec = set(["constructor", "function", "method"])
        return self.peek_token()[1] in subroutine_var_dec
    
    def compile_class_var_dec(self):
        self.write_start("classVarDec")
        self.write_token()
        self.write_token()
        self.write_token()
        while (self.peek_token()[1] == ","):
            self.write_token()
            self.write_token()
        self.write_token()
        self.write_end("classVarDec")
    
    def compile_subroutine_dec(self):
        self.write_start("subroutineDec")
        self.write_token()
        self.write_token()
        self.write_token()
        self.write_token()
        self.compile_parameter_list()
        self.write_token()
        self.compile_subroutine_body()
        self.write_end("subroutineDec")
    
    def compile_parameter_list(self):
        self.write_start("parameterList")
        while self.peek_token()[1] != ")":
            self.write_token()
        self.write_end("parameterList")
    
    def compile_subroutine_body(self):
        self.write_start("subroutineBody")
        self.write_token()
        while self._is_var_dec():
            self.compile_var_dec()
        self.compile_statements()
        self.write_token()
        self.write_end("subroutineBody")
    
    def _is_var_dec(self):
        return self.peek_token()[1] == "var"
    
    def _is_statement(self):
        statement = set(["let", "if", "while", "do", "return"])
        return self.peek_token()[1] in statement

    def compile_var_dec(self):
        self.write_start("varDec")
        self.write_token()
        self.write_token()
        self.write_token()
        while self.peek_token()[1] == ",":
            self.write_token()
            self.write_token()
        self.write_token()
        self.write_end("varDec")
    
    def compile_statements(self):
        self.write_start("statements")
        while self._is_statement():
            self.compile_statement()
        self.write_end("statements")

    def compile_statement(self):
        peek = self.peek_token()[1]
        if peek == "let":
            self.compile_let_statement()
        elif peek == "if":
            self.compile_if_statement()
        elif peek == "while":
            self.compile_while_statement()
        elif peek == "do":
            self.compile_do_statement()
        elif peek == "return":
            self.compile_return_statement()
    
    def compile_let_statement(self):
        self.write_start("letStatement")
        self.write_token()
        self.write_token()
        # possible [expression]
        if self.peek_token()[1] == "[":
            self.write_token()
            self.compile_expression()
            self.write_token()
        self.write_token()
        self.compile_expression()
        self.write_token()
        self.write_end("letStatement")
    
    def compile_if_statement(self):
        self.write_start("ifStatement")
        self.write_token()
        self.write_token()
        self.compile_expression()
        self.write_token()
        self.write_token()
        self.compile_statements()
        self.write_token()
        if self.peek_token()[1] == "else":
            self.write_token()
            self.write_token()
            self.compile_statements()
            self.write_token()
        self.write_end("ifStatement")
    
    def compile_while_statement(self):
        self.write_start("whileStatement")
        self.write_token()
        self.write_token()
        self.compile_expression()
        self.write_token()
        self.write_token()
        self.compile_statements()
        self.write_token()
        self.write_end("whileStatement")
    
    def compile_do_statement(self):
        self.write_start("doStatement")
        self.write_token()
        self.compile_subroutine_call()
        self.write_token()
        self.write_end("doStatement")
    
    def compile_return_statement(self):
        self.write_start("returnStatement")
        self.write_token()
        if self.peek_token()[1] != ";":
            self.compile_expression()
        self.write_token()
        self.write_end("returnStatement")
    
    def compile_subroutine_call(self, name_needed=True):
        # no start/end needed

        if name_needed:
            self.write_token()
        
        if self.peek_token()[1] == ".":
            self.write_token()
            self.compile_subroutine_call()
            return
        
        self.write_token()
        self.compile_expression_list()
        self.write_token()
        
    def compile_expression(self):
        self.write_start("expression")
        self.compile_term()
        while self._is_op():
            self.write_token()
            self.compile_term()
        self.write_end("expression")
    
    def _is_op(self):
        op = set(["+", "-", "*", "/", "&", "|", "<", ">", "="])
        return self.peek_token()[1] in op
    
    def compile_term(self):
        self.write_start("term")
        token_type, token = self.peek_token()
        if token_type == "integerConstant":
            self.write_token()
        elif token_type == "stringConstant":
            self.write_token()
        elif self._is_keyword_constant():
            self.write_token()
        elif token == "(":
            self.write_token()
            self.compile_expression()
            self.write_token()
        elif self._is_unary_op():
            self.write_token()
            self.compile_term()
        else:
            # remaining cases: varName, varName[expression], subroutineCall
            # compile the varname/subroutineName regardless
            self.write_token()
            token = self.peek_token()[1]
            if token == "[":
                self.write_token()
                self.compile_expression()
                self.write_token()
            elif token == "(" or token == ".":
                self.compile_subroutine_call(name_needed = False)

        self.write_end("term")
    
    def _is_keyword_constant(self):
        keyword_constant = ["true", "false", "null", "this"]
        return self.peek_token()[1] in keyword_constant
    
    def _is_unary_op(self):
        unary_op = ["-", "~"]
        return self.peek_token()[1] in unary_op
    
    def compile_expression_list(self):
        self.write_start("expressionList")
        # for at least 1 expression, it must start with a term
        if self._is_term():
            self.compile_expression()
            while self.peek_token()[1] == ",":
                self.write_token()
                self.compile_expression()
        self.write_end("expressionList")
        
    def _is_term(self):
        return self.peek_token()[1] != ")"
        