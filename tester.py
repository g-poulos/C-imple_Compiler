import unittest
from met import *

ex2_quads = ["1: begin_block exams _ _",
                 "2: := 1 _ a",
                 "3: + a b T_0",
                 "4: < T_0 1 6",
                 "5: jump _ _ 28",
                 "6: < b 5 8",
                 "7: jump _ _ 28",
                 "8: = t 1 10",
                 "9: jump _ _ 12",
                 "10: := 2 _ c",
                 "11: jump _ _ 17",
                 "12: = t 2 14",
                 "13: jump _ _ 16",
                 "14: := 4 _ c",
                 "15: jump _ _ 17",
                 "16: := 0 _ c",
                 "17: < a 1 19",
                 "18: jump _ _ 27",
                 "19: = a 2 21",
                 "20: jump _ _ 26",
                 "21: = b 1 23",
                 "22: jump _ _ 25",
                 "23: := 2 _ c",
                 "24: jump _ _ 21",
                 "25: jump _ _ 26",
                 "26: jump _ _ 17",
                 "27: jump _ _ 3",
                 "28: halt _ _ _",
                 "29: end_block exams _ _"]


class QuadTester(unittest.TestCase):

    def test_quad_list(self):
        lex_object = Lex(1, "intermediate_test_2.ci", None)
        parser_obj = Parser(lex_object)
        parser_obj.syntax_analyzer()

        for quad, expected_quad in zip(quad_list, ex2_quads):
            self.assertEqual(str(quad), str(expected_quad))
