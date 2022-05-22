# Dimitropoulos Dimitrios, 4352, cse84352
# Poulos Grigorios, 4480, cse84480

import os
import sys

PRINT_SCOPE_LIST = False
GENERATE_RISCV_CODE = True
DEFAULT_VARIABLE_OFFSET = 12
FILE_NAME = ""

group_symbol_list = ["{", "}", "(", ")", "[", "]"]
delimiter_list = [",", ";", "."]
operator_list = ["+", "-", "*", "/"]
rel_op_list = ["=", "<=", ">=", ">", "<", "<>"]

group_keyword_list = ["print", "program", "if", "switchcase", "not", "function",
                      "input", "declare", "else", "forcase", "and", "procedure",
                      "while", "incase", "or", "call", "case", "default",
                      "return", "in", "inout"]
end_reached = True
program_name = ""
quad_number = 1
temp_var_number = 0
quad_list = []

# Symbol Table variables
scope_list = []
global_nesting_level = 0
variable_offset = DEFAULT_VARIABLE_OFFSET
current_scope_functions = []
sb_file_str = ""

# Final code
final_code_list = ["L0:", "b Lmain"]
number_of_params = 0
first_parameter = True
num_flag = 1
jump_label_num = 0


def reset_global_variables():  # Resets global variables for testing
    global program_name, quad_number, temp_var_number, FILE_NAME, sb_file_str
    FILE_NAME = ""
    program_name = ""
    quad_number = 1
    temp_var_number = 0
    quad_list.clear()
    sb_file_str = ""


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
    end_reached = True
    file = None

    def __init__(self, current_line, file_name, first_token):
        global FILE_NAME
        self.current_line = current_line
        self.file_name = file_name
        self.token = first_token

        FILE_NAME = file_name.split("\\")[-1].split(".")[0]
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
        global end_reached
        recognized_string = ""
        while True:
            if character.isnumeric():
                recognized_string = recognized_string + character
            elif character.isalpha():
                self.__error("number", character)
            else:
                if -(pow(2, 32) - 1) <= int(recognized_string) <= (pow(2, 32) - 1):
                    if character == "":
                        end_reached = False
                    self.file.seek(self.file.tell() - 1)
                    return recognized_string, "number"
                else:
                    self.__error("number", character)
            character = self.file.read(1)

    def __is_keyword(self, first_char):
        global end_reached
        recognized_string = first_char
        while True:
            character = self.file.read(1)
            if not character.isnumeric() and not character.isalpha():
                if len(recognized_string) <= 30:
                    if character == "":
                        end_reached = False
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
        elif character in delimiter_list:
            return character, "delimiter"

    def __clear_blank_char(self, character):
        while True:
            if not character.isspace():
                return character
            elif character == "\n":
                self.current_line = self.current_line + 1

                # For every line o f the program print scope list
                if PRINT_SCOPE_LIST:
                    print_scope_list()

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

        if not end_reached:
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
        elif first_char in group_symbol_list or first_char in delimiter_list or first_char in operator_list:
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
        global token, program_name

        if token.recognized_string == "program":
            token = self.__get_token()
            if token.family == "identifier":
                program_name = token.recognized_string
                add_scope()
                token = self.__get_token()
                self.__block(program_name)

                if PRINT_SCOPE_LIST:
                    print_scope_list()
                save_symbol_table()
                delete_scope()
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
        global token, first_parameter
        if token.recognized_string == "{":
            token = self.__get_token()
            self.__declarations()
            self.__subprograms()

            gen_quad("begin_block", block_name, "_", "_")
            if block_name != program_name:
                current_scope_functions[-1].start_quad = quad_number
            block_start_quad = quad_number

            self.__blockstatements()

            if block_name == program_name:
                gen_quad("halt", "_", "_", "_")
            gen_quad("end_block", block_name, "_", "_")
            if token.recognized_string == "}":
                token = self.__get_token()
            else:
                self.__error("BLOCK_}")
        else:
            self.__error("BLOCK_{")
        # Generate Risc-V code

        if GENERATE_RISCV_CODE:
            first_parameter = True
            # print(f"_________{str(block_start_quad-1)}__{str(block_name)}__________")
            if block_name == program_name:
                riscv_write(f"Lmain:")

            for quad in quad_list[block_start_quad-2:]:
                # print(quad)
                generate_riscv(quad, block_name)

            # print("\n---------RISCV---------")
            # print_riscv_commands()

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
            add_entity(Variable(value, "Variable", scope_list[-1].variable_offset))
            while token.recognized_string == ",":
                token = self.__get_token()
                value = self.__idvalue()
                add_entity(Variable(value, "Variable", scope_list[-1].variable_offset))

    def __subprograms(self):
        global token
        while token.recognized_string == "function" or \
                token.recognized_string == "procedure":
            self.__subprogram()

    def __subprogram(self):
        global token, current_scope_functions
        type_of_subprogram = token.recognized_string
        if type_of_subprogram == "function" or type_of_subprogram == "procedure":
            token = self.__get_token()
            block_name = self.__idvalue()

            func = Function(block_name, type_of_subprogram, None, None, None)
            current_scope_functions.append(func)
            add_entity(func)
            add_scope()

            if token.recognized_string == "(":
                token = self.__get_token()
                self.__formalparlist()
                if token.recognized_string == ")":
                    token = self.__get_token()
                    self.__block(block_name)

                    current_scope_functions[-1].frame_length = scope_list[-1].variable_offset  # TODO: How to calculate
                    current_scope_functions = current_scope_functions[:-1]
                    save_symbol_table()
                    delete_scope()
                else:
                    self.__error("subprogram")

            else:
                self.__error("subprogram")

    def __formalparlist(self):
        global token, current_scope_functions
        argument_list = []
        argument = self.__formalparitem()
        if argument is not None:
            argument_list.append(argument)
        while token.recognized_string == ",":
            token = self.__get_token()
            argument = self.__formalparitem()
            argument_list.append(argument)
        current_scope_functions[-1].argument_list = argument_list

    def __formalparitem(self):
        global token
        par_mode = -1
        par_name = -1
        argument = None
        arg_mode = token.recognized_string
        if token.recognized_string == "in":
            token = self.__get_token()
            par_name = self.__idvalue()
            par_mode = "cv"
        elif token.recognized_string == "inout":
            token = self.__get_token()
            par_name = self.__idvalue()
            par_mode = "ref"

        if arg_mode != ")":
            parameter = Parameter(par_name, par_mode, scope_list[-1].variable_offset)
            argument = Argument(arg_mode, "int")
            add_entity(parameter)
        return argument

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
        function_id = self.__idvalue()
        print("AAAAAAAAAAAAAAAAAAAAAA" + function_id)
        if token.recognized_string == "(":
            token = self.__get_token()
            par_list = self.__actualparlist()
            if par_list != [None]:
                for par in par_list:
                    gen_quad("par", par[0], par[1], "_")
                temp_var = new_temp()
            gen_quad("call", function_id, "_", "_")

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
            term = self.__expression()
            return term, "CV"
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
        return f"{self.name}/{self.offset}"


