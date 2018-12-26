from tokenizer import Tokenizer
from symbol_table import SymbolTable, STATIC, FIELD, ARG, VAR
from vm_writer import VMWriter
from xml.sax.saxutils import escape

T_KEYWORD = "keyword"
T_SYMBOL = "symbol"
T_IDENTIFIER = "identifier"
T_INTCONST = "integerConstant"
T_STRCONST = "stringConstant"

KW_CLASS = "class"
KW_METHOD = "method"
KW_CONSTRUCTOR = "constructor"
KW_VAR = "var"
KW_LET = "let"
KW_IF = "if"
KW_WHILE = "while"
KW_DO = "do"
KW_RETURN = "return"
KW_ELSE = "else"
KW_TRUE = "true"
KW_FALSE = "false"
KW_THIS = "this"

TEMP_ARRAY = 1
TEMP_NULL = 0 

kind_to_segment = {"static":"static", "field":"this", "var":"local", "arg":"argument"}
op_to_command = {"+":"add", "-":"sub", "*":"call Math.multiply 2", "/":"call Math.divide 2",
                 "<":"lt", ">":"gt", "=":"eq", "&":"and", "|":"or"}

unary_op_to_command = {"-":"neg", "~":"not"}

class CompilationEngine:
    def __init__(self, fin, fout):
        t = Tokenizer(fin)
        self.tokens = []
        while t.has_more_tokens():
            t.advance()
            self.tokens.append((t.token_type, t.token))
        
        self._pointer = 0

        self.st = SymbolTable()
        self.vm = VMWriter(fout)
        self.compile_class()
        self.vm.close()
    
    def require(self, token_type, token=None):
        """ Requires a certain token to occur next
            Advances the pointer
        """
        if self._pointer < len(self.tokens):
            got_token_type, got_token = self.tokens[self._pointer]
            if (token_type != got_token_type) or ((token is not None) and ((token_type, token) != (got_token_type, got_token))):
                raise Exception("Expecting {}, got {}".format(token, got_token))
            else:
                self._pointer += 1
                return got_token
        else:
            raise Exception("Expecting {}, but reached EOF".format(token))
    
    def peek_token(self):
        if self._pointer < len(self.tokens):
            token_type, token = self.tokens[self._pointer]
            return token_type, token

    def push_variable(self, name):
        self.vm.write_push(kind_to_segment[self.st.kind_of(name)], self.st.index_of(name))
    
    def pop_variable(self, name):
        self.vm.write_pop(kind_to_segment[self.st.kind_of(name)], self.st.index_of(name))

    label_count = 0
    @classmethod
    def new_label(cls):
        cls.label_count += 1
        return cls.label_count - 1

    def compile_class(self):
        self.require(T_KEYWORD, KW_CLASS)
        self.compile_classname()
        self.require(T_SYMBOL, "{")
        while self._is_class_var_dec():
            self.compile_class_var_dec()
        while self._is_subroutine_dec():
            self.compile_subroutine_dec()
        self.require(T_SYMBOL, "}")
    
    def compile_classname(self):
        self.class_name = self.require(T_IDENTIFIER)
    
    def _is_class_var_dec(self):
        class_var_dec = set(["static", "field"])
        return self.peek_token()[1] in class_var_dec
        
    def _is_subroutine_dec(self):
        subroutine_var_dec = set(["constructor", "function", "method"])
        return self.peek_token()[1] in subroutine_var_dec
    
    def compile_class_var_dec(self):
        kind = self.require(T_KEYWORD)
        self._compile_dec(kind)
    
    def _compile_dec(self, kind):
        type = self.compile_type()
        name = self.require(T_IDENTIFIER)
        self.st.define(name, type, kind)
        while (self.peek_token()[1] == ","):
            self.require(T_SYMBOL, ",")
            name = self.require(T_IDENTIFIER)
            self.st.define(name, type, kind)
        self.require(T_SYMBOL, ";")
    
    def compile_type(self):
        if self.peek_token()[0] == T_KEYWORD:
            return self.require(T_KEYWORD)
        else:
            return self.require(T_IDENTIFIER)
    
    def compile_subroutine_dec(self):
        sub_type = self.require(T_KEYWORD) # method, function, constructor
        self.compile_type() # don't need the type: if void, then `return` has no value; we handle it there
        self.compile_subroutinename()

        # store the value
        self.st.start_subroutine()
        if sub_type == KW_METHOD:
            self.st.define("this", self.class_name, ARG)
        
        self.require(T_SYMBOL, "(")
        self.compile_parameter_list()
        self.require(T_SYMBOL, ")")

        self.compile_subroutine_body(sub_type)
    
    def compile_subroutinename(self):
        self.sub_name = self.require(T_IDENTIFIER)

    def compile_parameter_list(self):
        if self._not_end_parameter_list():
            type = self.compile_type()
            name = self.require(T_IDENTIFIER)
            self.st.define(name, type, ARG)
        while self.peek_token()[1] != ")":
            self.require(T_SYMBOL, ",")
            type = self.compile_type()
            name = self.require(T_IDENTIFIER)
            self.st.define(name, type, ARG)

    def _not_end_parameter_list(self):
        return self.peek_token()[1] != ")"

    def compile_subroutine_body(self, sub_type):
        self.require(T_SYMBOL, "{")
        while self._is_var_dec():
            self.compile_var_dec()
        self.write_subroutine_head(sub_type)
        self.compile_statements()
        self.require(T_SYMBOL, "}")
    
    def _is_var_dec(self):
        return self.peek_token()[1] == KW_VAR

    def compile_var_dec(self):
        self.require(T_KEYWORD, KW_VAR)
        self._compile_dec(VAR)
    
    def write_subroutine_head(self, sub_type):
        self.vm.write_function(self.class_name + "." + self.sub_name, self.st.var_count(VAR))
        if sub_type == KW_METHOD:
            self.vm.write_push("argument", 0)
            self.vm.write_pop("pointer", 0)
        elif sub_type == KW_CONSTRUCTOR:
            self.vm.write_push("constant", self.st.var_count(FIELD))
            self.vm.write_call("Memory.alloc", 1)
            self.vm.write_pop("pointer", 0)

    def _is_statement(self):
        statement = set(["let", "if", "while", "do", "return"])
        return self.peek_token()[1] in statement

    def compile_statements(self):
        while self._is_statement():
            self.compile_statement()

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
        self.require(T_KEYWORD, KW_LET)
        name = self.require(T_IDENTIFIER)

        # possible [expression]
        array_access = self.peek_token()[1] == "["
        if array_access:
            self.require(T_SYMBOL, "[")

            # array base access
            self.push_variable(name)
            self.compile_expression()
            self.vm.write_command("add")

            self.require(T_SYMBOL, "]")

        self.require(T_SYMBOL, "=")
        self.compile_expression()
        if array_access:
            self.vm.write_pop("temp", TEMP_ARRAY)
            self.vm.write_pop("pointer", 1)
            self.vm.write_push("temp", TEMP_ARRAY)
            self.vm.write_pop("that", 0)
        else:
            self.pop_variable(name)
        self.require(T_SYMBOL, ";")
    
    def compile_if_statement(self):
        self.require(T_KEYWORD, KW_IF)
        self.require(T_SYMBOL, "(")
        self.compile_expression()
        self.vm.write_arithmetic("not")
        l1 = self.new_label()
        l2 = self.new_label()
        self.require(T_SYMBOL, ")")
        self.vm.write_if(l1)
        self.require(T_SYMBOL, "{")
        self.compile_statements()
        self.vm.write_goto(l2)
        self.vm.write_label(l1)
        self.require(T_SYMBOL, "}")
        if self.peek_token()[1] == "else":
            self.require(T_KEYWORD, KW_ELSE)
            self.require(T_SYMBOL, "{")
            self.compile_statements()
            self.require(T_SYMBOL, "}")
        self.vm.write_label(l2)
    
    def compile_while_statement(self):
        l1 = self.new_label()
        l2 = self.new_label()
        self.require(T_KEYWORD, "while")
        self.require(T_SYMBOL, "(")
        self.vm.write_label(l1)
        self.compile_expression()
        self.vm.write_arithmetic("not")
        self.require(T_SYMBOL, ")")
        self.vm.write_if(l2)
        self.require(T_SYMBOL, "{")
        self.compile_statements()
        self.vm.write_goto(l1)
        self.require(T_SYMBOL, "}")
        self.vm.write_label(l2)

    def compile_do_statement(self):
        self.require(T_KEYWORD, KW_DO)
        self.compile_subroutine_call()
        self.vm.write_pop("temp", TEMP_NULL)
        self.require(T_SYMBOL, ";")
    
    def compile_return_statement(self):
        self.require(T_KEYWORD, KW_RETURN)
        if self.peek_token()[1] != ";":
            # yes return value
            self.compile_expression()
        else:
            # no return value
            self.vm.write_push("constant", 0) # write a filler 0 to be discarded
        self.require(T_SYMBOL, ";")
        self.vm.write_return()
    
    def compile_subroutine_call(self, caller=None):
        # no start/end needed
        if caller is None:
            caller = self.require(T_IDENTIFIER)

        if self.peek_token()[1] == ".":
            self.require(T_SYMBOL, ".")
            subcaller = self.require(T_IDENTIFIER)
            if self.st.kind_of(caller) is None: # if caller is a class
                name = caller + "." + subcaller
                n_args = 0
            else: # if caller is a variable
                name = self.st.type_of(caller) + "." + subcaller
                n_args = 1
                self.push_variable(caller)
        else:
            name = self.class_name + "." + caller
            n_args = 1
            self.vm.write_push("pointer", 0)
        
        self.require(T_SYMBOL, "(")
        n_args += self.compile_expression_list()
        self.require(T_SYMBOL, ")")
        self.vm.write_call(name, n_args)
        
    def compile_expression(self):
        self.compile_term()
        while self._is_op():
            op = self.require(T_SYMBOL)
            self.compile_term()
            self.vm.write_arithmetic(op_to_command[op])
    
    def _is_op(self):
        op = set(["+", "-", "*", "/", "&", "|", "<", ">", "="])
        return self.peek_token()[1] in op
    
    def compile_term(self):
        token_type, token = self.peek_token()
        if token_type == T_INTCONST:
            i = self.require(T_INTCONST)
            self.vm.write_push("constant", i)
        elif token_type == T_STRCONST:
            s = self.require(T_STRCONST)
            self.compile_string_const(s)
        elif self._is_keyword_constant():
            kw = self.require(T_KEYWORD)
            self.compile_keyword_const(kw)
        elif token == "(":
            self.require(T_SYMBOL, "(")
            self.compile_expression()
            self.require(T_SYMBOL, ")")
        elif self._is_unary_op():
            op = self.require(T_SYMBOL)
            self.compile_term()
            self.vm.write_arithmetic(unary_op_to_command[op])
        else:
            # remaining cases: varName, varName[expression], subroutineCall
            # compile the varname/subroutineName regardless
            name = self.require(T_IDENTIFIER)
            token = self.peek_token()[1]
            if token == "[":
                self.require(T_SYMBOL, "[")
                self.push_variable(name)
                self.compile_expression()
                self.vm.write_command("add")
                self.vm.write_pop("pointer", TEMP_ARRAY)
                self.vm.write_push("that", 0)
                self.require(T_SYMBOL, "]")
            elif token == "(" or token == ".":
                self.compile_subroutine_call(name)
            else:
                # all the previous two cases end up with the final value on the stack
                # we just need to do the same here
                self.push_variable(name)
    
    def compile_string_const(self, s):
        self.vm.write_push("constant", len(s))
        self.vm.write_call("String.new", 1)
        for c in s:
            self.vm.write_push("constant", ord(c))
            self.vm.write_call("String.appendChar", 2)

    def compile_keyword_const(self, kw):
        # set([true, false, null, this])
        if kw == KW_TRUE:
            self.vm.write_push("constant", 1) # -1
            self.vm.write_arithmetic("neg")
        elif kw == KW_THIS:
            self.vm.write_push("pointer", 0)
        else: # false or null
            self.vm.write_push("constant", 0)

    def _is_keyword_constant(self):
        keyword_constant = ["true", "false", "null", "this"]
        return self.peek_token()[1] in keyword_constant
    
    def _is_unary_op(self):
        unary_op = ["-", "~"]
        return self.peek_token()[1] in unary_op
    
    def compile_expression_list(self):
        n_arg = 0
        # for at least 1 expression, it must start with a term
        if self._is_term():
            self.compile_expression()
            n_arg += 1
            while self.peek_token()[1] == ",":
                n_arg += 1
                self.require(T_SYMBOL, ",")
                self.compile_expression()
        return n_arg
        
    def _is_term(self):
        return self.peek_token()[1] != ")"
        