_COLORS = {
    "red": "\033[1;31m",
    "green": "\033[1;32m",
    "reset": "\033[0;0m",
}

class PORT:
    
    def load(self) -> int:
        print("PORT: load")

    def store(self, value: int) -> None:
        print(f"PORT: {value}")

class DECIMAL_OUTPUT:

    def load(self) -> int:
        return 0

    def store(self, value: int) -> None:
        bin_value = f"{value:08b}"
        bin_value = [_COLORS["green"] + bit + _COLORS["reset"] if bit == "1" else _COLORS["red"] + bit + _COLORS["reset"] for bit in bin_value]
        print(f"{value:03d} | 0x{value:02X} | 0b{''.join(bin_value)}")

class INPUT:
    
    def load(self) -> int:
        return int(input('hex > 0x'), 16)

    def store(self, value: int) -> None:
        pass