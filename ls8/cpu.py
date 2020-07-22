"""CPU functionality."""

import sys


"""STEP 4: Add the `HLT` instruction definition to `cpu.py` so that you can refer to it by
name instead of by numeric value. """
HLT = 0b00000001

"""STEP 5: Add the `LDI` instruction definition to `cpu.py` so that you can refer to it by
name instead of by numeric value. """
LDI = 0b10000010

"""Step 6: Add the `PRN` instruction"""
PRN = 0b01000111

"""Step 8: Implement a Multiply and Print the Result"""
MUL = 0b10100010


class CPU:

    """Step 1: Add the constructor to `cpu.py`"""

    # Add list properties to the `CPU` class to hold 256 bytes of memory and 8
    # general-purpose registers.

    # Also add properties for any internal registers you need, e.g. `PC`.

    # Later on, you might do further initialization here, e.g. setting the initial
    # value of the stack pointer.

    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    """Step 2: Add RAM functions"""

    # In `CPU`, add method `ram_read()` and `ram_write()` that access the RAM inside
    # the `CPU` object.

    # `ram_read()` should accept the address to read and return the value stored
    # there.

    # `ram_write()` should accept a value to write, and the address to write it to.

    # Inside the CPU, there are two internal registers used for memory operations:
    # Memory Address Register (MAR) and Memory Data Register_(MDR).

    # The MAR contains the address that is being read or written to.
    # The MDR contains the data that was read or the data to write.
    #
    # You don't need to add the MAR or MDR to your `CPU` class, but they would make handy parameter names for
    # > `ram_read()` and `ram_write()`, if you wanted.

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        """Step 7: Un-hardcode the machine code"""

        if len(sys.argv) < 2:
            print("Please pass in two file names")

        file_name = sys.argv[1]

        try:
            with open(file_name) as file:
                for line in file:
                    # ignore whitespace + comments
                    split_line = line.split('#')[0]
                    command = split_line.strip()
                    if command == '':
                        continue

                    # use 2 for base 2 for binary
                    num = int(command, 2)

                    # store in memory
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    """Step 3: Implement the core of `CPU`'s `run()` method"""
    # This is the workhorse function of the entire processor.
    # It's the most difficult part to write.

    # It needs to read the memory address that's stored in register `PC`, and store
    # that result in `IR`, the _Instruction Register_. This can just be a local
    # variable in `run()`.

    # Some instructions requires up to the next two bytes of data _after_ the `PC` in
    # memory to perform operations on. Sometimes the byte value is a register number,
    # other times it's a constant value (in the case of `LDI`). Using `ram_read()`,
    # read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and
    # `operand_b` in case the instruction needs them.

    # Then, depending on the value of the opcode, perform the actions needed for the
    # instruction per the LS-8 spec. Maybe an `if-elif` cascade...? There are other
    # options, too.

    # After running code for any particular instruction, the `PC` needs to be updated
    # to point to the next instruction for the next iteration of the loop in `run()`.
    # The number of bytes an instruction uses can be determined from the two high bits
    # (bits 6-7) of the instruction opcode. See the LS-8 spec for details.

    def run(self):
        """Run the CPU."""
        # load program into memory
        self.load()

        running = True

        while running:
            IR = self.ram[self.pc]  # command

            # read bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            if IR == HLT:  # HALT
                running = False

            if IR == LDI:  # SAVE
                # save new value in specified register
                self.reg[operand_a] = operand_b
                self.pc += 3

            if IR == PRN:  # PRINT REG
                # Print numeric value stored in the given register.
                print(self.reg[operand_a])
                self.pc += 2

            if IR == MUL:  # MULTIPLY
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

        sys.exit()
