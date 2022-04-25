#include <stdio.h> 

int main() 
{
L_1: 
L_2: T_0 = 0;
L_3: if(a > 0) goto L_5
L_4: goto L_8;
L_5: T_1 = a - 1;
L_6: a = T_1;
L_7: T_0 = 1;
L_8: if(a < 0) goto L_10
L_9: goto L_13;
L_10: T_2 = a + 1;
L_11: a = T_2;
L_12: T_0 = 1;
L_13: if(T_0 == 1) goto L_2
L_14: return 0;
L_15: 
}