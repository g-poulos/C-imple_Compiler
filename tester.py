import unittest
from colorama import Fore
from met import *

program_pairs = [["tests/intermediate/intermediate_test_1.ci", "tests/intermediate/expected/inde_expected_1.txt"],
                 ["tests/intermediate/intermediate_test_2.ci", "tests/intermediate/expected/inde_expected_2.txt"],
                 ["tests/intermediate/intermediate_test_3.ci", "tests/intermediate/expected/inde_expected_3.txt"],
                 ["tests/intermediate/switchCase_test.ci", "tests/intermediate/expected/switchCase_expected.txt"],
                 ["tests/intermediate/forCase_test.ci", "tests/intermediate/expected/forCase_expected.txt"],
#                 ["tests/intermediate/inCase_test.ci", "tests/intermediate/expected/inCase_expected.txt"],
                 ["tests/intermediate/conditional.ci", "tests/intermediate/expected/conditional_expected.txt"],
                 ["tests/intermediate/small.ci", "tests/intermediate/expected/small_expected.txt"]]


def file_to_list(filename):
    file = open(filename, "r")
    file_list = file.read().split("\n")
    file.close()
    return file_list


class QuadTester(unittest.TestCase):

    def test_quad_programs(self):
        for pair in program_pairs:
            self.__test_quad_list(pair[0], pair[1])

    def __test_quad_list(self, program, expected):
        expected_quads = file_to_list(expected)
        lex_object = Lex(1, program, None)
        parser_obj = Parser(lex_object)
        parser_obj.syntax_analyzer()

        for quad, expected_quad in zip(quad_list, expected_quads):
            self.assertEqual(str(expected_quad), str(quad))
        reset_global_variables()
        print(Fore.GREEN + "DONE:" + program)




