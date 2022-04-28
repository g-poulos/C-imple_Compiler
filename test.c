#include <stdio.h> 

int main() 
{
int a,b,T_0,t,c;
L_1: 
L_2: a = 1;
L_3: T_0 = a + b;
L_4: if(T_0 < 1) goto L_6;
L_5: goto L_28;
L_6: if(b < 5) goto L_8;
L_7: goto L_28;
L_8: if(t == 1) goto L_10;
L_9: goto L_12;
L_10: c = 2;
L_11: goto L_17;
L_12: if(t == 2) goto L_14;
L_13: goto L_16;
L_14: c = 4;
L_15: goto L_17;
L_16: c = 0;
L_17: if(a < 1) goto L_19;
L_18: goto L_27;
L_19: if(a == 2) goto L_21;
L_20: goto L_26;
L_21: if(b == 1) goto L_23;
L_22: goto L_25;
L_23: c = 2;
L_24: goto L_21;
L_25: goto L_26;
L_26: goto L_17;
L_27: goto L_3;
L_28: return 0;
L_29: 
}