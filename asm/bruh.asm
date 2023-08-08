LDI R6 0xF4
LDI R1 0b01010101
LDI R2 0b00001111

AND R3 R1 R2
PST R3 R6            ; 0b00000101

ORR R3 R1 R2
PST R3 R6            ; 0b01011111

XOR R3 R1 R2
PST R3 R6            ; 0b01011010

NOT R3 R1
PST R3 R6            ; 0b10101010

RSH R3 R2 0x1
PST R3 R6            ; 0b00000111

LSH R3 R2 0x1
PST R3 R6            ; 0b00011110

ROT R3 R2 0x3
PST R3 R6            ; 0b111000001

PCS R3
PST R3 R6            ; whatever address is in PC

KYS                  ; halt