class Function(Entity):
    def __init__(self, name, type_of_func, start_quad, argument_list, frame_length):
        super().__init__(name, type_of_func)
        self.start_quad = start_quad
        self.argument_list = argument_list
        self.frame_length = frame_length

    def __str__(self):
        argument_list_str = ""
        if self.argument_list is not empty_list():
            for argument in self.argument_list:
                argument_list_str = argument_list_str + " " + argument.par_mode
        return f"{self.name}/{self.start_quad}/{self.frame_length}[{argument_list_str.strip()}]"


class Parameter(Entity):
    def __init__(self, name, par_mode, offset):
        super().__init__(name, "Parameter")
        self.par_mode = par_mode
        self.offset = offset

    def __str__(self):
        return f"{self.name}/{self.par_mode}/{self.offset}"


class TempVariable(Entity):
    def __init__(self, name, offset):
        super().__init__(name, "TempVariable")
        self.offset = offset

    def __str__(self):
        return f"{self.name}/{self.offset}"


class Scope:
    def __init__(self, entity_list, nesting_level):
        self.entity_list = entity_list
        self.nesting_level = nesting_level
        self.variable_offset = DEFAULT_VARIABLE_OFFSET

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
    add_entity(TempVariable(new_temp_variable, scope_list[-1].variable_offset))
    return new_temp_variable


