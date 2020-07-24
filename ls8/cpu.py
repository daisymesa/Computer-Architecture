"""CPU functionality."""

import sys


"""STEP 4: Add the `HLT` instruction definition to `cpu.py` so that you can refer to it by
name instead of by numeric value. """
HLT = 0b00000001

"""STEP 5: Add the `LDI` instruction definition to `cpu.py` so that you can refer to it by
name instead of by numeric value. """
LDI = 0b10000010

"""STEP 6: Add the `PRN` instruction"""
PRN = 0b01000111

"""STEP 8: Implement a Multiply and Print the Result"""
MUL = 0b10100010

"""Step 10: Implement System Stack"""
PUSH = 0b01000101
POP = 0b01000110

''' ### SPRINT CHALLENGE ### '''
# Add the CMP instruction and equal flag to your LS-8.
#  Add the JMP instruction.
#  Add the JEQ and JNE instructions.
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:

    """STEP 1: Add the constructor to `cpu.py`"""

    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # registers
        self.ram = [0] * 256  # memory
        self.pc = 0  # pc
        self.SP = 7  # stack pointer
        self.FL = 0

    """STEP 2: Add RAM functions"""

    # In `CPU`, add method `ram_read()` and `ram_write()` that access the RAM inside
    # the `CPU` object.

    # The MAR contains the ADDRESS that is BEING read or written to. (Memory Address Register)
    # The MDR contains the DATA that WAS read or the data TO write. (Memory Data Register)

    # `ram_write()` should accept a value to write, and the address to write it to.
    def ram_read(self, MAR):
        return self.ram[MAR]

    # `ram_read()` should accept the address to read and return the value stored there.
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

        """STEP 7: Un-hardcode the machine code"""

        if len(sys.argv) < 2:
            print("Please pass in two file names")

        file_name = sys.argv[1]

        try:
            with open(file_name) as f:
                for line in f:
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

    """STEP 3: Implement the core of `CPU`'s `run()` method"""

    def run(self):
        """Run the CPU."""
        # load program into memory
        self.load()

        # running = True

        while self.ram[self.pc] != HLT:
            IR = self.ram[self.pc]  # command

            # read bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            # if IR == HLT:  # HALT
            #     running = False

            if IR == LDI:  # SAVE
                # save new value in specified register
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == PRN:  # PRINT REG
                # Print numeric value stored in the given register.
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == MUL:  # MULTIPLY
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:  # PUSH
                # get the register number
                register = operand_a

                # decrement register number
                self.reg[self.SP] -= 1

                # get the value from the given register
                value = self.reg[register]

                # put the value at the stack pointer address
                stack_pointer = self.reg[self.SP]
                self.ram[stack_pointer] = value

                # increment the PC
                self.pc += 2

            elif IR == POP:  # POP
                # get the register number
                register = operand_a

                # use stack pointer to get the value
                stack_pointer = self.reg[self.SP]
                value = self.ram[stack_pointer]

                # put the value into the given register
                self.reg[register] = value

                # increment our stack pointer
                self.reg[self.SP] += 1

                # increment our PC
                self.pc += 2

            # CMP
            # Compare the values in two registers.

            # * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.

            # * If registerA is less than registerB, set the Less-than `L` flag to 1,
            #   otherwise set it to 0.

            # * If registerA is greater than registerB, set the Greater-than `G` flag
            #   to 1, otherwise set it to 0.
            elif IR == CMP:
                if (self.reg[operand_a] == self.reg[operand_b]) == True:
                    self.FL = 1

                self.pc += 3

            # JMP - Jump to the address stored in the given register.  Set the PC to the address stored in the given register.
            elif IR == JMP:
                self.pc = self.reg[operand_a]

            # JEQ - If equal flag is set (true), jump to the address stored in the given register.
            elif IR == JEQ:
                if self.FL == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            # JNE - If E flag is clear (false, 0), jump to the address stored in the given register.
            elif IR == JNE:
                if self.FL == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

        sys.exit()


"""Step 9: Beautify your `run()` loop"""

""" ================================================== """


# class CPU2:
#     def __init__(self):
#         self.reg = [0] * 8  # registers
#         self.ram = [0] * 256  # memory
#         self.pc = 0  # pc
#         self.SP = 7  # stack pointer
#         self.branchtable = {}
#         self.branchtable[LDI] = self.handle_ldi     # SAVE
#         self.branchtable[PRN] = self.handle_prn     # PRINT REG
#         # self.branchtable[MUL] = self.handle_mul     # MULTIPLY
#         self.branchtable[PUSH] = self.handle_push   # PUSH
#         self.branchtable[POP] = self.handle_pop     # POP
#         self.branchtable[HLT] = self.handle_hlt     # HLT

