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
program_name = ""
quad_number = 1
temp_var_number = 0
quad_list = []

scope_list = []
global_nesting_level = 0


def reset_global_variables():  # Resets global variables for testing
    global program_name, quad_number, temp_var_number
    program_name = ""
    quad_number = 1
    temp_var_number = 0
    quad_list.clear()


class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

    def __str__(self):
        return self.recognized_string + ", family: \"" + \
               self.family + "\", line: " + str(self.line_number)


token = Token(None, None, 1)


class Lex:
    bool = True
    file = None

    def __init__(self, current_line, file_name, token):
        self.current_line = current_line
        self.file_name = file_name
        self.token = token

        self.file = open(self.file_name, "r")

    def get_file(self):
        return self.file

    def __error(self, family, character):
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
        while True:
            if character.isnumeric():
                recognized_string = recognized_string + character
            elif character.isalpha():
                self.__error("number", character)
            else:
                if -(pow(2, 32) - 1) <= int(recognized_string) <= (pow(2, 32) - 1):
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
        first_character = first_char
        second_character = self.file.read(1)
        recognized_string = first_character + second_character
        if recognized_string == ":=":
            return recognized_string, "assignment"
        else:
            character = first_character + second_character
            self.__error("assignment", character)

    def __is_rel_operator(self, first_char):
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
        if character == "+" or character == "-":
            return character, "addOperator"
        elif character == "*" or character == "/":
            return character, "mulOperator"
        elif character in group_symbol_list:
            return character, "groupSymbol"
        elif character in delimeter_list:
            return character, "delimeter"

    def __clear_blank_char(self, character):
        while True:
            if not character.isspace():
                return character
            elif character == "\n":
                self.current_line = self.current_line + 1
                character = self.file.read(1)
            else:
                character = self.file.read(1)

    def __is_comment(self):
        character = self.file.read(1)
        while character != "#":
            character = self.file.read(1)
            if not character:
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
                first_char = self.__is_comment()
            else:
                first_char = self.__clear_blank_char(first_char)

        if not bool:
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
        self.file_pointer, next_token = lex.next_token(self.file_pointer)
        return next_token

    def syntax_analyzer(self):
        global token
        token = self.__get_token()
        self.__program()
        self.lexical_analyzer.get_file().close()
        print("Compilation successfully completed")

        # For testing only
        # print(f"{token.recognized_string:12} family: {token.family:12} line: {token.line_number:3}")
        return token

    def __error(self, error_code):

        error_codes = ["IDTAIL", "FACTOR1", "inputStat", "printStat", "callStat", "returnStat",
                       "incaseStat", "FORSTAT_)", "SWITCHCASESTAT_)", "WHILESTAT_)", "IFSTAT_)", "subprogram"]

        case_stat = ["FORSTAT_(", "SWITCHCASESTAT_("]

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
        global program_name

        if token.recognized_string == "program":
            token = self.__get_token()
            if token.family == "identifier":
                program_name = token.recognized_string
                token = self.__get_token()
                self.__block(program_name)
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

    def __block(self, block_name):
        global token
        if token.recognized_string == "{":
            add_scope(global_nesting_level)
            print_scope_list()
            token = self.__get_token()
            self.__declarations()
            self.__subprograms()
            gen_quad("begin_block", block_name, "_", "_")
            self.__blockstatements()
            if block_name == program_name:
                gen_quad("halt", "_", "_", "_")
            gen_quad("end_block", block_name, "_", "_")
            if token.recognized_string == "}":
                delete_scope()
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
            value = self.__idvalue()
            add_entity(Variable(value, "Variable", 0))
            while token.recognized_string == ",":
                token = self.__get_token()
                value = self.__idvalue()
                add_entity(Variable(value, "Variable", 0))

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
            block_name = self.__idvalue()
            if token.recognized_string == "(":
                token = self.__get_token()
                self.__formalparlist()
                if token.recognized_string == ")":
                    token = self.__get_token()
                    self.__block(block_name)
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

    def __if_stat(self):
        global token
        if_list = []
        token = self.__get_token()
        if token.recognized_string == "(":
            token = self.__get_token()
            cond_true, cond_false = self.__condition()
            if token.recognized_string == ")":
                token = self.__get_token()
                backpatch(cond_true, next_quad())
                self.__statements()
                if_list = make_list(next_quad())
                gen_quad("jump", "_", "_", "_")
                backpatch(cond_false, next_quad())
            else:
                self.__error("IFSTAT_)")
            self.__elsepart()
            backpatch(if_list, next_quad())
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
            self.__if_stat()
        elif token.recognized_string == "while":
            self.__while_stat()
        elif token.recognized_string == "switchcase":
            self.__switchcase_stat()
        elif token.recognized_string == "forcase":
            self.__forcase_stat()
        elif token.recognized_string == "incase":
            self.__incase_stat()
        elif token.recognized_string == "call":
            self.__call_stat()
        elif token.recognized_string == "return":
            self.__return_stat()
        elif token.recognized_string == "input":
            self.__input_stat()
        elif token.recognized_string == "print":
            self.__print_stat()
        elif token.recognized_string[0].isalpha() and \
                token.recognized_string != "eof" and \
                token.recognized_string not in group_keyword_list:
            self.__assign_stat()

    def __assign_stat(self):
        global token
        id_value = self.__idvalue()
        if token.recognized_string == ":=":
            token = self.__get_token()
            term = self.__expression()
            gen_quad(":=", term, "_", id_value)
        else:
            self.__error("assignStat")

    def __while_stat(self):
        global token
        token = self.__get_token()
        cond_quad = next_quad()
        if token.recognized_string == "(":
            token = self.__get_token()
            cond_true, cond_false = self.__condition()
            if token.recognized_string == ")":
                token = self.__get_token()
                backpatch(cond_true, next_quad())
                self.__statements()
                gen_quad("jump", "_", "_", cond_quad)
                backpatch(cond_false, next_quad())
            else:
                self.__error("WHILESTAT_)")
        else:
            self.__error("WHILESTAT_(")

    def __switchcase_stat(self):
        global token
        exit_list = empty_list()
        token = self.__get_token()
        while token.recognized_string == "case":
            token = self.__get_token()
            if token.recognized_string == "(":
                token = self.__get_token()
                cond_true, cond_false = self.__condition()
                if token.recognized_string == ")":
                    backpatch(cond_true, next_quad())
                    token = self.__get_token()
                    self.__statements()
                    t = make_list(next_quad())
                    gen_quad("jump", "_", "_", "_")
                    exit_list = merge_list(exit_list, t)
                    backpatch(cond_false, next_quad())
                else:
                    self.__error("SWITCHCASESTAT_)")
            else:
                self.__error("SWITCHCASESTAT_(")
        if token.recognized_string == "default":
            token = self.__get_token()
            self.__statements()
            backpatch(exit_list, next_quad())
        else:
            self.__error("SWITCHCASESTAT_DEFAULT")

    def __forcase_stat(self):
        global token
        first_cond_quad = next_quad()
        token = self.__get_token()
        while token.recognized_string == "case":
            token = self.__get_token()
            if token.recognized_string == "(":
                token = self.__get_token()
                cond_true, cond_false = self.__condition()
                if token.recognized_string == ")":
                    token = self.__get_token()
                    backpatch(cond_true, next_quad())
                    self.__statements()
                    gen_quad("jump", "_", "_", str(first_cond_quad))
                    backpatch(cond_false, next_quad())
                else:
                    self.__error("FORSTAT_)")
            else:
                self.__error("FORSTAT_(")
        if token.recognized_string == "default":
            token = self.__get_token()
            self.__statements()
        else:
            self.__error("FORSTAT_DEFAULT")

    def __incase_stat(self):
        global token
        flag = new_temp()
        first_cond_quad = next_quad()
        gen_quad(":=", "0", "_", flag)
        token = self.__get_token()
        while token.recognized_string == "case":
            token = self.__get_token()
            if token.recognized_string == "(":
                token = self.__get_token()
                cond_true, cond_false = self.__condition()
                if token.recognized_string == ")":
                    token = self.__get_token()
                    backpatch(cond_true, next_quad())
                    self.__statements()
                    gen_quad(":=", "1", "_", flag)
                    backpatch(cond_false, next_quad())
                else:
                    self.__error("incaseStat")

            else:
                self.__error("incaseStat")
        gen_quad("=", flag, "1", first_cond_quad)

    def __return_stat(self):
        global token
        token = self.__get_token()
        if token.recognized_string == "(":
            token = self.__get_token()
            term = self.__expression()
            gen_quad("RET", term, "_", "_")
            if not token.recognized_string == ")":
                self.__error("returnStat")
            token = self.__get_token()
        else:
            self.__error("returnStat")

    def __call_stat(self):
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

    def __print_stat(self):
        global token
        token = self.__get_token()
        if token.recognized_string == "(":
            token = self.__get_token()
            term = self.__expression()
            gen_quad("out", term, "_", "_")
            if not token.recognized_string == ")":
                self.__error("printStat")
            token = self.__get_token()
        else:
            self.__error("printStat")

    def __input_stat(self):
        global token
        token = self.__get_token()
        if token.recognized_string == "(":
            token = self.__get_token()
            value = self.__idvalue()
            gen_quad("in", value, "_", "_")
            if not token.recognized_string == ")":
                self.__error("inputStat")
            token = self.__get_token()
        else:
            self.__error("inputStat")

    def __actualparlist(self):
        global token
        par_list = []
        par_item = self.__actualparitem()
        par_list.append(par_item)
        while token.recognized_string == ",":
            token = self.__get_token()
            par_item = self.__actualparitem()
            par_list.append(par_item)
        return par_list

    def __actualparitem(self):
        global token
        if token.recognized_string == "in":
            token = self.__get_token()
            return self.__expression(), "CV"
        elif token.recognized_string == "inout":
            token = self.__get_token()
            return self.__idvalue(), "REF"

    def __condition(self):
        global token
        b_true, b_false = self.__boolterm()
        while token.recognized_string == "or":
            token = self.__get_token()
            backpatch(b_false, next_quad())
            q2_true, q2_false = self.__boolterm()
            b_true = merge_list(b_true, q2_true)
            b_false = q2_false
        return b_true, b_false

    def __boolterm(self):
        global token
        q_true, q_false = self.__boolfactor()
        while token.recognized_string == "and":
            token = self.__get_token()
            backpatch(q_true, next_quad())
            r2_true, r2_false = self.__boolfactor()
            q_false = merge_list(q_false, r2_false)
            q_true = r2_true
        return q_true, q_false

    def __boolfactor(self):
        global token
        r_true = []
        r_false = []
        if token.recognized_string == "not":
            token = self.__get_token()
            if token.recognized_string == "[":
                token = self.__get_token()
                r_false, r_true = self.__condition()
                if not token.recognized_string == "]":
                    self.__error("BOOLFACTOR_]")
                token = self.__get_token()
            else:
                self.__error("BOOLFACTOR_[")
        elif token.recognized_string == "[":
            token = self.__get_token()
            r_true, r_false = self.__condition()
            if not token.recognized_string == "]":
                self.__error("BOOLFACTOR_]")
            token = self.__get_token()
        else:
            term1 = self.__expression()
            operator = self.__reloperator()
            term2 = self.__expression()
            r_true = make_list(next_quad())
            gen_quad(operator, term1, term2, "_")
            r_false = make_list(next_quad())
            gen_quad("jump", "_", "_", "_")
        return r_true, r_false

    def __expression(self):
        global token
        sign = self.__optional_sign()
        term_1 = self.__term()
        if sign is not None:
            temp_var = new_temp()
            gen_quad(sign, term_1, "0", temp_var)
            term_1 = temp_var
        while token.recognized_string == "+" or \
                token.recognized_string == "-":
            operator = self.__addoperator()
            term_2 = self.__term()
            temp_var = new_temp()
            gen_quad(operator, term_1, term_2, temp_var)
            term_1 = temp_var
        return term_1

    def __term(self):
        global token
        factor_1 = self.__factor()
        while token.recognized_string == "*" or \
                token.recognized_string == "/":
            operator = self.__muloperator()
            factor_2 = self.__factor()
            temp_var = new_temp()
            gen_quad(operator, factor_1, factor_2, temp_var)
            factor_1 = temp_var
        return factor_1

    def __factor(self):
        global token
        if token.recognized_string.isnumeric():
            return self.__integervalue()
        elif token.recognized_string == "(":
            token = self.__get_token()
            term = self.__expression()
            if not token.recognized_string == ")":
                self.__error("FACTOR1")
            token = self.__get_token()
            return term
        elif token.recognized_string[0].isalpha():
            id_value = self.__idvalue()
            function_ret_val = self.__idtail(id_value)
            if function_ret_val is None:
                return id_value
            else:
                return function_ret_val

    def __idtail(self, function_id):
        global token
        if token.recognized_string == "(":
            token = self.__get_token()
            par_list = self.__actualparlist()

            for par in par_list:
                gen_quad("par", par[0], par[1], "_")
            temp_var = new_temp()
            gen_quad("par", temp_var, "RET", "_")
            gen_quad("call", function_id, "_", "_")

            if not token.recognized_string == ")":
                self.__error("IDTAIL")
            token = self.__get_token()
            return temp_var

    def __optional_sign(self):
        global token
        if token.recognized_string == "+" or \
                token.recognized_string == "-":
            return self.__addoperator()

    def __reloperator(self):
        global token
        operator = token.recognized_string
        rel_op_list = ["=", "<=", ">=", ">", "<", "<>"]
        if operator not in rel_op_list:
            self.__error("EXPECTED REL_OP")
        token = self.__get_token()
        return operator

    def __addoperator(self):
        global token
        operator = token.recognized_string
        if not operator == "+" and not operator == "-":
            self.__error("EXPECTED ADD_OP")
        token = self.__get_token()
        return operator

    def __muloperator(self):
        global token
        operator = token.recognized_string
        if not operator == "*" and not operator == "/":
            self.__error("EXPECTED MUL_OP")
        token = self.__get_token()
        return operator

    def __integervalue(self):
        global token
        value = token.recognized_string
        for i in range(len(value)):
            if not value[i].isnumeric():
                self.__error("NOT AN INTEGER")
        token = self.__get_token()
        return value

    def __idvalue(self):
        global token
        value = token.recognized_string
        if not value[0].isalpha():
            self.__error("NOT ID")

        for i in range(1, len(value) - 1):
            if not value[i].isalpha() and \
                    not value[i].isnumeric():
                self.__error("NOT ID")
        token = self.__get_token()
        return value