def empty_list():
    return []


def make_list(label):
    return [label]


def merge_list(list1, list2):
    return list1 + list2


def backpatch(unpatched_list, label):
    for i in unpatched_list:
        quad_list[i-1].set_operand3(label)
    unpatched_list.clear()


def print_quads():
    print("---------| QUADS |---------")
    for quad in quad_list:
        print(quad)


def convert_int():
    int_file_name = FILE_NAME + ".int"
    if os.path.exists(int_file_name):
        os.remove(int_file_name)
    f_int = open(int_file_name, "a")
    for quad in quad_list:
        f_int.write(quad.__str__() + "\n")
    f_int.close()


def convert_c():
    function_vars = ["par", "cv", "ref", "ret", "call"]
    flag = 1

    for quad in quad_list:
        if str(quad.operator).lower() in function_vars:
            flag = 0

    if flag == 1:
        c_default = "#include <stdio.h> \n\nint main() \n{"
        c_file_name = FILE_NAME + ".c"
        if os.path.exists(c_file_name):
            os.remove(c_file_name)

        f_c = open(c_file_name, "a")
        f_c.write(c_default)

        var = []

        for quad in quad_list:
            if str(quad.operator) == ":=" or str(quad.operator) in operator_list or str(quad.operator) in rel_op_list or str(quad.operator) == "in":
                if not str(quad.operand1).isnumeric() and not str(quad.operand1) == "_":
                    var.append(str(quad.operand1))

                if not str(quad.operand2).isnumeric() and not str(quad.operand2) == "_":
                    var.append(str(quad.operand2))

                if not str(quad.operand3).isnumeric() and not str(quad.operand3) == "_":
                    var.append(str(quad.operand3))

        var = list(dict.fromkeys(var))

        f_c.write("\nint ")
        for elements in range(len(var)):
            if elements != len(var)-1:
                f_c.write(var[elements] + ",")
            else:
                f_c.write(var[elements] + ";")

        for quad in quad_list:
            f_c.write("\nL_" + str(quad.quad_label) + ": ")
            if str(quad.operator) in operator_list:
                f_c.write(str(quad.operand3) + " = " + str(quad.operand1) + " " +
                          str(quad.operator) + " " + str(quad.operand2) + ";")
            elif str(quad.operator) == "jump":
                f_c.write("goto " + "L_" + str(quad.operand3) + ";")
            elif str(quad.operator) == ":=":
                f_c.write(str(quad.operand3) + " = " + str(quad.operand1) + ";")
            elif str(quad.operator) in rel_op_list:
                if str(quad.operator) == "=":
                    f_c.write("if(" + str(quad.operand1) + " " + str(quad.operator) +
                              str(quad.operator) + " " + str(quad.operand2) + ")" + " goto L_" + str(quad.operand3) + ";")
                elif str(quad.operator) == "<>":
                    f_c.write("if(" + str(quad.operand1) + " != " + str(quad.operand2) + ")" + " goto L_" + str(
                        quad.operand3) + ";")
                else:
                    f_c.write("if(" + str(quad.operand1) + " " + str(quad.operator) +
                              " " + str(quad.operand2) + ")" + " goto L_" + str(quad.operand3) + ";")
            elif str(quad.operator) == "halt":
                f_c.write("return 0;")
            elif str(quad.operator) == "in":
                f_c.write('scanf("%d",&' + quad.operand1 + ');')
            elif str(quad.operator) == "out":
                f_c.write('printf("%d\\n",' + quad.operand1 + ');')
            elif str(quad.operator) == "end_block":
                f_c.write("{}")
        f_c.write("\n}")
        f_c.close()

    else:
        print("\nThis program cannot be converted to c.\n")


