import sys


class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

def isNumber(file):
    recognized_string = ""
    while True:
            character = file.read(1)
            if(not character.isnumeric()):
                return recognized_string, "number"
            elif(int(character) in range(10)):
                recognized_string = recognized_string + character

def isKeyword(file):
    recognized_string = ""
    while True:
            character = file.read(1)
            if not character.isnumeric() and not character.isalpha():
                return recognized_string, "keyword"
            else:
                recognized_string = recognized_string + character

def isSimple(file):
    group_symbol_list = ["{", "}", "(", ")", "[", "]"]
    delimeter_list = [",", ";", "."]

    character = file.read(1)
    if(character == "+"):
        return character, "addOperator"
    elif(character == "-"):
        return character, "addOperator"
    elif(character in group_symbol_list):
        return character, "groupSymbol"
    elif(character in delimeter_list):
        return character, "delimeter"
    else:
        return "", ""

def clearBlankChar(file):
    character = file.read(1)
    while(True):
        print(character)
        if(not character.isspace()):
            file.seek(file.tell()-1)
            break
        character = file.read(1)


def lex(file):
    family = ""
    line_counter = 0

    clearBlankChar(file)

    recognized_string, family = isNumber(file)
    #recognized_string, family = isSimple(file)
    #recognized_string, family = isKeyword(file)

    print(recognized_string + " family: " + family + " line: ", line_counter)
    return Token(recognized_string, family, line_counter)

def main():
    #if(len(sys.argv) < 3):
            #print(sys.argv[1]) 

    with open(sys.argv[1], "r") as file:
        lex(file)

if __name__ == "__main__":
    main()