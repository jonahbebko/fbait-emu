import os
from port import PORT

REGISTERS = [0] * 8
MEMORY = [0] * 32
PROM = [0] * 32
PORTS = [PORT() for _ in range(256)]
FLAGS = {'ZERO': 0, 'COUT': 0, 'MSB': 0}
SETTINGS = {}
PC = 0

files = [i[:-3] for i in os.listdir() if i.endswith(".fb")]
if len(files) == 0:
    raise Exception("no programs found")
print("files found:", ", ".join(files))
a = input("select program to run: ")

try:
    assembly_file = open(f"{a}.fb", 'r')
except:
    raise Exception(f'program {a}.fb not found')
program: list[str] = assembly_file.readlines()
assembly_file.close()

for index, line in enumerate(program):
    PROM[index] = line.strip()

class DECIMAL_OUTPUT(PORT):

    def load(self) -> int:
        return 0

    def store(self, value: int) -> None:
        print(value)

class INPUT(PORT):
    
    def load(self) -> int:
        return int(input('hex > 0x'), 16)

    def store(self, value: int) -> None:
        pass

PORTS[0xF3] = INPUT()
PORTS[0xF4] = DECIMAL_OUTPUT()

class CPU:

    def __init__(self):
        self.registers = REGISTERS
        self.memory = MEMORY
        self.prom = PROM
        self.ports = PORTS
        self.flags = FLAGS
        self.pc = PC
        self.running = True
        self.branched = False
    
    def decode(self, instruction: str) -> tuple[str, str]:
        split_instruction = instruction.split(" ")
        opcode = split_instruction[0]
        operands = split_instruction[1:]
        return (opcode, operands)
    
    def execute(self, opcode: str, operands: str) -> None:
        match opcode:
            case '00000': self.NOP(operands)
            case '00001': self.MOV(operands)
            case '00010': self.LDI(operands)
            case '00011': self.LOD(operands)
            case '00100': self.LDP(operands)
            case '00101': self.STR(operands)
            case '00110': self.STP(operands)
            case '00111': self.ADD(operands)
            case '01000': self.SUB(operands)
            case '01001': self.INC(operands)
            case '01010': self.DEC(operands)
            case '01011': self.AND(operands)
            case '01100': self.ORR(operands)
            case '01101': self.XOR(operands)
            case '01110': self.NOT(operands)
            case '01111': self.RSH(operands)
            case '10000': self.LSH(operands)
            case '10001': self.ROT(operands)
            case '10010': self.CMP(operands)
            case '10011': self.BRH(operands)
            case '10100': self.PCS(operands)
            case '10101': self.PLD(operands)
            case '10110': self.PST(operands)
            case '11110': self.SET(operands)
            case '11111': self.KYS(operands)
            case _:
                raise NotImplementedError(f'opcode {opcode} not found')
        
    def update_flags(self, result: int) -> None:
        self.flags["ZERO"] = result & 0xFF == 0
        self.flags["COUT"] = result & 0x100 != 0
        self.flags["MSB"] = result & 0x80 != 0

    def step(self) -> None:
        if self.branched:
            self.branched = False
        else:
            self.pc += 1
        instruction = self.prom[self.pc]
        opcode, operands = self.decode(instruction)
        try:
            self.execute(opcode, operands)
        except IndexError as e:
            print(f"IndexError: {e}\nmost likely caused by invalid register (>7)")
            exit(1)
        except Exception as e:
            print(f"Exception: {e}")
            exit(1)
    
    def run(self) -> None:
        while self.running:
            self.step()
        else:
            print('cpu halted')

    def NOP(self, operands: str) -> None:
        halt = operands[0]
        if halt == '1':
            self.running = False

    def MOV(self, operands: str) -> None:
        regs = [operands[0], operands[1]]
        self.registers[int(regs[0], 2)] = self.registers[int(regs[1], 2)]
    
    def LDI(self, operands: str) -> None:
        reg = operands[0]
        imm = operands[1]
        self.registers[int(reg, 2)] = int(imm, 2)
    
    def LOD(self, operands: str) -> None:
        reg = operands[0]
        addr = operands[1]
        self.registers[int(reg, 2)] = self.memory[int(addr, 2)]
    
    def LDP(self, operands: str) -> None:
        regs = [operands[0], operands[1]]
        if int(regs[1], 2) > len(MEMORY):
            raise IndexError(f'memory address {regs[1]} is out of bounds')
        self.registers[int(regs[0], 2)] = self.memory[self.registers[int(regs[1], 2)]]
    
    def STR(self, operands: str) -> None:
        reg = operands[0]
        addr = operands[1]
        self.memory[int(addr, 2)] = self.registers[int(reg, 2)]
    
    def STP(self, operands: str) -> None:
        regs = [operands[0], operands[1]]
        if int(regs[1], 2) > len(MEMORY):
            raise IndexError(f'memory address {regs[1]} is out of bounds')
        self.memory[self.registers[int(regs[1], 2)]] = self.registers[int(regs[0], 2)]
    
    def ADD(self, operands: str) -> None:
        regs = [operands[0], operands[1], operands[2]]
        if len(operands) == 3:
            update = '0'
        else:
            update = operands[3]
        self.registers[int(regs[0], 2)] = self.registers[int(regs[1], 2)] + self.registers[int(regs[2], 2)]
        if update == '1':
            self.update_flags(self.registers[int(regs[0], 2)])
    
    def SUB(self, operands: str) -> None:
        regs = [operands[0], operands[1], operands[2]]
        if len(operands) == 3:
            update = '0'
        else:
            update = operands[3]
        self.registers[int(regs[0], 2)] = self.registers[int(regs[1], 2)] - self.registers[int(regs[2], 2)]
        if update == '1':
            self.update_flags(self.registers[int(regs[0], 2)])
    
    def INC(self, operands: str) -> None:
        reg = operands[0]
        imm = operands[1]
        self.registers[int(reg, 2)] += int(imm, 2)
    
    def DEC(self, operands: str) -> None:
        reg = operands[0]
        imm = operands[1]
        self.registers[int(reg, 2)] -= int(imm, 2)
    
    def AND(self, operands: str) -> None:
        regs = [operands[0], operands[1], operands[2]]
        negate = operands[9]
        if negate == '1':
            self.registers[int(regs[0], 2)] = ~(self.registers[int(regs[1], 2)] & self.registers[int(regs[2], 2)])
        else:
            self.registers[int(regs[0], 2)] = self.registers[int(regs[1], 2)] & self.registers[int(regs[2], 2)]
    
    def ORR(self, operands: str) -> None:
        regs = [operands[0], operands[1], operands[2]]
        negate = operands[9]
        if negate == '1':
            self.registers[int(regs[0], 2)] = ~(self.registers[int(regs[1], 2)] | self.registers[int(regs[2], 2)])
        else:
            self.registers[int(regs[0], 2)] = self.registers[int(regs[1], 2)] | self.registers[int(regs[2], 2)]
    
    def XOR(self, operands: str) -> None:
        regs = [operands[0], operands[1], operands[2]]
        negate = operands[3]
        if negate == '1':
            self.registers[int(regs[0], 2)] = ~(self.registers[int(regs[1], 2)] ^ self.registers[int(regs[2], 2)])
        else:
            self.registers[int(regs[0], 2)] = self.registers[int(regs[1], 2)] ^ self.registers[int(regs[2], 2)]
    
    def NOT(self, operands: str) -> None:
        reg = operands[0]
        self.registers[int(reg, 2)] = ~self.registers[int(reg, 2)]
    
    def RSH(self, operands: str) -> None:
        reg = operands[0]
        amt = operands[1]
        self.registers[int(reg, 2)] >>= int(amt, 2)
    
    def LSH(self, operands: str) -> None:
        reg = operands[0]
        amt = operands[1]
        self.registers[int(reg, 2)] <<= int(amt, 2)
    
    def ROT(self, operands: str) -> None:
        reg = operands[0]
        amt = operands[1]
        self.registers[int(reg, 2)] = (self.registers[int(reg, 2)] << int(amt, 2)) | (self.registers[int(reg, 2)] >> (8 - int(amt, 2)))
    
    def CMP(self, operands: str) -> None:
        regs = [operands[0], operands[1]]
        compare = self.registers[int(regs[0], 2)] + (self.registers[int(regs[1], 2)] ^ 0xFF) + 1
        self.update_flags(compare)
    
    def BRH(self, operands: str) -> None:
        cond = operands[0]
        addr = self.registers[int(operands[1], 2)]
        match cond:
            case "000": # unconditional
                self.pc = addr
            case "001": # zero
                if self.flags["ZERO"]: self.pc = addr
            case "010": # not zero
                if not self.flags["ZERO"]: self.pc = addr
            case "011": # carry
                if self.flags["COUT"]: self.pc = addr
            case "100": # unsigned greater
                if self.flags["COUT"] and not self.flags["ZERO"]: self.pc = addr
            case "101": # unsigned greater or equal
                if self.flags["COUT"]: self.pc = addr
            case "110": # unsigned less
                if not self.flags["COUT"]: self.pc = addr
            case "111": # unsigned less or equal
                if not self.flags["COUT"] or self.flags["ZERO"]: self.pc = addr
            case _:
                raise ValueError(f'invalid condition {cond}')
        if self.pc == addr:
            self.branched = True
    
    def PCS(self, operands: str) -> None:
        reg = operands[0]
        self.registers[int(reg, 2)] = self.pc
    
    def PLD(self, operands: str) -> None:
        reg = operands[0]
        port = operands[1]
        self.registers[int(reg, 2)] = self.ports[int(port, 2)].load()
    
    def PST(self, operands: str) -> None:
        reg = operands[0]
        port = operands[1]
        self.ports[int(port, 2)].store(self.registers[int(reg, 2)])
    
    def SET(self, operands: str) -> None:
        setting = operands[0]
        match setting:
            case "000": # nop
                pass
            case _:
                raise ValueError(f'invalid setting {setting}')
    
    def KYS(self, operands: str) -> None:
        exit("cpu blew up :(")

cpu = CPU()
cpu.run()
