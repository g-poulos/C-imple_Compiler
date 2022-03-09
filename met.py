# Dimitropoulos Dimitrios, 4352, cse84352
# Poulos Grigorios, 4480, cse84480

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


    def __error(self,family,character):
        if family == "number" and character.isalpha():
            sys.exit("ERROR: Expected number but found " + character + " in line " 
                        + str(self.current_line))
        elif family == "number":
            sys.exit("ERROR: Constant exceeded bounds. Value must be between " + 
                        "-((2^32)-1) and (2^32)-1. line: " + str(self.current_line))
        elif family == "keyword":
            sys.exit("ERROR: Expected string has length greater than allowed (30) in line "
                         + str(self.current_line))
        elif family == "assignment":
            sys.exit("ERROR: Expected := but found '" + character + "' in line " 
                        + str(self.current_line))
        elif family == "comment":
            sys.exit("ERROR: '#' was not closed, line: " + str(self.current_line))
        else:
            sys.exit("ERROR: '" + character + "' does not belong to C-imple. line: " 
                        + str(self.current_line))


    def __is_number(self, character):
        global bool
        recognized_string = ""
        while (True):
            if (character.isnumeric()):
                recognized_string = recognized_string + character
            elif (character.isalpha()):
                self.__error("number", character)
            else:
                if (int(recognized_string) >= -(pow(2, 32) - 1) and
                        int(recognized_string) <= (pow(2, 32) - 1)):
                    if character == "":
                        bool = False
                    self.file.seek(self.file.tell() - 1)
                    return recognized_string, "number"
                else:
                    self.__error("number", character)
            character = self.file.read(1)


    def __is_keyword(self, first_char):
        global bool
        recognized_string = first_char
        while True:
            character = self.file.read(1)
            if not character.isnumeric() and not character.isalpha():
                if len(recognized_string) <= 30:
                    if character == "":
                        bool = False
                    self.file.seek(self.file.tell() - 1)
                    # print(character)
                    if recognized_string in group_keyword_list:
                        return recognized_string, "keyword"
                    else:
                        return recognized_string, "identifier"
                else:
                    self.__error("keyword", character)
            else:
                recognized_string = recognized_string + character


    def __is_assignment(self, first_char):
        recognized_string = ""
        first_character = first_char
        second_character = self.file.read(1)
        recognized_string = first_character + second_character
        if recognized_string == ":=":
            return recognized_string, "assignment"
        else:
            character = first_character + second_character
            self.__error("assignment", character)


    def __is_rel_operator(self, first_char):
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


    def __is_single_char(self, first_char):
        character = first_char
        if (character == "+" or character == "-"):
            return character, "addOperator"
        elif (character == "*" or character == "/"):
            return character, "mulOperator"
        elif (character in group_symbol_list):
            return character, "groupSymbol"
        elif (character in delimeter_list):
            return character, "delimeter"


    def __clear_blank_char(self, character):
        while (True):
            if (not character.isspace()):
                return character
            elif (character == "\n"):
                self.current_line = self.current_line + 1
                character = self.file.read(1)
            else:
                character = self.file.read(1)


    def __is_comment(self, character):
        character = self.file.read(1)
        while (character != "#"):
            character = self.file.read(1)
            if (not character):
                self.__error("comment", character)
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
                first_char = self.__is_comment(first_char)
            else:
                first_char = self.__clear_blank_char(first_char)

        if bool == False:
            first_char = "eof"
            family = "eof"

        if first_char.isnumeric():
            recognized_string, family = self.__is_number(first_char)
        elif first_char.isalpha():
            recognized_string, family = self.__is_keyword(first_char)
        elif first_char == ":":
            recognized_string, family = self.__is_assignment(first_char)
        elif first_char == ">" or first_char == "<" or first_char == "=":
            recognized_string, family = self.__is_rel_operator(first_char)
        elif first_char in group_symbol_list or first_char in delimeter_list or first_char in operator_list:
            recognized_string, family = self.__is_single_char(first_char)
        else:
            if first_char == "":
                recognized_string = "eof"
                family = "eof"
            else:
                self.__error("", first_char)

        file_pointer = file.tell()
        # print(file_pointer)
        file.seek(0)
        # print(f"{recognized_string:12} family: {family:12} line: {self.current_line:3}")
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
        self.__program()
        print("Compilation successfully completed")

        # For testing only
        # print(f"{token.recognized_string:12} family: {token.family:12} line: {token.line_number:3}")
        return token

    def __error(self, error_code):

        error_codes = ["IDTAIL", "FACTOR1", "inputStat", "printStat", "callStat", "returnStat",
                        "incaseStat", "FORSTAT_)", "SWITCHCASESTAT_)", "WHILESTAT_)", "IFSTAT_)", "subprogram"]

        case_stat =["FORSTAT_(", "SWITCHCASESTAT_("]

        global token
        lex = self.lexical_analyzer

        if error_code == "KEYWORD PROGRAM NOT FOUND":
            print("SYNTAX ERROR: keyword 'program' expected in line " + str(lex.current_line) +
                  ".\nAll programs should start with the keyword 'program'.Instead, " +
                  "the word '" + token.recognized_string + "' appeared.")

        elif error_code == "EXPECTED REL_OP":
            print("SYNTAX ERROR: Expected rel operator in line " + str(lex.current_line) + "\n" + " '"
                  + token.recognized_string + "' appeared.")

        elif error_code == "EXPECTED ADD_OP":
            print("SYNTAX ERROR: Expected add operator in line " + str(lex.current_line) + "\n" + " '"
                  + token.recognized_string + "' appeared.")

        elif error_code == "EXPECTED MUL_OP":
            print("SYNTAX ERROR: Expected mul operator in line " + str(lex.current_line) + "\n" + " '"
                  + token.recognized_string + "' appeared.")

        elif error_code == "NOT AN INTEGER":
            print("SYNTAX ERROR: Expected integer in line " + str(lex.current_line) +
                  "\nbut '" + token.recognized_string + "' appeared.")

        elif error_code == "NOT ID":
            print("SYNTAX ERROR: Expected id in line " + str(lex.current_line) +
                  "\nbut '" + token.recognized_string + "' appeared." +
                  "\nAll id values should start with a letter and consist of letters and numbers.")

        elif error_code == "FORSTAT_DEFAULT":
            print("SYNTAX ERROR: Missing 'default' case in line: " + str(lex.current_line))

        elif error_code == "assignStat":
            print("SYNTAX ERROR: Expected ':=' in line " + str(lex.current_line) +
                  " but " + token.recognized_string + " appeared.")

        elif error_code in error_codes:
            print("SYNTAX ERROR: Expected ')' in line " + str(lex.current_line) +
                  " but " + token.recognized_string + " appeared.")

        elif error_code in case_stat:
            print("SYNTAX ERROR: Expected '(' after 'case' in line " + str(lex.current_line) +
                  " but " + token.recognized_string + " appeared.")

        elif error_code == "WHILESTAT_(":
            print("SYNTAX ERROR: Expected '(' after 'while' in line " + str(lex.current_line) +
                  " but " + token.recognized_string + " appeared.")

        elif error_code == "IFSTAT_(":
            print("SYNTAX ERROR: Expected '(' after 'if' in line " + str(lex.current_line) +
                  " but " + token.recognized_string + " appeared.")

        elif error_code == "STATEMENTS_}":
            print("SYNTAX ERROR: Expected '}' in line " + str(lex.current_line) +
                  ".\nMore than one statements should be grouped with brackets.")

        elif error_code == "STATEMENTS_;":
            print("SYNTAX ERROR: Expected ';' in line " + str(lex.current_line) +
                  " but " + token.recognized_string + " appeared." + 
                  "\nAll statements should end with a ';'")

        elif error_code == "declaration":
            print("SYNTAX ERROR: Expected ';' in line " + str(lex.current_line) +
                  " but " + token.recognized_string + " appeared." + 
                  "\nAll declarations should end with a ';'")

        elif error_code == "NO_EOF":
            print("SYNTAX ERROR: No characters are allowed after the fullstop indicating the end of the program.")

        elif error_code == "NO_DOT":
            print("SYNTAX ERROR: Every program should end with a fullstop, fullstop at the end is missing.")
        
        elif error_code == "PROGRAM_NAME":
            print("SYNTAX ERROR: The name of the program expected after the keyword 'program' in line" + 
                    str(lex.current_line) + " . The illegal program name '" + token.recognized_string + "' appeared.")
        
        elif error_code == "BLOCK_}":
            print("SYNTAX ERROR: Expected '}' at the end of the block in line: " + str(lex.current_line))

        elif error_code == "BLOCK_{":
            print("SYNTAX ERROR: Expected '{' at the beginning of the block in line: " + str(lex.current_line))

        elif error_code == "BOOLFACTOR_]":
            print("SYNTAX ERROR: Expected ']' at the end of boolean expression in line: " + str(lex.current_line))

        elif error_code == "BOOLFACTOR_[":
            print("SYNTAX ERROR: Expected '[' at the beginning of boolean expression in line: " + str(lex.current_line))

        sys.exit(1)

    def __program(self):
        global token

        if token.recognized_string == "program":
            token = self.__get_token()
            if token.family == "identifier":
                token = self.__get_token()
                self.__block()
                if token.recognized_string == ".":
                    token = self.__get_token()
                    if token.recognized_string == "eof": 
                        token = self.__get_token()
                    else:
                        self.__error("NO_EOF")
                else:
                    self.__error("NO_DOT")
            else:
                self.__error("PROGRAM_NAME")  
        else:
            self.__error("KEYWORD PROGRAM NOT FOUND")

    def __block(self):
        global token
        if token.recognized_string == "{":
            token = self.__get_token()
            self.__declarations()
            self.__subprograms()
            self.__blockstatements()
            if token.recognized_string == "}":
                token = self.__get_token()
            else:
                self.__error("BLOCK_}")  
        else:
            self.__error("BLOCK_{")  

    def __declarations(self):
        global token
        while token.recognized_string == "declare":
            token = self.__get_token()
            self.__varlist()
            if token.recognized_string == ";":
                token = self.__get_token()
            else:
                self.__error("declaration")

    def __varlist(self):
        global token
        if token.recognized_string[0].isalpha():
            self.__idvalue()
            while token.recognized_string == ",":
                token = self.__get_token()
                self.__idvalue()

    def __subprograms(self):
        global token
        while token.recognized_string == "function" or \
                token.recognized_string == "procedure":
            self.__subprogram()

    def __subprogram(self):
        global token
        if token.recognized_string == "function" or \
                token.recognized_string == "procedure":
            token = self.__get_token()
            self.__idvalue()
            if token.recognized_string == "(":
                token = self.__get_token()
                self.__formalparlist()
                if token.recognized_string == ")":
                    token = self.__get_token()
                    self.__block()
                else:
                    self.__error("subprogram")

            else:
                self.__error("subprogram")

    def __formalparlist(self):
        global token
        self.__formalparitem()
        while token.recognized_string == ",":
            token = self.__get_token()
            self.__formalparitem()

    def __formalparitem(self):
        global token
        if token.recognized_string == "in":
            token = self.__get_token()
            self.__idvalue()
        elif token.recognized_string == "inout":
            token = self.__get_token()
            self.__idvalue()

    def __statements(self):
        global token
        if token.recognized_string == "{":
            token = self.__get_token()
            self.__statement()
            while token.recognized_string == ";":
                token = self.__get_token()
                self.__statement()
            if token.recognized_string == "}":
                token = self.__get_token()
            else:
                self.__error("STATEMENTS_}")
        else:
            self.__statement()
            if not token.recognized_string == ";":
                self.__error("STATEMENTS_;")
            token = self.__get_token()

    def __blockstatements(self):
        global token
        self.__statement()

        while token.recognized_string == ";":
            token = self.__get_token()
            self.__statement()

    def __ifStat(self):
        global token
        token = self.__get_token()
        if token.recognized_string == "(":
            token = self.__get_token()
            self.__condition()
            if token.recognized_string == ")":
                token = self.__get_token()
                self.__statements()
            else:
                self.__error("IFSTAT_)")
            self.__elsepart()
        else:
            self.__error("IFSTAT_(")

    def __elsepart(self):
        global token
        if token.recognized_string == "else":
            token = self.__get_token()
            self.__statements()

    def __statement(self):
        global token
        if token.recognized_string == "if":
            self.__ifStat()
        elif token.recognized_string == "while":
            self.__whileStat()
        elif token.recognized_string == "switchcase":
            self.__switchcaseStat()
        elif token.recognized_string == "forcase":
            self.__forcaseStat()
        elif token.recognized_string == "incase":
            self.__incaseStat()
        elif token.recognized_string == "call":
            self.__callStat()
        elif token.recognized_string == "return":
            self.__returnStat()
        elif token.recognized_string == "input":
            self.__inputStat()
        elif token.recognized_string == "print":
            self.__printStat()
        elif token.recognized_string[0].isalpha() and \
             token.recognized_string != "eof" and \
             not token.recognized_string in group_keyword_list:
            self.__assignStat()

    def __assignStat(self):
        global token
        self.__idvalue()
        if token.recognized_string == ":=":
            token = self.__get_token()
            self.__expression()
        else:
            self.__error("assignStat")

    def __whileStat(self):
        global token
        token = self.__get_token()
        if token.recognized_string == "(":
            token = self.__get_token()
            self.__condition()
            if token.recognized_string == ")":
                token = self.__get_token()
                self.__statements()
            else:
                self.__error("WHILESTAT_)")
        else:
            self.__error("WHILESTAT_(")

    def __switchcaseStat(self):
        global token
        token = self.__get_token()
        while token.recognized_string == "case":
            if token.recognized_string == "(":
                token = self.__get_token()
                self.__condition()
                if token.recognized_string == ")":
                    token = self.__get_token()
                    self.__statements()
                else:
                    self.__error("SWITCHCASESTAT_)")
            else:
                self.__error("SWITCHCASESTAT_(")
        if token.recognized_string == "default":
            token = self.__get_token()
            self.__statements()
        else:
            self.__error("SWITCHCASESTAT_DEFAULT")

    def __forcaseStat(self):
        global token
        token = self.__get_token()
        while token.recognized_string == "case":
            token = self.__get_token()
            if token.recognized_string == "(":
                token = self.__get_token()
                self.__condition()
                if token.recognized_string == ")":
                    token = self.__get_token()
                    self.__statements()
                else:
                    self.__error("FORSTAT_)")
            else:
                self.__error("FORSTAT_(")
        if token.recognized_string == "default":
            token = self.__get_token()
            self.__statements()
        else:
            self.__error("FORSTAT_DEFAULT")

    def __incaseStat(self):
        global token
        token = self.__get_token()
        while token.recognized_string == "case":
            token = self.__get_token()
            if token.recognized_string == "(":
                token = self.__get_token()
                self.__condition()
                if token.recognized_string == ")":
                    token = self.__get_token()
                    self.__statements()
                else:
                    self.__error("incaseStat")

            else:
                self.__error("incaseStat")

    def __returnStat(self):
        global token
        token = self.__get_token()
        if token.recognized_string == "(":
            token = self.__get_token()
            self.__expression()
            if not token.recognized_string == ")":
                self.__error("returnStat")
            token = self.__get_token()
        else:
            self.__error("returnStat")

    def __callStat(self):
        global token
        token = self.__get_token()
        self.__idvalue()
        if token.recognized_string == "(":
            token = self.__get_token()
            self.__actualparlist()
            if not token.recognized_string == ")":
                self.__error("callStat")
            token = self.__get_token()
        else:
            self.__error("callStat")

    def __printStat(self):
        global token
        token = self.__get_token()
        if token.recognized_string == "(":
            token = self.__get_token()
            self.__expression()
            if not token.recognized_string == ")":
                self.__error("printStat")
            token = self.__get_token()
        else:
            self.__error("printStat")

    def __inputStat(self):
        global token
        token = self.__get_token()
        if token.recognized_string == "(":
            token = self.__get_token()
            self.__idvalue()
            if not token.recognized_string == ")":
                self.__error("inputStat")
            token = self.__get_token()
        else:
            self.__error("inputStat")

    def __actualparlist(self):
        global token
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

    def __condition(self):
        global token
        self.__boolterm()
        while token.recognized_string == "or":
            self.__get_token()
            self.__boolfactor()

    def __boolterm(self):
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
                self.__condition()
                if not token.recognized_string == "]":
                    self.__error("BOOLFACTOR_]")  
                token = self.__get_token()
            else:
                self.__error("BOOLFACTOR_[")
        elif token.recognized_string == "[":
            token = self.__get_token()
            self.__condition()
            if not token.recognized_string == "]":
                self.__error("BOOLFACTOR_]") 
            token = self.__get_token()
        else:
            self.__expression()
            self.__reloperator()
            self.__expression()

    def __expression(self):
        global token
        self.__optionalSign()
        self.__term()
        while token.recognized_string == "+" or \
                token.recognized_string == "-":
            self.__addoperator()
            self.__term()

    def __term(self):
        global token
        self.__factor()
        while token.recognized_string == "*" or \
                token.recognized_string == "/":
            self.__muloperator()
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
            token = self.__get_token()
        elif token.recognized_string[0].isalpha():
            self.__idvalue()
            self.__idtail()

    def __idtail(self):
        global token
        if token.recognized_string == "(":
            token = self.__get_token()
            self.__actualparlist()
            if not token.recognized_string == ")":
                self.__error("IDTAIL")
            token = self.__get_token()

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

        for i in range(1, len(token.recognized_string) - 1):
            if not token.recognized_string[i].isalpha() and \
                    not token.recognized_string[i].isnumeric():
                self.__error("NOT ID")
        token = self.__get_token()


def main():
    if (len(sys.argv) != 2):
        sys.exit("ERROR: Usage $python met.py <inputfile>")
    
    print(sys.argv[1].split("."))
    #if (sys.argv[1].split(".")[2] != "ci"):
    #    sys.exit("ERROR: Compiler accepts only '.ci' files")

    token1 = Token(None, None, 1)
    lex_object = Lex(1, sys.argv[1], None)
    parser_obj = Parser(lex_object)

    parser_obj.syntax_analyzer()

    # fp = 0
    # while True:
    #     fp, token = lex_object.next_token(fp)
    #     if token.recognized_string == "eof":
    #          break


if __name__ == "__main__":
    main()
