# C-imple_Compiler


    def __program(self):

    def __block(self): OK

    def __declarations(self):

    def __varlist(self):

    def __subprograms(self):

    def __subprogram(self):

    def __formalparlist(self):

    def __formalparitem(self):

    def __statements(self):

    def __blockstatements(self):

    def __ifStat(self):

    def __elsepart(self):
    
    def __statement(self):

    def __assignStat(self):

    def __whileStat(self):

    def __switchcaseStat(self):

    def __forcaseStat(self):

    def __incaseStat(self):

    def __returnStat(self):

    def __callStat(self):

    def __printStat(self):

    def __inputStat(self):

    def __actualparlist(self):

    def __actualparitem(self):

    def __condition(self):

    def __boolterm(self):

    def __boolfactor(self):

    def __expression(self):

    def __term(self):

    def __factor(self):

    def __idtail(self): 

    def __optionalSign: OK

    def __reloperator(self): OK

    def __addoperator(self): OK

    def __muloperator(self): OK

    def __integervalue(self): OK 

    def __idvalue(self): OK

1: begin_block P1 _ _
2: - Y 1 T_0
3: := T_0 _ Y
4: = X 1 6
5: jump _ _ 8
6: retv X _ _
7: jump _ _ 14
8: - X 1 T_1
9: par T_1 CV _
10: par Y REF _
11: par T_2 RET _
12: call _ _ P1
13: retv T_2 _ _
14: end_block P1 _ _
15: begin_block ex1 _ _
16: := 10 _ c
17: := 5 _ b
18: par c CV _
19: par b REF _
20: par T_3 RET _
21: call _ _ P1
22: := T_3 _ g
23: halt _ _ _
24: end_block ex1 _ _