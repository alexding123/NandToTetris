import string
import re

symbols = set("{}()[].,;+-*/&|<>=~")
keywords = set(["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"])
integer = re.compile(r"^\d{1,5}")
identifier_char = re.compile(r"^\w+")
str_constant = re.compile(r"^\".*\"")
long_comment = re.compile(r"/\*[\S\s]*?\*/")
inline_comment = re.compile(r"//.*")
spaces = re.compile(r"[\n\t ]+")

class Tokenizer():
    def __init__(self, f):
        self.corpus = str(open(f).read())
        self._preprocess()
        self.token = ""
        self.token_type = "EMPTY"
        self._pointer = 0

    def has_more_tokens(self):
        return self._pointer < len(self.corpus)
    
    def advance(self):
        if not self.has_more_tokens():
            return

        # eliminate possible whitespace (at most one)
        if self._peek() == " ":
            self._read()

        token_body = self._peek_to_space()

        current = token_body[0]
        # string constant
        if current == "\"":
            match = re.match(str_constant, token_body)
            self.token = match.group(0)[1:-1]
            self.token_type = "stringConstant"
            self._pointer += len(match.group(0))
            return
        # integer
        elif current in string.digits:
            match = re.match(integer, token_body)
            self.token = match.group(0)
            self.token_type = "integerConstant"
            self._pointer += len(self.token)
            return
        # symbol
        elif current in symbols:
            self.token = current
            self.token_type = "symbol"
            self._pointer += 1
            return
        
        # remaining cases: keyword and identifier (both could end with symbols)
        
        for t in token_body[1:]:
            if t in symbols:
                break
            current = current + t
        
        # decide which case
        self.token = current
        self._pointer += len(self.token)
        if current in keywords:
            self.token_type = "keyword"
        else:
            self.token_type = "identifier"
        return
        
    def _preprocess(self):
        self.corpus = re.sub(long_comment, "", self.corpus) # remove long comments
        self.corpus = re.sub(inline_comment, "", self.corpus) # remove short comments
        self.corpus = re.sub(spaces, " ", self.corpus) # shorten all long spaces
        # remove possible trailing whitespace
        if self.corpus[-1] == " ":
            self.corpus = self.corpus[:-1]

    def _read(self):
        t = self.corpus[self._pointer]
        self._pointer += 1
        return t
    
    def _peek(self):
        return self.corpus[self._pointer]
    
    def _peek_to_space(self):
        pointer = self._pointer
        in_unpaired_quote = False
        while pointer < len(self.corpus):
            if self.corpus[pointer] == "\"":
                in_unpaired_quote = not in_unpaired_quote
            if self.corpus[pointer] == " ":
                if not in_unpaired_quote:
                    return self.corpus[self._pointer:pointer]
            pointer += 1
        
        return self.corpus[self._pointer:]