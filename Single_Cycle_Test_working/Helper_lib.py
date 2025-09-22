def read_file_to_list(filename):
    """
    Reads a text file and returns a list where each element is a line in the file.

    :param filename: The name of the file to read.
    :return: A list of strings, where each string is a line from the file.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Stripping newline characters from each line
        lines = [line.strip() for line in lines]
    return lines

        
 ###################################### 
 #####ERAY 

class Instruction:
    """
    Parses a 32-bit RISC-V R-type instruction from hex format.

    :param instruction: A string representing the 32-bit instruction in hex format (e.g., '00f50533')
    """
    def __init__(self, instruction):
        # Convert the hex instruction to a 32-bit binary string
        self.binary_instr = format(int(instruction, 16), '032b')

        # Extract fields according to RISC-V instruction format
        self.opcode = int(self.binary_instr[25:32], 2)     # bits [6:0]
        self.rd     = int(self.binary_instr[20:25], 2)     # bits [11:7]
        self.funct3 = int(self.binary_instr[17:20], 2)     # bits [14:12]
        self.rs1    = int(self.binary_instr[12:17], 2)     # bits [19:15]
        self.rs2    = int(self.binary_instr[7:12], 2)      # bits [24:20]
        self.funct7 = int(self.binary_instr[0:7], 2)       # bits [31:25]
        self.imm_i = int(self.binary_instr[0:12], 2)       #imm bits 

    def log(self, logger):
        logger.debug("****** Current RISC-V Instruction *********")
        logger.debug("Binary: %s", self.binary_instr)
        logger.debug("opcode : 0x%02X", self.opcode)
        logger.debug("rd     : x%d", self.rd)
        logger.debug("rs1    : x%d", self.rs1)
        logger.debug("rs2    : x%d", self.rs2)
        logger.debug("funct3 : %s", format(self.funct3, '03b'))
        logger.debug("funct7 : %s", format(self.funct7, '07b'))
        logger.debug("imm_i  : %d (0x%03X)", self.imm_i, self.imm_i & 0xFFF)

 ################################
"""
class Instruction:
    def __init__(self, instruction):
        # Convert the hex instruction to a 32-bit binary string
        self.binary_instr = format(int(instruction, 16), '032b')
        #Since python indexing is reversed to extract fields (31-index) for msb and (32-index) for lsb
        #For single bits do (31-index)
        self.Cond = int(self.binary_instr[0:4], 2)
        self.Op = int(self.binary_instr[4:6], 2)
        self.I = int(self.binary_instr[6], 2)
        self.cmd = int(self.binary_instr[7:11], 2)
        self.S = int(self.binary_instr[11], 2)
        self.Rn = int(self.binary_instr[12:16], 2)
        self.Rd = int(self.binary_instr[16:20], 2)
        self.rot = int(self.binary_instr[20:24], 2)
        self.imm8 = int(self.binary_instr[24:32], 2)
        self.shamt5 = int(self.binary_instr[20:25], 2)
        self.sh = int(self.binary_instr[25:27], 2)
        self.Rm = int(self.binary_instr[28:32], 2)
        self.Rs = int(self.binary_instr[20:24], 2)
        self.imm12 = int(self.binary_instr[20:32], 2)
        self.L = int(self.binary_instr[11], 2)
        if self.binary_instr[8] == '1':
            # Perform sign extension by flipping all bits and subtracting 1
            inverted_string = ''.join('0' if bit == '1' else '1' for bit in self.binary_instr[8:32])
            self.imm24 = -int(inverted_string, 2) - 1
        else:
            # It's a positive number, convert normally
            self.imm24 = int(self.binary_instr[8:32], 2)
        self.L_branch = int(self.binary_instr[7], 2)
        
    def log(self,logger):
        logger.debug("****** Current Instruction *********")
        logger.debug("Binary string:%s", self.binary_instr)
        if(self.binary_instr[4:28]=="000100101111111111110001"):
            logger.debug("Operation type BX")
            logger.debug("Rm: %d",self.Rm)
        elif(self.Op == 0):
            logger.debug("Operation type Data Processing")
            logger.debug("cond:%s ",'{0:X}'.format(self.Cond))
            logger.debug("Immediate bit:%d ",self.I)
            logger.debug("cmd:%s ",'{0:X}'.format(self.cmd))
            logger.debug("Set bit:%d ",self.S)
            logger.debug("Rn:%d \t Rd:%d ",self.Rn,self.Rd)
            if(self.I==1):
                logger.debug("rot:%d \t imm8:%d ",self.rot,self.imm8)
            else:
                logger.debug("shamt5:%d \t sh:%d \t Rm:%d ",self.shamt5,self.sh,self.Rm)
        elif(self.Op == 1):
            logger.debug("Operation type Memory")
            logger.debug("Load bit:%d ",self.L)
            logger.debug("Rn:%d \t Rn:%d ",self.Rn,self.Rd)
            logger.debug("imm12:%d",self.imm12)
        elif(self.Op==2):
            logger.debug("Operation type Branch (except Bx)")
            logger.debug("Link bit:%d ",self.L_branch)
            logger.debug("imm24:%d",self.imm24)

