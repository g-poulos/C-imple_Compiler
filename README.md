# C-imple_Compiler

## Example 1 - Expected Outcome
```
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
```

## Conditionals Example - Expected Outcome
```
1: begin_block conditional _ _
2: >, a, b, _       # true
3: jump, _, _, 4
4: >, a, c, 6
5: jump, _, _, _    # false
6: >, b, c, 10
7: jump, _, _, 8
8: >, a, 1, 108
9: jump, _, _, _    # false
10: =, b, 1, _       # true
11: jump, _, _, _
12: retv X _ _
13: halt _ _ _
14: end_block conditional _ _
```