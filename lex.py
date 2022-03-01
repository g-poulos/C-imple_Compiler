import sys
 
line_counter = 1
group_symbol_list = ["{", "}", "(", ")", "[", "]"]
delimeter_list = [",", ";", "."]
operator_list = ["+", "-", "*", "/"]


class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number


def is_number(file, character):
    recognized_string = ""
    while(True):        
        if (character.isnumeric()):
            recognized_string = recognized_string + character
        elif (character.isalpha()):
            file.seek(file.tell()-1)
            sys.exit("ERROR: Expected number but found " + character + " at line " + str(line_counter))
        else:
            file.seek(file.tell() - 1)
            return recognized_string, "number"
        character = file.read(1)


def is_keyword(file, first_char):
    recognized_string = first_char
    while True:
        character = file.read(1)
        if not character.isnumeric() and not character.isalpha():
            if len(recognized_string) <= 30:
                return recognized_string, "keyword"
            else:
                sys.exit("ERROR: Expected string has length greater than allowed (30) at line " + str(line_counter))
        else:
            recognized_string = recognized_string + character
        


def is_assignment(file, first_char):
    recognized_string = ""
    first_character = first_char
    second_character = file.read(1)
    recognized_string = first_character + second_character
    if recognized_string == ":=":
        return recognized_string, "assignment"
    else:
        sys.exit("ERROR: Expected := but found " + first_char + second_character + " at line " + str(line_counter))


def is_rel_operator(file, first_char):
    recognized_string = ""
    character = first_char
    while True:
        if character == ">":
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


def is_simple(file, first_char):

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
        return "a", "a"   #What to do in case of no `.` at the end of the program 


def clear_blank_char(file, character):
    global line_counter
    while(True):
        if(not character.isspace()):
            return character
        elif (character == "\n"):
            line_counter = line_counter + 1
            character = file.read(1)
        else:
            character = file.read(1)


def is_comment(file, character):
    character = file.read(1)
    while (character != "#"):
        character = file.read(1)
        if (not character):
            sys.exit("ERROR: '#' was not closed, line: " + str(line_counter))
    
def lex(file, file_pointer):
    file.seek(file_pointer)
    family = ""
    recognized_string = ""
    first_char = file.read(1)
    first_char = clear_blank_char(file, first_char)

    if first_char.isnumeric():
        recognized_string, family = is_number(file, first_char)
    elif first_char.isalpha():
        recognized_string, family = is_keyword(file, first_char)
    elif first_char == ":":
        recognized_string, family = is_assignment(file, first_char)
    elif first_char == ">" or first_char == "<":
        recognized_string, family = is_rel_operator(file, first_char)
    elif first_char == "#":
        is_comment(file, first_char) # If there is a comment at the beginning lex() returns empty recognized_string and family
    elif first_char in group_symbol_list or first_char in delimeter_list or first_char in operator_list:
        recognized_string, family = is_simple(file, first_char)
    else:
        sys.exit("ERROR: " + first_char + " does not belong at C-imple. line: " + str(line_counter))

    file_pointer = file.tell()
    file.seek(0)
    print(f"{recognized_string:12} family: {family:12} line: {line_counter:3}")
    return file_pointer, Token(recognized_string, family, line_counter)


def main():
    if (len(sys.argv) != 2):
        # Temporary usage
        sys.exit("ERROR: Usage $ python lex.py <inputfile>")

    current_pointer = 0
    next_pointer = -1
    with open(sys.argv[1], "r") as file: 
        while True:
            next_pointer, token = lex(file, current_pointer)
            #print(current_pointer, next_pointer)
            if (next_pointer == current_pointer):
                break
            current_pointer = next_pointer

if __name__ == "__main__":
    main()
