; example program: fibonacci sequence
LDI R6 0xF4 ; current port (decimal display)
LDI R7 0x5  ; loop address
LDI R5 0xC  ; overflow halt address
LDI R1 1
LDI R2 0
ADD R1 R1 R2 1
BRH 0b011 R5 ; if overflow, halt
PST R1 R6
ADD R2 R1 R2 1
BRH 0b011 R5 ; if overflow, halt
PST R2 R6
BRH 0b000 R7 ; jump to return address in R7
NOP 1