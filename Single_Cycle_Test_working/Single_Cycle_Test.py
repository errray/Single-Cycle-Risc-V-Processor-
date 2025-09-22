# ==============================================================================
# Authors:              Doğu Erkan Arkadaş
#
# Cocotb Testbench:     For Single Cycle ARM Laboratory
#
# Description:
# ------------------------------------
# Test bench for the single cycle laboratory, used by the students to check their designs
#
# License:
# ==============================================================================
class Constants:
    # Define your constant values as class attributes for operation types
    ADD = 4
    SUB = 2
    AND = 0
    ORR = 12
    CMP = 10
    MOV = 13
    EQ = 0
    NE = 1
    AL = 14

import logging
import cocotb
from Helper_lib import read_file_to_list,Instruction,rotate_right, shift_helper, ByteAddressableMemory,reverse_hex_string_endiannes,interpret_as_signed,arithmetic_shift_right,logical_shift_right
from Helper_lib import get_unsigned_32bit,get_unsigned_16bit,get_unsigned_8bit
from Helper_Student import Log_Datapath,Log_Controller
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Edge, Timer
from cocotb.binary import BinaryValue
from decimal import *


class TB:
    def __init__(self, Instruction_list,dut,dut_PC,dut_regfile):
        self.dut = dut
        self.dut_PC = dut_PC
        self.dut_regfile = dut_regfile
        self.Instruction_list = Instruction_list
        #Configure the logger
        self.logger = logging.getLogger("Performance Model")
        self.logger.setLevel(logging.DEBUG)
        #Initial values are all 0 as in a FPGA
        self.PC = 0
        self.Z_flag = 0
        self.Register_File =[]
        for i in range(32):
            self.Register_File.append(0)
        #Memory is a special class helper lib to simulate HDL counterpart    
        self.memory = ByteAddressableMemory(8192)# changed it to 8192 from 1024?

        self.clock_cycle_count = 0        
    #Calls user populated log functions    
    def log_dut(self):
        Log_Datapath(self.dut,self.logger)
        Log_Controller(self.dut,self.logger)


    #Compares and lgos the PC and register file of Python module and HDL design
    def compare_result(self):
        self.logger.debug("************* Performance Model / DUT Data  **************")
        self.logger.debug("PC:%08X",self.dut_PC.value.signed_integer)
        self.logger.debug("PC:%08X:",self.PC)
        i=0
        j=1
        while  i < 32 :
            self.logger.debug("Register%d: %d \t %d",i,self.Register_File[i], self.dut_regfile.Reg_Out[i].value.signed_integer)
            i = i + 1
        assert self.PC == self.dut_PC.value
        for j in range(32):
           reg_val = self.dut_regfile.Reg_Out[j].value
           print(f"Register[{j}] = {reg_val}")          
           assert self.Register_File[j] == self.dut_regfile.Reg_Out[j].value.signed_integer
        

    #Function to write into the register file, handles writing into R15(PC)
    def write_to_register_file(self,register_no, data):
        self.Register_File[register_no] = data

    #A model of the verilog code to confirm operation, data is In_data
    def performance_model (self):
        self.logger.debug("**************** Clock cycle: %d **********************",self.clock_cycle_count)
        self.clock_cycle_count = self.clock_cycle_count+1
        #Read current instructions, extract and log the fields
        self.logger.debug("**************** Instruction No: %d **********************",int((self.PC)/4))
        current_instruction = self.Instruction_list[int((self.PC)/4)]
        current_instruction = current_instruction.replace(" ", "")
        #We need to reverse the oRDer of bytes since little endian makes the string reversed in Python
        current_instruction = reverse_hex_string_endiannes(current_instruction)
        execute_flag = True
        binary_instr = format(int(current_instruction, 16), '032b')
        opcode = binary_instr[25:30]
        funct3 = binary_instr[17:20]
        funct7 = binary_instr[0:7]
        RS1 = int(binary_instr[12:17], 2)
        RS2 = int(binary_instr[7:12], 2)
        RD = int(binary_instr[20:25], 2)
        #Call Instruction calls to get each field from the instruction
        inst_fields = Instruction(current_instruction)
        inst_fields.log(self.logger)
        immediate_immediate = interpret_as_signed(int(binary_instr[0:12], 2), 12)
        immediate_load = interpret_as_signed(int(binary_instr[0:12], 2), 12)  
        immediate_branch = interpret_as_signed(int(binary_instr[0], 2) << 12 | int(binary_instr[24], 2) << 11 | int(binary_instr[1:7], 2) << 5 | int(binary_instr[20:24], 2) << 1, 12)
        immediate_lui_aupic = int(binary_instr[0:20], 2)
        upper_bits = int(binary_instr[0:7], 2) << 5
        lower_bits = int(binary_instr[20:25], 2)
        imm_store = upper_bits + lower_bits
        immediate_store = interpret_as_signed(imm_store, 12)
        load_case= binary_instr[0:12]
        if(execute_flag):

            if opcode =='00100':#Immediate type
                if(RD != 0):#if the RD is nor 0 since if it is not gonna be put into R0
                    if funct3 == '000':
                        result = immediate_immediate+ self.Register_File[RS1] 
                        self.write_to_register_file(RD, result)  # ADDI
                        self.PC = self.PC + 4 #new instr. is added

                    elif funct3 == '111':
                        result =  immediate_immediate & self.Register_File[RS1] 
                        self.write_to_register_file(RD, result)  # ANDI
                        self.PC = self.PC + 4 #new instr. added

                    elif funct3 == '100':
                        result = self.Register_File[RS1] ^ immediate_immediate
                        self.write_to_register_file(RD, result)  # XORI
                        self.PC = self.PC + 4 #new instr. added

                    elif funct3 == '110':
                        result = self.Register_File[RS1] | immediate_immediate
                        self.write_to_register_file(RD, result)  # ORI
                        self.PC = self.PC + 4 #new instr. added

                    elif  binary_instr[1] == '1' and funct3 == '101' :
                        immediate_immediate_2 = interpret_as_signed(int(binary_instr[7:12], 2), 12)
                        result = arithmetic_shift_right(self.Register_File[RS1], immediate_immediate_2, 32)
                        self.write_to_register_file(RD, interpret_as_signed(result, 32))  # SRAI
                        self.PC = self.PC + 4 #new instruc. added

                    elif funct3 == '001':
                        result = self.Register_File[RS1] << immediate_immediate
                        self.write_to_register_file(RD, interpret_as_signed(result, 32))  # SLLI
                        self.PC = self.PC + 4  #new instruc. added

                    elif binary_instr[1] != '1' and funct3 == '101' :
                        result = logical_shift_right(self.Register_File[RS1], immediate_immediate, 32)
                        self.write_to_register_file(RD, interpret_as_signed(result, 32))  # SRLI
                        self.PC = self.PC + 4 #new instruc. added

                    elif funct3 == '010':
                        if(self.Register_File[RS1] < immediate_immediate):  
                            self.write_to_register_file(RD, 1)  # SLTI
                        else:
                            self.PC = self.PC + 4 #new instruc. added
                    else:
                        self.logger.error("Cannot write to R0")


                elif funct3 == '011':

                    if(get_unsigned_32bit(self.Register_File[RS1]) < get_unsigned_32bit(immediate_immediate)):
                        self.write_to_register_file(RD, 1)  # SLTIU
                        self.PC = self.PC + 4 #new instruc. added
                    else:
                        self.PC = self.PC + 4 #new instruc. added
                else:
                    self.logger.error("I-type instruction error !")
                    self.PC = self.PC + 4
                    

            elif opcode == '01101': # LUI instr. rd=(imm<<12)
                if(RD != 0):#if the RD is nor 0 since if it is not gonna be put into R0
                    self.PC = self.PC + 4
                    self.write_to_register_file(RD, immediate_lui_aupic << 12)
                else:
                    self.logger.error("Cannot write to R0")
            elif opcode == '00101': # AUPIC instr. rd= pc +  (imm<<12), 
                if(RD != 0):#if the RD is nor 0 since if it is not gonna be put into R0
                    self.write_to_register_file(RD, self.PC+ (immediate_lui_aupic<< 12))
                    self.PC = self.PC + 4  #new instruc. added
                else:
                    self.logger.error("Cannot write to R0")
            elif opcode =='01100':#R type inst.(arithmatic)
                if(RD != 0):#if the RD is nor 0 since if it is not gonna be put into R0
                    if funct3 == '000' and funct7 == '0000000':
                        result = self.Register_File[RS1] + self.Register_File[RS2]
                        self.write_to_register_file(RD, result)  # ADD
                        self.PC = self.PC + 4  #new instruc. added
                    elif funct3 == '000' and funct7 == '0100000':
                        result = self.Register_File[RS1] - self.Register_File[RS2]
                        self.write_to_register_file(RD, result)  # SUB
                        self.PC = self.PC + 4  #new instruc. added
                    elif funct3 == '111':
                        result = self.Register_File[RS1] & self.Register_File[RS2]
                        self.write_to_register_file(RD, result)  # AND
                        self.PC = self.PC + 4  #new instruc. added
                    elif funct3 == '110':
                        result = self.Register_File[RS1] | self.Register_File[RS2]
                        self.write_to_register_file(RD, result)  # OR
                        self.PC = self.PC + 4  #new instruc. added
                    elif funct3 == '100':
                        result = self.Register_File[RS1] ^ self.Register_File[RS2]
                        self.write_to_register_file(RD, result)  # XOR
                        self.PC = self.PC + 4  #new instruc. added
                    elif funct3 == '001' and funct7 == '0000000':      
                        result = self.Register_File[RS1] << (self.Register_File[RS2] & 0x1F)
                        self.write_to_register_file(RD, interpret_as_signed(result, 32))  # SLL
                        self.PC = self.PC + 4  #new instruc. added
                    elif funct3 == '101' and funct7 == '0000000':      
                        result = logical_shift_right(self.Register_File[RS1], self.Register_File[RS2] & 0x1F, 32)
                        self.write_to_register_file(RD, interpret_as_signed(result, 32))  # SRL
                        self.PC = self.PC + 4  #new instruc. added
                    elif funct3 == '101' and funct7 == '0100000':
                        result = arithmetic_shift_right(self.Register_File[RS1], (self.Register_File[RS2] & 0x1F), 32)
                        self.write_to_register_file(RD, interpret_as_signed(result, 32))  # SRA
                        self.PC = self.PC + 4  #new instruc. added
                    elif funct3 == '011' and funct7 == '0000000':
                        if(get_unsigned_32bit(self.Register_File[RS1]) < get_unsigned_32bit(self.Register_File[RS2])):
                            self.write_to_register_file(RD, 1)  # SLTU
                            self.PC = self.PC + 4  #new instruc. added

                    elif funct3 == '010' and funct7 == '0000000':
                        if(self.Register_File[RS1] < self.Register_File[RS2]):
                            self.write_to_register_file(RD, 1)  # SLT
                            self.PC = self.PC + 4  #new instruc. added

                    else:
                        self.logger.error("R-type instruction error!")
                        self.PC = self.PC + 4 # to go to the next instr.
                        assert False
                else:
                    self.logger.error("Cannot write to R0")
            elif opcode == '00000':  # Load instr.
                if(RD != 0):#if the RD is nor 0 since if it is not gonna be put into R0
                    self.PC = self.PC + 4
                    if funct3 == '010':
                        if load_case=='010000000100':
                            self.write_to_register_file(RD, -1)  # LW 0x404 and When buffer does not have new data 
                        else:
                            self.write_to_register_file(RD, interpret_as_signed(int.from_bytes(self.memory.read(self.Register_File[RS1] + immediate_load)), 32))  # LW
                    elif funct3 == '001':
                        self.write_to_register_file(RD, interpret_as_signed(int.from_bytes(self.memory.read(self.Register_File[RS1] + immediate_load)) & 0xFFFF, 16))  # LH
                    elif funct3 == '101':
                        self.write_to_register_file(RD, (int.from_bytes(self.memory.read(self.Register_File[RS1] + immediate_load))) & 0xFFFF)  # LHU
                    elif funct3 == '000':
                        self.write_to_register_file(RD, interpret_as_signed(int.from_bytes(self.memory.read(self.Register_File[RS1] + immediate_load)) & 0xFF, 8))  # LB
                    elif funct3 == '100':
                        self.write_to_register_file(RD, (int.from_bytes(self.memory.read(self.Register_File[RS1] + immediate_load))) & 0xFF)  # LBU
                    else:
                        self.logger.error("Load instruction error!")
                        assert False
                else:
                    self.logger.error("Cannot write to R0")
            elif opcode == '11000':  # B-type (branch)
                
                if funct3 == '000': # BEQ inst.
                    if self.Register_File[RS1] == self.Register_File[RS2]:
                        self.PC += immediate_branch   #New PC value
                    else:
                        self.PC = self.PC + 4 #else do nor branch
                elif funct3 == '001': # BNE instr.
                    if self.Register_File[RS1] != self.Register_File[RS2]:
                        self.PC += immediate_branch  #New PC value
                    else:
                        self.PC = self.PC + 4
                elif funct3 == '100':# BLT instr.
                    if self.Register_File[RS1] < self.Register_File[RS2]:
                        self.PC += immediate_branch   #New PC value
                    else:
                        self.PC = self.PC + 4
                elif funct3 == '101': # BGE instr.
                    if self.Register_File[RS1] >= self.Register_File[RS2]:
                        self.PC += immediate_branch # the new PC value is from immediate
                    else:
                        self.PC = self.PC + 4
                elif funct3 == '110': # BLTU instr.
                    if abs(self.Register_File[RS1]) < get_unsigned_32bit(self.Register_File[RS2]):
                        self.PC += immediate_branch  #New PC value
                    else:
                        self.PC = self.PC + 4
                elif funct3 == '111': # BGEU instr.
                    if abs(self.Register_File[RS1]) >= get_unsigned_32bit(self.Register_File[RS2]):
                        self.PC += immediate_branch   #New PC value
                    else:
                        self.PC = self.PC + 4

                else:
                    self.logger.error("B-type instruction error!")
                    assert False



            elif opcode == '11001': # JALR instr. only

                self.PC = self.PC + 4
                imm_jalr = int(binary_instr[0:12], 2)
                immediate_jalr = interpret_as_signed(imm_jalr, 12)
                RS1_value = self.Register_File[RS1]
                if(RD != 0):#if the RD is nor 0 since if it is not gonna be put into R0
                    self.write_to_register_file(RD, self.PC)#in jalr in x[rd] the pc+4 is put        
                else:
                    self.logger.error("Cannot write to R0")       
                self.PC = immediate_jalr + RS1_value


            elif opcode == '11011':  # JAL instr. only

                imm_jal = (int(binary_instr[0:1], 2) << 20) + (int(binary_instr[12:20], 2) << 12) + (int(binary_instr[11:12], 2) << 11) | (int(binary_instr[1:11], 2) << 1)
                immediate_jal = interpret_as_signed(imm_jal, 21)
                if(RD != 0):
                    self.write_to_register_file(RD, self.PC+4) #pc+4 is put to the RD when RD is not R0
                else:
                    self.logger.error("Cannot write to R0")
                self.PC += immediate_jal  #pc is updated with adding immediate

            elif opcode == '01000':  # S-type

                if funct3 == '001':  # SH
                    self.memory.write(self.Register_File[RS1] + immediate_store, get_unsigned_16bit(self.Register_File[RS2]), 2)
                    self.PC = self.PC + 4 #to next inst.
                elif funct3 == '010':  # SW
                    self.memory.write(self.Register_File[RS1] + immediate_store, get_unsigned_32bit(self.Register_File[RS2]), 4)
                    self.PC = self.PC + 4 #to next inst.
                
                elif funct3 == '000':  # SB
                    addr = self.Register_File[RS1] + immediate_store
                    data = get_unsigned_8bit(self.Register_File[RS2])
                    print(f"SB write: addr=0x{addr:X}, data=0x{data:X}, size=1, mem_size={self.memory.size}")
                    self.memory.write(addr, data, 1)
                    self.memory.write(self.Register_File[RS1] + immediate_store, get_unsigned_8bit(self.Register_File[RS2]), 1)
                    self.PC = self.PC + 4 #to next inst.
                else:
                    self.logger.error("S-type instruction error!")
                    self.PC = self.PC + 4 # to new instr.
                    assert False
      
            else:
                self.logger.error(" Not found!")
                self.PC = self.PC + 4 #to new instr.
                assert False
        else:
            self.logger.debug("Error!!!!!!")

    async def run_test(self):
        self.performance_model()
        await Timer(1, units="us")
        self.log_dut()
        await RisingEdge(self.dut.clk)
        await FallingEdge(self.dut.clk)
        self.compare_result()
        while(int(self.Instruction_list[int((self.PC)/4)].replace(" ", ""),16)!=0):
            self.performance_model()
            self.log_dut()
            await RisingEdge(self.dut.clk)
            await FallingEdge(self.dut.clk)
            self.compare_result()
                
                   
@cocotb.test()
async def Single_cycle_test(dut):
    #Generate the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    #Reset onces before continuing with the tests
    dut.reset.value=1
    await RisingEdge(dut.clk)
    dut.reset.value=0
    await FallingEdge(dut.clk)
    instruction_lines = read_file_to_list('Instructions.hex')
    #Give PC signal handle and Register File MODULE handle
    tb = TB(instruction_lines,dut, dut.PC, dut.my_datapath.reg_file_dp)
    await tb.run_test()