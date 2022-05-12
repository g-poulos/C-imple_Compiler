import unittest
from colorama import Fore

import met
from met import *
import os

program_pairs = [["tests/intermediate/intermediate_test_1.ci", "tests/intermediate/expected/inde_expected_1.txt"],
                 ["tests/intermediate/intermediate_test_2.ci", "tests/intermediate/expected/inde_expected_2.txt"],
                 ["tests/intermediate/intermediate_test_3.ci", "tests/intermediate/expected/inde_expected_3.txt"],
                 ["tests/intermediate/switchCase_test.ci", "tests/intermediate/expected/switchCase_expected.txt"],
                 ["tests/intermediate/forCase_test.ci", "tests/intermediate/expected/forCase_expected.txt"],
                 ["tests/intermediate/inCase_test.ci", "tests/intermediate/expected/inCase_expected.txt"],
                 ["tests/intermediate/conditional.ci", "tests/intermediate/expected/conditional_expected.txt"],
                 ["tests/intermediate/small.ci", "tests/intermediate/expected/small_expected.txt"],
                 ["tests/intermediate/ifwhile.ci", "tests/intermediate/expected/ifwhile_expected.txt"]]


def file_to_list(filename):
    file = open(filename, "r")
    file_list = file.read().split("\n")
    file.close()
    return file_list


class CompilerTester(unittest.TestCase):

    def test_quad_programs(self):
        for pair in program_pairs:
            self.__test_quad_list(pair[0], pair[1])

    def __test_quad_list(self, program, expected):
        test_name = program.split("/")
        test_name = test_name[len(test_name)-1]
        print(Fore.CYAN + "Processing " + test_name + "...")
        expected_quads = file_to_list(expected)
        lex_object = Lex(1, program, None)
        parser_obj = Parser(lex_object)
        parser_obj.syntax_analyzer()

        for quad, expected_quad in zip(quad_list, expected_quads):
            self.assertEqual(str(expected_quad), str(quad))
        reset_global_variables()
        print(Fore.GREEN + "DONE\n")

    @staticmethod
    def test_complete_programs():
        directory = "tests/complete_programs"
        program_list = os.listdir(directory)
        program_count = 1
        met.PRINT_SCOPE_LIST = False
        for program_file in program_list:
            print(Fore.CYAN + "Processing " + program_file + "...")
            lex_object = Lex(1, directory + "/" + program_file, None)
            parser_obj = Parser(lex_object)
            parser_obj.syntax_analyzer()
            reset_global_variables()
            print(Fore.GREEN + f"DONE\n [{program_count}/{len(program_list)}]")
            program_count = program_count + 1

    def test_loadvr_boolean_functions(self):
        variable = Variable("Var", "Variable", 0)
        cv_par = Parameter("cv_par", "CV", 0)
        ref_par = Parameter("ref_par", "REF", 0)
        temp_var = TempVariable("temp_var", 0)

        self.assertTrue(local_var_cv_par(variable))
        self.assertTrue(local_var_cv_par(cv_par))
        self.assertFalse(local_var_cv_par(ref_par))
        self.assertFalse(local_var_cv_par(temp_var))

        self.assertTrue(local_var_cv_par_temp_var(variable))
        self.assertTrue(local_var_cv_par_temp_var(cv_par))
        self.assertTrue(local_var_cv_par_temp_var(temp_var))
        self.assertFalse(local_var_cv_par_temp_var(ref_par))

        self.assertTrue(ref_param(ref_par))
        self.assertFalse(ref_param(variable))
        self.assertFalse(ref_param(cv_par))
        self.assertFalse(ref_param(temp_var))

        self.assertTrue(cv_param(cv_par))
        self.assertFalse(cv_param(variable))
        self.assertFalse(cv_param(ref_par))
        self.assertFalse(cv_param(temp_var))