class Quad:
    def __init__(self, quad_label, operator, operand1, operand2, operand3):
        self.quad_label = quad_label
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3

    def __str__(self):
        return str(self.quad_label) + ": " + str(self.operator) + " " \
               + str(self.operand1) + " " + str(self.operand2) + " " + str(self.operand3)

    def set_operand3(self, operand):
        self.operand3 = operand


class Entity:
    def __init__(self, name, type_of_entity):
        self.name = name
        self.type_of_entity = type_of_entity

    def __str__(self):
        return f"{self.name}: {self.type_of_entity}"


class Variable(Entity):
    def __init__(self, name, type_of_var, offset):
        super().__init__(name, type_of_var)
        self.offset = offset

    def __str__(self):
        return f"{self.name}: {self.type_of_entity} {self.offset}"


class Function(Entity):
    def __init__(self, name, type_of_func, start_quad, list_argument, frame_length):
        super().__init__(name, type_of_func)
        self.start_quad = start_quad
        self.list_argument = list_argument
        self.frame_length = frame_length


class Constant(Entity):
    def __init__(self, name, value):
        super().__init__(name, "Constant")
        self.value = value


class Parameter(Entity):
    def __init__(self, name, par_mode, offset):
        super().__init__(name, "Parameter")
        self.par_mode = par_mode
        self.offset = offset