"""
def interpret_as_signed(binary_str, width):
    value = int(binary_str)
    if value >= 2**(width - 1):
        value -= 2**width
    return value

def arithmetic_shift_right(num, amount, width):
    if num < 0:         #arithmatic shift right funct.
        num += (1 << width)       
        num >>= amount
        num |= ((1 << amount) - 1) << (width - amount) 
    else:
        num >>= amount
    return num & ((1 << width) - 1)
def logical_shift_right(val, amount, width):
    max_val = (1 << width) - 1
    val = val & max_val        
    result = val >> amount     
    result &= max_val >> amount  
    return result
    

def get_unsigned_32bit(num):
    return num & 0xFFFFFFFF 
def get_unsigned_16bit(num):
    return num & 0x0000FFFF 

def get_unsigned_8bit(num):
    return num & 0x000000FF 
def rotate_right(value, shift, n_bits=32):
    """
    Rotate `value` to the right by `shift` bits.

    :param value: The integer value to rotate.
    :param shift: The number of bits to rotate by.
    :param n_bits: The bit-width of the integer (default 32 for standard integer).
    :return: The value after rotating to the right.
    """
    shift %= n_bits  # Ensure the shift is within the range of 0 to n_bits-1
    return (value >> shift) | (value << (n_bits - shift)) & ((1 << n_bits) - 1)

def shift_helper(value, shift,shift_type, n_bits=32):
    shift %= n_bits  # Ensure the shift is within the range of 0 to n_bits-1
    if shift_type == 0:
        return (value << shift) % 0x100000000
    elif shift_type == 1:
        return (value >> shift) % 0x100000000
    elif shift_type == 2:
        if (value & 0x80000000) != 0:
            filler = (0xFFFFFFFF >> (n_bits - shift)) << (n_bits - shift)
            return ((value >> shift) | filler) % 0x100000000
        else:
            return (value >> shift) % 0x100000000
    elif shift_type == 3:
        return rotate_right(value, shift, n_bits)

    """
    match shift_type:
        case 0:
            return (value  << shift)% 0x100000000
        case 1:
            return (value  >> shift) % 0x100000000
        case 2:
            if((value & 0x80000000)!=0):
                    filler = (0xFFFFFFFF >> (n_bits-shift))<<((n_bits-shift))
                    return ((value  >> shift)|filler) % 0x100000000
            else:
                return (value  >> shift) % 0x100000000
        case 3:
            return rotate_right(value,shift,n_bits)
    """
        
def reverse_hex_string_endiannes(hex_string):  
    reversed_string = bytes.fromhex(hex_string)
    reversed_string = reversed_string[::-1]
    reversed_string = reversed_string.hex()        
    return  reversed_string
class ByteAddressableMemory:
    def __init__(self, size=8192):
        self.size = size
        self.memory = bytearray(size)  # Initialize memory as a bytearray of the given size

    def read(self, address):
        if address < 0 or address + 4 > self.size:
            raise ValueError("Invalid memory address or length")
        return_val = bytes(self.memory[address : address + 4])
        return_val = return_val[::-1]
        return return_val

    def write(self, address, data, size):
        if address < 0 or address + size > self.size:
            raise ValueError("Invalid memory address or data length")
        data_bytes = data.to_bytes(size, byteorder='little')
        self.memory[address : address + size] = data_bytes
        


