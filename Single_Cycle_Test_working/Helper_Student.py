def ToHex(value):
    try:
        ret = hex(value.integer)
    except: #If there are 'x's in the value
        ret = "0b" + str(value)
    return ret

#Populate the below functions as in the example lines of code to print your values for debugging
def Log_Datapath(dut,logger):
    #Log whatever signal you want from the datapath, called before positive clock edge
    logger.debug("************ DUT DATAPATH Signals ***************")
    #dut._log.info("reset:%s", ToHex(dut.my_datapath.reset.value))
    dut._log.info("ALUSrc:%s", ToHex(dut.my_datapath.ALUSrc.value))
    #dut._log.info("MemWrite:%s", ToHex(dut.my_datapath.MemWrite.value))
    dut._log.info("RegWrite:%s", ToHex(dut.my_datapath.RegWrite.value))
    dut._log.info("PCSrc:%s", ToHex(dut.my_datapath.PCSrc.value))
    dut._log.info("MemtoReg:%s", ToHex(dut.my_datapath.MemtoReg.value))
    dut._log.info("SrcA:%s", ToHex(dut.my_datapath.SrcA.value))
    dut._log.info("SrcB:%s", ToHex(dut.my_datapath.SrcB.value))
    dut._log.info("ALUControl:%s", ToHex(dut.my_datapath.ALUControl.value))
    dut._log.info("PCPlus4:%s", ToHex(dut.my_datapath.PCPlus4.value))
    dut._log.info("ALUResult:%s", ToHex(dut.my_datapath.ALUResult.value))
    dut._log.info("PCTarget:%s", ToHex(dut.my_datapath.PCTarget.value))
    dut._log.info("ExtImm:%s", ToHex(dut.my_datapath.ExtImm.value))
    dut._log.info("Result:%s", ToHex(dut.my_datapath.Result.value))
    dut._log.info("PC_prime:%s", ToHex(dut.my_datapath.PC_prime.value))
    dut._log.info("less_than:%s", ToHex(dut.my_datapath.less_than.value))
    dut._log.info("PC:%s", ToHex(dut.my_datapath.PC.value))
    dut._log.info("ReadData:%s", ToHex(dut.my_datapath.ReadData.value))
    dut._log.info("uart_tx_serial_output:%s", ToHex(dut.my_datapath.uart_tx_serial_output.value))
    dut._log.info("start:%s", ToHex(dut.my_datapath.start.value))


def Log_Controller(dut,logger):
    #Log whatever signal you want from the controller, called before positive clock edge
    logger.debug("************ DUT Controller Signals ***************")
    dut._log.info("Op:%s", ToHex(dut.my_controller.op.value))
    #dut._log.info("Funct:%s", ToHex(dut.my_controller.Funct.value))
    #dut._log.info("Rd:%s", ToHex(dut.my_controller.Rd.value))
    #dut._log.info("Src2:%s", ToHex(dut.my_controller.Src2.value))
    dut._log.info("PCSrc:%s", ToHex(dut.my_controller.PCSrc.value))
    dut._log.info("RegWrite:%s", ToHex(dut.my_controller.RegWrite.value))
    dut._log.info("MemWrite:%s", ToHex(dut.my_controller.MemWrite.value))
    dut._log.info("ALUControl:%s", ToHex(dut.my_controller.ALUControl.value))
    dut._log.info("Branch_control:%s", ToHex(dut.my_controller.Branch_control.value))
    #dut._log.info("nMemWrite:%s", ToHex(dut.my_controller.nMemWrite.value))
    #dut._log.info("ALUSrc:%s", ToHex(dut.my_controller.ALUSrc.value))
    dut._log.info("MemtoReg:%s", ToHex(dut.my_controller.MemtoReg.value))
    #dut._log.info("ALUControl:%s", ToHex(dut.my_controller.ALUControl.value))
    dut._log.info("deneme:%s", ToHex(dut.my_controller.deneme.value))
    #dut._log.info("ImmSrc:%s", ToHex(dut.my_controller.ImmSrc.value))
    #dut._log.info("RegSrc:%s", ToHex(dut.my_controller.RegSrc.value))
    #dut._log.info("ALUFlags:%s", ToHex(dut.my_controller.ALUFlags.value))
    #dut._log.info("ShiftControl:%s", ToHex(dut.my_controller.ShiftControl.value))
    #dut._log.info("shamt:%s", ToHex(dut.my_controller.shamt.value))
    #dut._log.info("CondEx:%s", ToHex(dut.my_controller.CondEx.value))