import tkinter
import math
from .port import PORT

DIMENSIONS = "40x20"

_mode = 0x0
_function = 0x0
_x1 = 0x0
_x2 = 0x0
_y1 = 0x0
_y2 = 0x0
_z1 = 0x0
_z2 = 0x0

_root = None

class CHARACTER(PORT):

    def store(value: int) -> None:
        print(chr(value), end="")

class X1(PORT):

    def store(value: int) -> None:
        global _x1; _x1 = value

class X2(PORT):

    def store(value: int) -> None:
        global _x2; _x2 = value

class Y1(PORT):

    def store(value: int) -> None:
        global _y1; _y1 = value

class Y2(PORT):

    def store(value: int) -> None:
        global _y2; _y2 = value

class Z1(PORT):

    def store(value: int) -> None:
        global _z1; _z1 = value

class Z2(PORT):

    def store(value: int) -> None:
        global _z2; _z2 = value

class MODE(PORT):

    def store(value: int) -> None:
        match value:
            case 0x00: # 3x5 text
                pass
            case 0x01: # 5x7 text
                pass
            case 0x02: # pixel mode - use X1, Y1
                _root = tkinter.Tk()
                _root.title("Pixel Mode")
                _root.geometry(DIMENSIONS)
                _root.resizable(False, False)
                _root.configure(bg="black")
                _root.mainloop()
            case 0x03: # 2d mode - use X1, X2, Y1, Y2
                _root = tkinter.Tk()
                _root.title("2D Mode")
                _root.geometry(DIMENSIONS)
                _root.resizable(False, False)
                _root.configure(bg="black")
                _root.mainloop()
            case 0x04: # 3d mode - use X1, X2, Y1, Y2, Z1, Z2
                raise NotImplementedError("3d mode not implemented")
            case _:
                raise NotImplementedError(f"GPU mode {value} not implemented")
        _mode = value

class FUNCTION(PORT):

    def store(value: int) -> None:
        global _x1, _x2, _y1, _y2, _z1, _z2, _root
        match value:
            case 0x00: # clear screen
                if _root is None:
                    raise RuntimeError(f"GPU function {value} requires a set mode")
                _root.delete("all")
            case 0x01: # clear registers
                pass # emulator just draws screen with tkinter so there's no registers to clear
            case 0x02: # clear memory
                pass # same as above
            case 0x03: # draw pixel/line to buffer
                match _mode:
                    case 0x02: # pixel mode
                        if _root is None:
                            raise RuntimeError(f"GPU function {value} requires a set mode")
                        _root.create_rectangle(_x1, _y1, _x1, _y1, fill="orange")
                    case 0x03: # 2d mode
                        if _root is None:
                            raise RuntimeError(f"GPU function {value} requires a set mode")
                        _root.create_line(_x1, _y1, _x2, _y2, fill="orange")
                    case 0x04: # 3d mode
                        raise NotImplementedError("3d mode not implemented")
                        
            case 0x04: # buffer screen
                pass
            case 0xFF: # disable
                pass
            case _:
                raise NotImplementedError(f"GPU function {value} not implemented")
        _function = value