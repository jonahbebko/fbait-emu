import re, os

INSTRUCTIONS = {}
LENGTHS = {}
ASSEMBLED = []

files = [i[:-4] for i in os.listdir() if i.endswith(".asm")]
if len(files) == 0:
    raise Exception("failed: no assembly files found")
print("files found:", ", ".join(files))
a = input("select file to assemble: ")

isa_file = open("isa.txt", "r")
isa = isa_file.readlines()
isa_file.close()

try:
    assembly_file = open(f"{a}.asm", "r")
except:
    raise Exception(f"failed: file {a}.asm not found")
assembly = assembly_file.readlines()
assembly_file.close()

output = open(f"{a}.fb", "w")

for index, line in enumerate(isa):
    spl = line.split(":")
    INSTRUCTIONS[spl[0]] = spl[1]
    LENGTHS[spl[1]] = [int(i.replace("\n", "")) for i in spl[2].split(",")]

for index, line in enumerate(assembly):

    if not line.strip(): continue
    if line.startswith(";"):
        continue
    elif line.__contains__(";"):
        line = line.split(";")[0].strip()

    assembled_line = []
    symbols = line.split(" ")

    if symbols[0] not in INSTRUCTIONS.keys():
        raise Exception(f"failed: instruction {symbols[0]} not found in ISA")
    
    opcode = INSTRUCTIONS[symbols[0]]
    operands = symbols[1:]

    if len(operands) != len(LENGTHS[opcode]) and symbols[0] not in ["NOP", "ADD", "SUB", "AND", "ORR", "XOR"]:
        raise Exception(f"failed: instruction {opcode} expects {len(LENGTHS[opcode])} operands, got {len(operands)}")

    assembled_line.append(opcode)

    for oindex, operand in enumerate(operands):

        if not operand: continue
        operand = operand.strip()

        binary_operand = ""

        if len(operand.replace("0b", "").replace("0x", "")) > LENGTHS[opcode][oindex]:
            raise Exception(f"failed: operand {operand} is too long for {opcode}")

        if re.match(r"[rR]\d*", operand):
            # register, 3 bits
            if int(operand[1:]) > 7:
                raise Exception(f"failed: register {operand} should not be greater than 7")
            binary_operand = bin(int(operand[1:]))[2:].zfill(LENGTHS[opcode][oindex])

        elif re.match(r"0x[0-9a-fA-F]{1,2}", operand):
            # hex literal, 8 bits
            if len(operand) == 3:
                operand = "0x0" + operand[2]
            binary_operand = bin(int(operand[2:], 16))[2:].zfill(LENGTHS[opcode][oindex])

        elif re.match(r"0b[01]{1,8}", operand):
            # binary literal, 8 bits
            binary_operand = operand[2:].zfill(LENGTHS[opcode][oindex])

        elif re.match(r"\d{1,3}", operand):
            # decimal literal, 8 bits
            binary_operand = bin(int(operand))[2:].zfill(LENGTHS[opcode][oindex])
        
        else:
            raise Exception(f"failed: type of operand '{operand}' unknown")

        assembled_line.append(binary_operand)
    
    ASSEMBLED.append(" ".join(assembled_line))

if len(ASSEMBLED) > 32:
    print(f"warn: program is too long ({len(ASSEMBLED)} instructions), max is 32")

print("program assembled successfully")

output.write("\n".join(ASSEMBLED))
output.close()