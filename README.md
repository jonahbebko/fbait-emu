[![Badge](https://img.shields.io/badge/link-996.icu-%23FF4D5B.svg?style=flat-square)](https://996.icu/#/en_US)

# fbait-emu
Emulator written in Python for my 8-bit "FURRYBAIT" CPU built entirely in Minecraft.
Tested and run only with `python3.11.4` but should work with any version of `python3`.

## Files
`assembly.txt` - code for CPU written in custom assembly

`isa.txt` - text representation of the CPU's instruction set architecture (ISA), in `instruction:opcode:oplength,oplength,oplength` format

`machinecode.txt` - assembled binary output to be read and executed by CPU

`assembler.py` - custom assembler which converts assembly into machine code

`emulator.py` - the CPU emulator

`port.py` - definition for the base PORT class

## Programming in Assembly

The ISA for FURRYBAIT can be found [here.](https://docs.google.com/spreadsheets/d/1BiFGfeyPMsWl56HnLYbaD-BoIZvfuITvZX8m75RIMmI/edit?usp=sharing)

An example Fibonacci program can be found in `assembly.txt` which prints the first 12 fibonacci numbers (less than 256) then halts.

Registers are prefixed with `R` like `R0` and `R4`.

Immediates and literals can be written in binary like `0b110`, hex like `0x3F`, or decimal for immediates up to and including `255`.

Comments can be written either in-line or whole-line with a semicolon. **Jump addresses ignore commented lines** as the machine code doesn't include comments.

## Extra Notes

FURRYBAIT will automatically detect out-of-range registers at assembletime and memory addresses at runtime.

A URCL compiler will eventually be implemented.

## Contact

If you must contact me, my email is jonahbebko@outlook.com.
