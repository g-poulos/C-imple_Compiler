import sys

line_counter = 1


class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number


def is_number(file, character):
    recognized_string = character
    while (True):
        if (character.isnumeric()):
            recognized_string = recognized_string + character
        elif (character.isalpha()):
            # Error if a letter is inside of a number
            file.seek(file.tell() - 1)
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
            return recognized_string, "keyword"
        else:
            recognized_string = recognized_string + character


def is_assignment(file, first_char):
    recognized_string = ""
    first_character = first_char
    second_character = file.read(1)
    recognized_string = first_character + second_character
    if recognized_string == ":=":
        return recognized_string, "assignment"


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
    group_symbol_list = ["{", "}", "(", ")", "[", "]"]
    delimeter_list = [",", ";", "."]

    character = first_char
    if (character == "+"):
        return character, "addOperator"
    elif (character == "-"):
        return character, "addOperator"
    elif (character in group_symbol_list):
        return character, "groupSymbol"
    elif (character in delimeter_list):
        return character, "delimeter"
    else:
        file.seek(file.tell() - 1)
        return "", ""


def clear_blank_char(file):
    character = file.read(1)
    while (True):
        print(character)
        if (not character.isspace()):
            file.seek(file.tell() - 1)
            break
        character = file.read(1)


def lex(file):
    family = ""
    first_char = file.read(1)
    clear_blank_char(file)

    if first_char.isnumeric():
        recognized_string, family = is_number(file, first_char)
        print(recognized_string + " family: " + family + " line: ", line_counter)
    elif first_char.isalpha():
        recognized_string, family = is_keyword(file, first_char)
        print(recognized_string + " family: " + family + " line: ", line_counter)
    elif first_char == ":":
        recognized_string, family = is_assignment(file, first_char)
        print(recognized_string + " family: " + family + " line: ", line_counter)
    elif first_char == ">" or first_char == "<":
        recognized_string, family = is_rel_operator(file, first_char)
        print(recognized_string + " family: " + family + " line: ", line_counter)
    else:
        recognized_string, family = is_simple(file)
        print(recognized_string + " family: " + family + " line: ", line_counter)

    return Token(recognized_string, family, line_counter)


def main():
    if (len(sys.argv) < 3):
        print(sys.argv[1])

    file = open(sys.argv[1], "r")
    lex(file)


if __name__ == "__main__":
    main()