class TempVariable(Entity):
    def __init__(self, name, offset):
        super().__init__(name, "TempVariable")
        self.offset = offset


class Scope:
    def __init__(self, entity_list, nesting_level):
        self.entity_list = entity_list
        self.nesting_level = nesting_level

    def __str__(self):
        return f"{str(self.nesting_level)}:[{str(len(self.entity_list))}]"

    def add_entity(self, entity):
        self.entity_list.append(entity)


class Argument:
    def __init__(self, par_mode, type_of_arg):
        self.par_mode = par_mode
        self.type_of_arg = type_of_arg


def gen_quad(operator, operand1, operand2, operand3):
    global quad_number
    label = next_quad()
    quad_number = quad_number + 1
    new_quad = Quad(label, operator, operand1, operand2, operand3)
    quad_list.append(new_quad)
    return new_quad


def next_quad():
    return quad_number


def new_temp():
    global temp_var_number
    new_temp_variable = "T_" + str(temp_var_number)
    temp_var_number = temp_var_number + 1
    return new_temp_variable


def empty_list():
    return []


def make_list(label):
    return [label]


def merge_list(list1, list2):
    return list1 + list2


def backpatch(list, label):
    for i in list:
        quad_list[i-1].set_operand3(label)
    list.clear()


def print_quads():
    print("---------| QUADS |---------")
    for quad in quad_list:
        print(quad.__str__())


