LDI R1 1
LDI R2 0xA
LDI R7 0x4
LDI R6 0xF6
LDI R5 0xF4
PLD R3 R6
PST R3 R5
INC R1 1
CMP R2 R1
BRH 0b010 R7
KYS