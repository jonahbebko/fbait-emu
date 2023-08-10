LDI R1 0xFE ; select gpu mode as 2d graphics
LDI R2 0x03
PST R2 R1

LDI R1 0xF8 ; set x1
LDI R2 0x01
PST R2 R1

LDI R1 0xFA ; set y1
LDI R2 0x01
PST R2 R1

LDI R1 0xF9 ; set x2
LDI R2 0x10
PST R2 R1

LDI R1 0xFB ; set y2
LDI R2 0x10
PST R2 R1

LDI R1 0xFF ; buffer line to screen
LDI R2 0x04
PST R2 R1