#     # `ram_write()` should accept a value to write, and the address to write it to.
#     def ram_read(self, MAR):
#         return self.ram[MAR]

#     # `ram_read()` should accept the address to read and return the value stored there.
#     def ram_write(self, MDR, MAR):
#         self.ram[MAR] = MDR

#     def load(self):
#         address = 0
#         running = True

#         if len(sys.argv) < 2:
#             print("Please pass in two file names")

#         file_name = sys.argv[1]

#         try:
#             with open(file_name) as f:
#                 for line in f:
#                     # ignore whitespace + comments
#                     split_line = line.split('#')[0]
#                     command = split_line.strip()
#                     if command == '':
#                         continue

#                     # use 2 for base 2 for binary
#                     num = int(command, 2)

#                     # store in memory
#                     self.ram[address] = num
#                     address += 1

#         except FileNotFoundError:
#             print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
#             sys.exit()

#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]
#         elif op == "MUL":
#             self.reg[reg_a] *= self.reg[reg_b]
#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             # self.fl,
#             # self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

#     # SAVE
#     def handle_hlt(self, a, b):
#         "handle_hlt"
#         sys.exit()

#     def handle_ldi(self, a, b):
#         "handle_ldi"
#         self.reg[a] = b
#         self.pc += 3

#     # PRINT REG
#     def handle_prn(self, a, b):
#         "handle_prn"
#         print(self.reg[a])
#         self.pc += 2

#     # MULTIPLY
#     def handle_mul(self, a, b):
#         "handle_mul"
#         self.alu("MUL", a, b)
#         self.pc += 3

#     # PUSH
#     def handle_push(self, a, b):
#         "handle_push"
#         # get the register number
#         register = a

#         # decrement register number
#         self.reg[self.SP] -= 1

#         # get the value from the given register
#         value = self.reg[register]

#         # put the value at the stack pointer address
#         stack_pointer = self.reg[self.SP]
#         self.ram[stack_pointer] = value

#         self.pc += 2

#     # POP
#     def handle_pop(self, a, b):
#         "handle_pop"
#         # get the register number
#         register = a

#         # use stack pointer to get the value
#         stack_pointer = self.reg[self.SP]
#         value = self.ram[stack_pointer]

#         # put the value into the given register
#         self.reg[register] = value

#         # increment our stack pointer
#         self.reg[self.SP] += 1

#         self.pc += 2

#     def run(self):
#         self.load()

#         IR = self.ram[self.pc]  # command
#         # a = self.ram[self.pc + 1]
#         # b = self.ram[self.pc + 2]
#         # self.branchtable[IR](a, b)

#         while IR != HLT:
#             IR = self.ram[self.pc]  # command

#             a = self.ram[self.pc + 1]  # operand_a
#             b = self.ram[self.pc + 2]  # operand_b

#             # IR = LDI
#             # self.branchtable[IR](a, b)

#             IR = PRN
#             # self.branchtable[IR](a)
#             self.branchtable[IR](a, b)

#             if IR == HLT:
#                 running = False

#             if IR == LDI:  # SAVE
#                 self.branchtable[IR](a, b)
#                 # self.pc += 3

#             elif IR == PRN:  # PRINT REG
#                 self.branchtable[IR](a, b)
#                 # self.pc += 2

#             elif IR == MUL:  # MULTIPLY
#                 self.alu("MUL", a, b)
#                 # self.pc += 3

#             elif IR == PUSH:
#                 self.branchtable[IR](a, b)
#                 # self.pc += 2

#             elif IR == POP:
#                 self.branchtable[IR](a, b)
#                 # self.pc += 2

#         sys.exit()


# # class Foo:

# #     def __init__(self):
# #         # Set up the branch table
# #         self.branchtable = {}
# #         self.branchtable[OP1] = self.handle_op1
# #         self.branchtable[OP2] = self.handle_op2

# #     def handle_op1(self, a):
# #         print("op 1: " + a)

# #     def handle_op2(self, a):
# #         print("op 2: " + a)

# #     def run(self):
# #         # Example calls into the branch table
# #         ir = OP1
# #         self.branchtable[ir]("foo")

# #         ir = OP2
# #         self.branchtable[ir]("bar")


# # # # c = Foo()
# # # # c.run()
