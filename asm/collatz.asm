LDI R6 0xF3    ; input port
PLD R1 R6      ; store input in R1
LDI R6 0xF4    ; output port

LDI R7 0x1A    ; return address if even
STR R7 0x0     ; store in mem[0]
LDI R7 0x14    ; return address if odd
STR R7 0x1     ; store in mem[1]
LDI R7 0xC     ; loop return address
STR R7 0x2     ; store in mem[2]
LDI R7 0x1E    ; halt return address
STR R7 0x3     ; store in mem[3]

LDI R2 0x01    ; load mask

PST R1 R6      ; print number

CMP R1 R2      ; x-1
LOD R7 0x3     ; load return address for halt
BRH 0b001 R7   ; jump to halt

AND R3 R1 R2   ; applied mask
CMP R3 R0      ; compare (just to update flags)

LOD R7 0x0     ; load return address for even
BRH 0b001 R7   ; branch if even

; odd case
ADD R4 R1 R1   ; 2x
ADD R4 R4 R1   ; 3x
INC R4 0x1     ; 3x+1
MOV R1 R4      ; update number
LOD R7 0x2     ; load return address for loop
BRH 0b000 R7   ; jump to loop

; even case
RSH R4 R1 0x1  ; x/2
MOV R1 R4      ; update number
LOD R7 0x2     ; load return address for loop
BRH 0b000 R7   ; jump to loop

KYS            ; halt