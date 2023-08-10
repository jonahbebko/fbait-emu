import random
from .port import PORT
from .colors import FG, BG

class HEX_OUTPUT(PORT):

    def store(value: int) -> None:
        bin_value = f"{value:08b}"
        bin_value = [FG["green"] + bit + FG["reset"] if bit == "1" else FG["red"] + bit + FG["reset"] for bit in bin_value]
        print(f"{value:03d} | 0x{value:02X} | 0b{''.join(bin_value)}")

class BINARY_OUTPUT(PORT):

    def store(value: int) -> None:
        print("".join([FG["green"] + bit + FG["reset"] if bit == "1" else FG["red"] + bit + FG["reset"] for bit in f'{value:08b}']))

class INPUT(PORT):
    
    def load() -> int:
        return int(input('hex > 0x'), 16)

class RANDOM_NUMBER(PORT):

    def load() -> int:
        return random.randint(0, 255)