def add_scope():
    global global_nesting_level
    scope = Scope([], global_nesting_level)
    global_nesting_level = global_nesting_level + 1
    scope_list.append(scope)


def delete_scope():
    global global_nesting_level
    global_nesting_level = global_nesting_level - 1
    del scope_list[len(scope_list)-1]


def find_in_symbol_table(entity_name):
    # Searches for entity after the Symbol Table is complete
    for scope in reversed(scope_list):
        for entity in scope.entity_list:
            if entity.name == entity_name:
                return entity, scope.nesting_level
    # print(f"ERROR: Entity '{entity_name}' not found!")
    return False


def save_symbol_table():
    global sb_file_str
    sb_file_str = sb_file_str + "+---------------------------------------+\n"
    for scope in reversed(scope_list):
        sb_file_str = sb_file_str + scope.__str__()
        for entity in scope.entity_list:
            sb_file_str = sb_file_str + " -- " + entity.__str__()
        sb_file_str = sb_file_str + "\n"
    sb_file_str = sb_file_str + "\n"


def write_sb_file():
    # Generating the symbol table file
    sb_file_name = FILE_NAME + ".symb"
    if os.path.exists(sb_file_name):
        os.remove(sb_file_name)
    sb_file = open(sb_file_name, "a")
    sb_file.write(sb_file_str)
    sb_file.close()


def print_scope_list():
    print("\n---------| SCOPE LIST |---------")
    for scope in reversed(scope_list):
        print(scope, end="")
        for entity in scope.entity_list:
            print(" -- " + entity.__str__(), end="")
        print()


def add_entity(entity):
    if entity.type_of_entity == "Parameter" or \
            entity.type_of_entity == "Variable" or \
            entity.type_of_entity == "TempVariable":
        scope_list[-1].variable_offset = scope_list[-1].variable_offset + 4
        print(f"ADDED TO SCOPE {len(scope_list)-1} {scope_list[-1].variable_offset} {entity} {entity.type_of_entity}")
    scope_list[len(scope_list)-1].add_entity(entity)


def riscv_write(command):
    print(command)
    final_code_list.append(command)


def gnvlcode(v):
    global final_code_list
    entity, entity_nesting_level = find_in_symbol_table(v)
    levels = scope_list[-1].nesting_level - entity_nesting_level
    riscv_write(f"lw t0, -4(sp)")
    for i in range(levels):
        riscv_write(f"lw t0, -4(t0)")
    riscv_write(f"addi t0, t0, -{entity.offset}")


def loadvr(v, r):
    # print(f"LOADVR {v} {r}")
    if v.isnumeric():                   # Constant
        riscv_write(f"li t{r}, {v}")
    else:
        entity, entity_level = find_in_symbol_table(v)
        current_level = scope_list[-1].nesting_level
        
        if entity.type_of_entity == "Variable" and entity_level == 0:
            riscv_write(f"lw t{r}, -{entity.offset}(gp)")
        elif entity_level == current_level and local_var_cv_par_temp_var(entity):
            riscv_write(f"lw t{r}, -{entity.offset}(sp)")
        elif entity_level == current_level and ref_param(entity):
            riscv_write(f"lw t0, -{entity.offset}(sp)")
            riscv_write(f"lw t{r}, (t0)")
        elif entity_level < current_level and local_var_cv_par(entity):
            gnvlcode(v)
            riscv_write(f"lw t{r}, (t0)")
        elif entity_level < current_level and ref_param(entity):
            gnvlcode(v)
            riscv_write(f"lw t0, (t0)")
            riscv_write(f"t{r}, (t0)")
        else:
            print("ERROR : loadvr")
            print(entity, end=" ")
            print(entity_level)
            print(current_level)
            sys.exit(-1)


