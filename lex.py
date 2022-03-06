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

class Lex:
    def __init__(self, current_line, file_name, token):
        self.current_line = current_line
        self.file_name = file_name
        self.token = token 
        

    def is_number(self, file, character):
        recognized_string = ""
        while (True):
            #print(recognized_string)
            if (character.isnumeric()):
                recognized_string = recognized_string + character
            elif (character.isalpha()):
                sys.exit("ERROR: Expected number but found " + character + 
                                            " at line " + str(self.current_line))
            else:
                if (int(recognized_string) >= -(pow(2, 32)-1) and 
                    int(recognized_string) <= (pow(2, 32)-1)):
                        file.seek(file.tell()-1)
                        return recognized_string, "number"
                else:
                    sys.exit("ERROR: Constant exceeded bounds \n \
                    Value must be between -((2^32)-1) and (2^32)-1")
            character = file.read(1)


    def is_keyword(self, file, first_char):
        recognized_string = first_char
        while True:
            character = file.read(1)
            if not character.isnumeric() and not character.isalpha():
                if len(recognized_string) <= 30:
                    file.seek(file.tell() - 1)
                    if recognized_string in group_keyword_list:
                        return recognized_string, "keyword"
                    else:
                        return recognized_string, "identifier"
                else:
                    sys.exit("ERROR: Expected string has length greater than \
                                    allowed (30) at line " + str(self.current_line))
            else:
                recognized_string = recognized_string + character


    def is_assignment(self, file, first_char):
        recognized_string = ""
        first_character = first_char
        second_character = file.read(1)
        recognized_string = first_character + second_character
        if recognized_string == ":=":
            return recognized_string, "assignment"
        else:
            sys.exit("ERROR: Expected := but found " + first_char + 
                            second_character + " at line " + str(self.current_line))


    def is_rel_operator(self, file, first_char):
        recognized_string = ""
        character = first_char
        while True:
            if character == "=":
                return character, "relOperator"
            elif character == ">":
                second_char = file.read(1)
                if second_char == "=":
                    recognized_string = character + second_char
                    return recognized_string, "relOperator"
                else:
                    file.seek(file.tell() - 1)
                    return character, "relOperator"
            elif character == "<":
                second_char = file.read(1)
                if second_char == "=" or second_char == ">":
                    recognized_string = character + second_char
                    return recognized_string, "relOperator"
                else:
                    file.seek(file.tell() - 1)
                    return character, "relOperator"


    def is_simple(self, file, first_char):
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
            return "a", "a"  # What to do in case of no `.` at the end of the program


    def clear_blank_char(self, file, character):
        while (True):
            if (not character.isspace()):
                return character
            elif (character == "\n"):
                self.current_line = self.current_line + 1
                character = file.read(1)
            else:
                character = file.read(1)


    def is_comment(self, file, character):
        character = file.read(1)
        while (character != "#"):
            character = file.read(1)
            if (not character):
                sys.exit("ERROR: '#' was not closed, line: " + str(self.current_line))
        character = file.read(1)
        return character


    def next_token(self, file, file_pointer):
        file.seek(file_pointer)
        family = ""
        recognized_string = ""
        
        first_char = file.read(1)

        # Clear comments and blank characters 
        while first_char.isspace() or first_char == "#":
            if first_char == "#":
                first_char = self.is_comment(file, first_char) 
            else:
                first_char = self.clear_blank_char(file, first_char)

        if first_char.isnumeric():
            recognized_string, family = self.is_number(file, first_char)
        elif first_char.isalpha():
            recognized_string, family = self.is_keyword(file, first_char)
        elif first_char == ":":
            recognized_string, family = self.is_assignment(file, first_char)
        elif first_char == ">" or first_char == "<" or first_char == "=":
            recognized_string, family = self.is_rel_operator(file, first_char)
        elif first_char in group_symbol_list or first_char in delimeter_list or first_char in operator_list:
            recognized_string, family = self.is_simple(file, first_char)
        else:
            if first_char == "":
                sys.exit()
            else:
                sys.exit("ERROR: " + first_char + " does not belong at C-imple. line: " + str(self.current_line))

        file_pointer = file.tell()
        file.seek(0)
        print(f"{recognized_string:12} family: {family:12} line: {self.current_line:3}")
        return file_pointer, Token(recognized_string, family, self.current_line)

def main():
    if (len(sys.argv) != 2):
        # Temporary usage
        sys.exit("ERROR: Usage $ python lex.py <inputfile>")

    current_pointer = 0
    next_pointer = -1

    token1 = Token("Xaxa", "xaxa", 0)
    lex_object = Lex(1, sys.argv[1], token1)

    with open(sys.argv[1], "r") as file:
        while True:
            
            # print(current_pointer, next_pointer)
            if (input()):
                next_pointer, token = lex_object.next_token(file, current_pointer)
                current_pointer = next_pointer


if __name__ == "__main__":
    main()
