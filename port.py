class PORT:
    
    def load(self) -> int:
        print("PORT: load")

    def store(self, value: int) -> None:
        print(f"PORT: {value}")

class DECIMAL_OUTPUT:

    def load(self) -> int:
        return 0

    def store(self, value: int) -> None:
        print(f"{value} | 0x{value:02X} | 0b{value:08b}")

class INPUT:
    
    def load(self) -> int:
        return int(input('hex > 0x'), 16)

    def store(self, value: int) -> None:
        pass