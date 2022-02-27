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
                return recognized_string
            elif(int(character) in range(10)):
                recognized_string = recognized_string + character

def isAddOperator(file):
    character = file.read(1)
    #if(character == "+"):
    #    recognized_st
    #elif(character == "-"):

def lex(file):
    family = ""
    line_counter = 0
    
    recognized_string = isNumber(file)
    if(recognized_string != ""):
        family = "number"
    
    print(recognized_string + " family: " + family + " line: ", line_counter)
    return Token(recognized_string, family, line_counter)

def main():
    if(len(sys.argv) < 3):
            print(sys.argv[1]) 

    file = open(sys.argv[1], "r")
    lex(file)

if __name__ == "__main__":
    main()