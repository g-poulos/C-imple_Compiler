import sys

group_symbol_list = ["{", "}", "(", ")", "[", "]"]
delimeter_list = [",", ";", "."]
operator_list = ["+", "-", "*", "/"]

group_keyword_list = ["print", "program", "if", "switchcase", "not", "function",
                      "input", "declare", "else", "forcase", "and", "procedure",
                      "while", "incase", "or", "call", "case", "default",
                      "return", "in", "inout"]




class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

    def __str__(self):
        return self.recognized_string + ", family: \"" + \
                self.family + "\", line: " + str(self.line_number)



class Lex:
    bool = True
    file = None

    def __init__(self, current_line, file_name, token):
        self.current_line = current_line
        self.file_name = file_name
        self.token = token

        self.file = open(self.file_name, "r")


    def error(self,family,character):
        if family == "number" and character.isalpha():
            sys.exit("ERROR: Expected number but found " + character + " at line " + str(self.current_line))
        elif family == "number":
            sys.exit("ERROR: Constant exceeded bounds. Value must be between -((2^32)-1) and (2^32)-1. line: " + str(self.current_line))
        elif family == "keyword":
            sys.exit("ERROR: Expected string has length greater than allowed (30) at line " + str(self.current_line))
        elif family == "assignment":
            sys.exit("ERROR: Expected := but found " + character + " at line " + str(self.current_line))
        elif family == "comment":
            sys.exit("ERROR: '#' was not closed, line: " + str(self.current_line))
        else:
            sys.exit("ERROR: " + character + " does not belong to C-imple. line: " + str(self.current_line))


    def is_number(self, character):
        global bool
        recognized_string = ""
        while (True):
            #print(recognized_string)
            if (character.isnumeric()):
                recognized_string = recognized_string + character
            elif (character.isalpha()):
                self.error("number", character)
            else:
                if (int(recognized_string) >= -(pow(2, 32)-1) and
                    int(recognized_string) <= (pow(2, 32)-1)):
                    if character == "":
                        bool = False
                    self.file.seek(self.file.tell() - 1)
                        #print(character)
                    return recognized_string, "number"
                else:
                    self.error("number", character)
            character = self.file.read(1)


    def is_keyword(self, first_char):
        global bool
        recognized_string = first_char
        while True:
            character = self.file.read(1)
            if not character.isnumeric() and not character.isalpha():
                if len(recognized_string) <= 30:
                    if character == "":
                        bool = False
                    self.file.seek(self.file.tell() - 1)
                    #print(character)
                    if recognized_string in group_keyword_list:
                        return recognized_string, "keyword"
                    else:
                        return recognized_string, "identifier"
                else:
                    self.error("keyword", character)
            else:
                recognized_string = recognized_string + character


    def is_assignment(self, first_char):
        recognized_string = ""
        first_character = first_char
        second_character = self.file.read(1)
        recognized_string = first_character + second_character
        if recognized_string == ":=":
            return recognized_string, "assignment"
        else:
            character = first_character + second_character
            self.error("assignment", character)


    def is_rel_operator(self, first_char):
        recognized_string = ""
        character = first_char
        while True:
            if character == "=":
                return character, "relOperator"
            elif character == ">":
                second_char = self.file.read(1)
                if second_char == "=":
                    recognized_string = character + second_char
                    return recognized_string, "relOperator"
                else:
                    self.file.seek(self.file.tell() - 1)
                    return character, "relOperator"
            elif character == "<":
                second_char = self.file.read(1)
                if second_char == "=" or second_char == ">":
                    recognized_string = character + second_char
                    return recognized_string, "relOperator"
                else:
                    self.file.seek(self.file.tell() - 1)
                    return character, "relOperator"


    def is_simple(self, first_char):
        character = first_char
        if (character == "+" or character == "-"):
            return character, "addOperator"
        elif (character == "*" or character == "/"):
            return character, "mulOperator"
        elif (character in group_symbol_list):
            return character, "groupSymbol"
        elif (character in delimeter_list):
            return character, "delimeter"
        else:
            return "a", "a"  # TODO What to do in case of no `.` at the end of the program


    def clear_blank_char(self, character):
        while (True):
            if (not character.isspace()):
                return character
            elif (character == "\n"):
                self.current_line = self.current_line + 1
                character = self.file.read(1)
            else:
                character = self.file.read(1)


    def is_comment(self, character):
        character = self.file.read(1)
        while (character != "#"):
            character = self.file.read(1)
            if (not character):
                self.error("comment", character)
        character = self.file.read(1)
        return character


    def next_token(self, file_pointer):
        self.file.seek(file_pointer)
        family = ""
        recognized_string = ""


        first_char = self.file.read(1)
        file = self.file

        # Clear comments and blank characters
        while first_char.isspace() or first_char == "#":
            if first_char == "#":
                first_char = self.is_comment(first_char)
            else:
                first_char = self.clear_blank_char(first_char)

        if bool == False:
            first_char = "eof"
            family = "eof"

        if first_char.isnumeric():
            recognized_string, family = self.is_number(first_char)
        elif first_char.isalpha():
            recognized_string, family = self.is_keyword(first_char)
        elif first_char == ":":
            recognized_string, family = self.is_assignment(first_char)
        elif first_char == ">" or first_char == "<" or first_char == "=":
            recognized_string, family = self.is_rel_operator(first_char)
        elif first_char in group_symbol_list or first_char in delimeter_list or first_char in operator_list:
            recognized_string, family = self.is_simple(first_char)
        else:
            if first_char == "":
                recognized_string = "eof"
                family = "eof"
            else:
                self.error("", first_char)

        file_pointer = file.tell()
        #print(file_pointer)
        file.seek(0)
        #print(f"{recognized_string:12} family: {family:12} line: {self.current_line:3}")
        return file_pointer, Token(recognized_string, family, self.current_line)