def add_scope(nesting_level):
    global global_nesting_level
    scope = Scope([], nesting_level)
    global_nesting_level = global_nesting_level + 1
    scope_list.append(scope)


def delete_scope():
    global global_nesting_level
    global_nesting_level = global_nesting_level - 1
    del scope_list[len(scope_list)-1]


def print_scope_list():
    print("---------| SCOPE LIST |---------")
    for scope in scope_list:
        print(scope.__str__())
        for entity in scope.entity_list:
            print(entity.__str__())


def add_entity(entity):
    scope_list[len(scope_list)-1].add_entity(entity)


def main():
    if len(sys.argv) != 2:
        sys.exit("ERROR: Usage $python met.py <inputfile>")

    # print(sys.argv[1].split("."))
    # if (sys.argv[1].split(".")[2] != "ci"):
    #    sys.exit("ERROR: Compiler accepts only '.ci' files")

    # ------------------------------- Phase 1 main
    lex_object = Lex(1, sys.argv[1], None)
    parser_obj = Parser(lex_object)

    parser_obj.syntax_analyzer()

    print_quads()
    print_scope_list()

    # -------------------------------

    # fp = 0
    # while True:
    #     fp, token = lex_object.next_token(fp)
    #     if token.recognized_string == "eof":
    #          break


if __name__ == "__main__":
    main()
