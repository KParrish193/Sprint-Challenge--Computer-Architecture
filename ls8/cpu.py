"""CPU functionality."""

import sys

# instructions list
LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
RET = 0b00010001
CALL = 0b01010000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        # memory that has 256 bytes of memory
        # 1 index is 1 byte(8bits)
        self.ram = [0] * 256

        # registers r0-r7
        # r5,r6,r7 are reserved
        self.register = [0] * 8

        # program counter (pc) starts at 0
        self.program_counter = 0
        self.running = False

        self.stack_pointer = 7
        # branch table
        self.ir_table = {
            LDI: self.LDI,
            PRN: self.PRN,
            HLT: self.HLT,
            ADD: self.ADD,
            MUL: self.MUL,
            PUSH: self.PUSH,
            POP: self.POP,
            RET: self.RET,
            CALL: self.CALL
        }

    def load(self, filename):
        """Load a program into memory."""

        # open file and store instructions to memory
        with open(f"examples/{filename}") as f:
            address = 0

            for line in f:
                line = line.split("#")
                line = line[0].strip()

                if line == "":
                    continue

                self.ram_write(int(line, 2), address)

                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.program_counter,
            #self.fl,
            #self.ie,
            self.ram_read(self.program_counter),
            self.ram_read(self.program_counter + 1),
            self.ram_read(self.program_counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()


    def run(self):
        """Run the CPU."""
        SP = self.stack_pointer
        # initialize value at register[7] to be 0
        self.register[SP] = 0xf4
        
        self.running = True
        # while running:
        while self.running:
            # instruction register
            IR = self.ram[self.program_counter]
            self.ir_table[IR]()

    def ram_read(self, MAR):
        # MAR - address being read
        # MDR - value that was read
        MDR = self.ram[MAR]

        return MDR

    def ram_write(self, MDR, MAR):
        # MAR - address being written to
        # MDR - value to write
        self.ram[MAR] = MDR

    def LDI(self):
        operand_a = self.ram_read(self.program_counter + 1)
        operand_b = self.ram_read(self.program_counter + 2)

        self.register[operand_a] = operand_b

        self.program_counter += 3
    
    # Print  
    def PRN(self):
        operand_a = self.ram_read(self.program_counter + 1)
        value = self.register[operand_a]

        print(value)

        self.program_counter += 2

    # Halt
    def HLT(self):
        self.running = False

    # Add
    def ADD(self):
        operand_a = self.ram_read(self.program_counter + 1)
        operand_b = self.ram_read(self.program_counter + 2)

        self.alu("ADD", operand_a, operand_b)

        self.program_counter += 3

    def MUL(self):
        operand_a = self.ram_read(self.program_counter + 1)
        operand_b = self.ram_read(self.program_counter + 2)

        self.alu("MUL", operand_a, operand_b)

        self.program_counter += 3

    def PUSH(self):
        sp = self.stack_pointer
        self.register[sp] -= 1

        reg_num = self.ram_read(self.program_counter + 1)
        value = self.register[reg_num]

        stack_addr = self.register[sp]
        self.ram_write(value, stack_addr)

        self.program_counter += 2

    def POP(self):
        # this is where we'll store the value at self.ram[sp]
        sp = self.stack_pointer
        stack_addr = self.register[self.stack_pointer]

        reg_num = self.ram_read(self.program_counter + 1)
        value = self.ram_read(stack_addr)

        self.register[reg_num] = value
        self.register[sp] += 1
        self.program_counter += 2

    def CALL(self):
        #  Where we're going to RET to
        return_address = self.program_counter + 2
        
        # Push onto the stack
        self.register[self.stack_pointer] -= 1
        self.ram_write(return_address, self.register[self.stack_pointer])

        # Get the address to call
        reg_num = self.ram_read(self.program_counter + 1)
        subroutine_address = self.register[reg_num]
        
        # Call it
        self.program_counter = subroutine_address

    def RET(self):
        # Pop the value from the top of the stack and store it in the `PC`.
        self.program_counter = self.ram_read(self.register[self.stack_pointer])
        self.register[self.stack_pointer] += 1






"""
# PUSH
What's stored in r7 is the address in ram where we want to store a value
decrement sp so the next time we push, we put the value on a different addres, one below the first one

we grab the value we want to store by reading  the PUSH instruction so the next index in ram is the value
we write that value in the address stored in register 7


# POP
we grab value at register 7, which is the address in memory we want to grab

ram[self.reg[sp]] is the value we want to pop 


"""