def local_var_cv_par(entity):
    if entity.type_of_entity == "Variable" or \
            (entity.type_of_entity == "Parameter" and entity.par_mode == "cv"):
        return True
    return False


def local_var_cv_par_temp_var(entity):
    if local_var_cv_par(entity) or entity.type_of_entity == "TempVariable":
        return True
    return False


def ref_param(entity):
    if entity.type_of_entity == "Parameter" and entity.par_mode == "ref":
        return True
    return False


def cv_param(entity):
    if entity.type_of_entity == "Parameter" and entity.par_mode == "cv":
        return True
    return False


def storerv(r, v):
    # print("STOREVR")

    if v.isnumeric():
        loadvr(r, "0")
        storerv("0", v)

    else:
        entity, entity_level = find_in_symbol_table(v)
        current_level = scope_list[-1].nesting_level

        if entity.type_of_entity == "Variable" and entity_level == 0:
            riscv_write(f"sw t{r}, -{entity.offset}(gp)")
        elif entity.type_of_entity == "Variable" or (cv_param(entity) and entity_level == current_level) or \
                entity.type_of_entity == "TempVariable":
            riscv_write(f"sw t{r}, -{entity.offset}(sp)")
        elif ref_param(entity) and entity_level == current_level:
            riscv_write(f"lw t0, -{entity.offset}(sp)")
            riscv_write(f"sw t{r}, (t0)")
        elif entity.type_of_entity == "Variable" or (cv_param(entity) and entity_level < current_level):
            gnvlcode(v)
            riscv_write(f"sw t{r}, (t0)")
        elif ref_param(entity) and entity_level < current_level:
            gnvlcode(v)
            riscv_write(f"lw t0, (t0)")
            riscv_write(f"sw t{r}, (t0)")
        else:
            print(f"ERROR : storerv {r} {v}")   # TODO: cleanup
            print(entity, end=" ")
            print(entity_level)
            print(current_level)
            sys.exit(-1)


