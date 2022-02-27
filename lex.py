import sys


class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number


def lex(file):
    recognized_string = ""
    while True:
        character = file.read(1)
        while int(character) in range(0, 9):
            recognized_string = recognized_string + character
            character = file.read(1)
        print(recognized_string)
        break


def main():
    if(len(sys.argv) < 3):
            print(sys.argv[1]) 

    file = open(sys.argv[1], "r")
    lex(file)

if __name__ == "__main__":
    main()