class Parser:
    file_pointer = 0


    def __init__(self, lexical_analyzer):
        global token
        self.lexical_analyzer = lexical_analyzer
        token = lexical_analyzer.token


    def __get_token(self):
        lex = self.lexical_analyzer
        self.file_pointer, token = lex.next_token(self.file_pointer)
        return token

    def syntax_analyzer(self):
        global token
        token = self.__get_token()
        # self.__program()
        # print("Compilation successfully completed")
        self.test()

        # For testing only
        print(f"{token.recognized_string:12} family: {token.family:12} line: {token.line_number:3}")
        return token

    def __error(self, error_code):
        global token
        lex = self.lexical_analyzer

        if error_code == "KEYWORD PROGRAM NOT FOUND":
            print("SYNTAX ERROR: keyword 'program' expected in line"+ str(lex.current_line) +
                    ". \n All programs should start with the keyword 'program'. Instead, \
                    the word " + token.recognized_string + "appeared")
        elif error_code == "EXPECTED REL_OP":
            print("SYNTAX ERROR: Expected rel operator but got " + token.recognized_string +
                    " at line: " + str(lex.current_line))
        elif error_code == "EXPECTED ADD_OP":
            print("SYNTAX ERROR: Expected add operator but got " + token.recognized_string +
                    " at line: " + str(lex.current_line))
        elif error_code == "EXPECTED MUL_OP":
            print("SYNTAX ERROR: Expected mul operator but got " + token.recognized_string +
                    " at line: " + str(lex.current_line))
        elif error_code == "NOT AN INTEGER":
            print("SYNTAX ERROR: Expected integer but got " + token.recognized_string +
                    " at line: " + str(lex.current_line))
        elif error_code == "NOT ID":
            print("SYNTAX ERROR: Expected id but got " + token.recognized_string +
                    " at line: " + str(lex.current_line) + "\nAll id values should start " +
                    "with a letter and consist of letters and numbers")
        elif error_code == "IDTAIL":
            print("SYNTAX ERROR: Expected ')' at line: " + str(lex.current_line))
        elif error_code == "FACTOR1":
            print("SYNTAX ERROR: Expected ')' at line: " + str(lex.current_line))

        sys.exit(1)

    def __program(self):
        global token

        if token.recognized_string == "program":
            token = self.__get_token()
            if token.family == "identifier":
                token = self.__get_token()
                # self.block() TODO block method
                if token.recognized_string == ".":
                    token = self.__get_token()
                    if token.recognized_string == "eof": # TODO make lex return eof at end of file
                        token = self.__get_token()
                    else:
                        print()
                else:
                    print()
            else:
                print()
        else:
            self.__error("KEYWORD PROGRAM NOT FOUND")


    def __block(self):
        self.__declarations()


    def __declarations(self):
        pass


    def __varlist(self):
        pass

    def __subprograms(self):
        pass

    def __subprogram(self):
        pass

    def __formalparlist(self):
        pass

    def __formalparitem(self):
        pass

    def __statements(self):
        pass

    def __blockstatements(self):
        pass

    def statement(self):
        pass

    def assignStat(self):
        pass

    def ifStat(self):
        pass

    def elsepart(self):
        pass

    def __whileStat(self):
        pass

    def __switchcaseStat(self):
        pass

    def __forcaseStat(self):
        pass

    # ---------------------------------------------------

    def __actualparlist(self):
        global token 
        if token.recognized_string == "in" or \
            token.recognized_string == "inout":
            self.__actualparitem()
            
            while token.recognized_string == ",":
                token = self.__get_token()
                self.__actualparitem()

    def __actualparitem(self):
        global token   
        if token.recognized_string == "in":
            token = self.__get_token()
            self.__expression()
        elif token.recognized_string == "inout":
            token = self.__get_token()
            self.__idvalue()

    def boolterm(self):
        global token
        self.__boolfactor()
        while token.recognized_string == "and":
            token = self.__get_token()
            self.__boolfactor()

    def __boolfactor(self):
        global token 
        if token.recognized_string == "not":
            token = self.__get_token()
            if token.recognized_string == "[":
                token = self.__get_token()
                #self.__condition() TODO
    
    def __expression(self):
        global token 
        self.__optionalSign()
        token = self.__get_token()
        self.__term()
        while token.recognized_string == "+" or \
              token.recognized_string == "-":
            self.__muloperator()
            token = self.__get_token()
            self.__term()

    def __term(self):
        global token 
        self.__factor()
        while token.recognized_string == "*" or \
              token.recognized_string == "/": 
            self.__muloperator()
            token = self.__get_token()
            self.__factor()

    def __factor(self):
        global token 
        if token.recognized_string.isnumeric():
            self.__integervalue()
        elif token.recognized_string == "(":
            token = self.__get_token()
            self.__expression()
            if not token.recognized_string == ")":
                self.__error("FACTOR1")
        elif token.recognized_string.isalpha():
            self.__idvalue()
            token = self.__get_token()
            self.__idtail()


    def __idtail(self):
        global token 
        if token.recognized_string == "(":
            token = self.__get_token()
            print(token.__str__())
            self.__actualparlist() 
            
            if not token.recognized_string == ")":
                self.__error("IDTAIL")
    
    def test(self):
        self.__idtail()

    # ---------------------------------------------------

    def __optionalSign(self):
        global token 
        if token.recognized_string == "+" or \
            token.recognized_string == "-":
            self.__addoperator()

    def __reloperator(self):
        global token
        rel_op_list = ["=", "<=", ">=", ">", "<", "<>"]
        if not token.recognized_string in rel_op_list:
            self.__error("EXPECTED REL_OP")
        token = self.__get_token()

    def __addoperator(self):
        global token
        if not token.recognized_string == "+" and \
           not token.recognized_string == "-":
            self.__error("EXPECTED ADD_OP")
        token = self.__get_token()

    def __muloperator(self):
        global token
        if not token.recognized_string == "*" and \
           not token.recognized_string == "/":
            self.__error("EXPECTED MUL_OP")
        token = self.__get_token()

    def __integervalue(self):
        global token
        for i in range(len(token.recognized_string)):
            if not token.recognized_string[i].isnumeric():
                self.__error("NOT AN INTEGER")
        token = self.__get_token()

    def __idvalue(self):
        global token
        if not token.recognized_string[0].isalpha():
            self.__error("NOT ID")
        for i in range(1, len(token.recognized_string)-1):
            if not token.recognized_string[i].isalpha() and \
                not token.recognized_string[i].isnumeric():
                self.__error("NOT ID")
        token = self.__get_token()


def main():
    if (len(sys.argv) != 2):
        # Temporary usage
        sys.exit("ERROR: Usage $ python lex.py <inputfile>")

    token1 = Token("(xaxa, xaxax)", "xaxa", 0)
    lex_object = Lex(1, sys.argv[1], None)
    parser_obj = Parser(lex_object)

    while True:
        parser_obj.syntax_analyzer()
        if token.recognized_string == "eof":
            break

    # fp = 0
    # while True:
    #     fp, token = lex_object.next_token(fp)
    #     print(token.__str__())
    #     if token.recognized_string == "eof":
    #          break
        
    #parser_obj.test()

if __name__ == "__main__":
    main()