def generate_riscv(quad, block_name):
    global number_of_params
    global num_flag
    global first_parameter

    riscv_write(f"L{num_flag}:")
    num_flag += 1

    if quad.operator == "jump":
        riscv_write(f"j {quad.quad_label}")

    elif quad.operator == "begin_block":
        if block_name == program_name:
            riscv_write(f"addi sp, sp, {scope_list[0].variable_offset}")
            riscv_write(f"move gp, sp")
        else:
            riscv_write(f"sw ra, -0(sp)")

    elif quad.operator == "end_block":
        riscv_write(f"lw ra, -0(sp)")
        riscv_write(f"jr ra")

    elif quad.operator in rel_op_list:
        riscv_operator = convert_to_riscv_branch(quad.operator)
        loadvr(quad.operand1, "1")
        loadvr(quad.operand2, "2")
        riscv_write(f"{riscv_operator}, t1, t2, {quad.operand3}")

    elif quad.operator == "out":
        entity, level = find_in_symbol_table(quad.operand1)
        riscv_write(f"lw t1, -{entity.offset}(sp)")

    elif quad.operator == "halt":
        riscv_write(f"li a0, 0")
        riscv_write(f"li a7,93")
        riscv_write(f"ecall")

    elif quad.operator == ":=":
        loadvr(quad.operand1, "1")
        storerv("1", quad.operand3)

    elif quad.operator in operator_list:
        riscv_operator = convert_to_riscv_operator(quad.operator)
        loadvr(quad.operand1, "1")
        loadvr(quad.operand2, "2")
        riscv_write(f"{riscv_operator} t1, t1, t2")
        storerv("1", quad.operand3)

    elif quad.operator == "RET":
        loadvr(quad.operand1, "1")
        riscv_write(f"lw t0, -8(sp)")
        riscv_write(f"sw t1, (t0)")

    elif quad.operator == "par":
        entity, entity_level = find_in_symbol_table(quad.operand1)

        if block_name == program_name:
            caller_level = 0
            frame_length = entity.offset + 12+4*number_of_params #scope_list[0].variable_offset

        else:
            caller, caller_level = find_in_symbol_table(block_name)
            frame_length = caller.frame_length

        if first_parameter:
            riscv_write(f"addi fp, sp, {frame_length}")  # TODO: calculate frame length
            first_parameter = False

        if quad.operand2 == "CV":
            loadvr(quad.operand1, "1")
            riscv_write(f"sw t1, -{12 + 4 * number_of_params}(fp)")
        elif quad.operand2 == "REF":
            if caller_level == entity_level:

                if entity.type_of_entity == "Variable" or cv_param(entity):
                    riscv_write(f"addi t0, sp, -{entity.offset}")
                    riscv_write(f"sw t0, -{12 + 4 * number_of_params}(fp)")

                elif ref_param(entity):
                    riscv_write(f"lw t0, -{entity.offset}(sp)")
                    riscv_write(f"sw t0, -{12 + 4 * number_of_params}(fp)")
            else:
                if entity.type_of_entity == "Variable" or cv_param(entity):
                    gnvlcode(quad.operand1)
                    riscv_write(f"sw t0, -{12 + 4 * number_of_params}(fp)")

                elif ref_param(entity):
                    gnvlcode(quad.operand1)
                    riscv_write(f"lw t0, (t0)")
                    riscv_write(f"sw t0, -{12 + 4 * number_of_params}(fp)")

        elif quad.operand2 == "RET":
            riscv_write(f"addi t0, sp, -{entity.offset}")
            riscv_write(f"sw t0, -8(fp)")
        number_of_params += 1

    elif quad.operator == "call":

        if block_name == program_name:
            caller_level = 0
            # frame_length = scope_list[0].variable_offset
        else:
            caller, caller_level = find_in_symbol_table(block_name)
            # frame_length = caller.frame_length

        callee, callee_level = find_in_symbol_table(quad.operand1)

        if caller_level == callee_level:
            riscv_write(f"lw t0, -4(sp)")
            riscv_write(f"sw t0, -4(fp)")
        else:
            riscv_write(f"sw sp, -4(fp)")

        riscv_write(f"addi sp, sp, {callee.frame_length}")
        riscv_write(f"jal L{callee.start_quad - 1}")
        riscv_write(f"addi sp, sp, -{callee.frame_length}")


def convert_to_riscv_branch(operator):
    rel_op_to_riscv = [["=", "beq"], ["<", "blt"], [">", "bgt"],
                       ["<=", "ble"], [">=", "bge"], ["<>", "bne"]]
    for riscv_op in rel_op_to_riscv:
        if operator == riscv_op[0]:
            return riscv_op[1]
    return "OP_MATCH_FAILED"


def convert_to_riscv_operator(operator):
    op_to_riscv = [["+", "add"], ["-", "sub"], ["*", "mul"], ["/", "div"]]

    for riscv_op in op_to_riscv:
        if operator == riscv_op[0]:
            return riscv_op[1]
    return "OP_MATCH_FAILED"


def write_riscv_file():
    riscv_file_name = FILE_NAME + ".asm"
    if os.path.exists(riscv_file_name):
        os.remove(riscv_file_name)
    riscv_file = open(riscv_file_name, "a")
    for command in final_code_list:
        riscv_file.write(command + "\n")
    riscv_file.close()


def print_riscv_commands():
    for command in final_code_list:
        print(command)


def main():
    if len(sys.argv) != 2:
        sys.exit("ERROR: Usage $python met.py <inputfile>")

    if sys.argv[1].split(".")[-1] != "ci":
        sys.exit("ERROR: Compiler accepts only '.ci' files")

    lex_object = Lex(1, sys.argv[1], None)
    parser_obj = Parser(lex_object)
    parser_obj.syntax_analyzer()

    # print_quads()
    write_sb_file()
    convert_int()
    convert_c()

    write_riscv_file()
    print_riscv_commands()


if __name__ == "__main__":
    main()
