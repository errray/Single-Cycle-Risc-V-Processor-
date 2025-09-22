module top(

	input clk,
    input CLK100MHZ,
	input reset,
    input uart_rx_serial_input, //connect it to corresponding board part by master.xdc file   
	output [31:0] PC,
    output uart_tx_serial_output,
    input [4:0] Debug_Source_select ,
    output [31:0] Debug_out

);  


// Control signals
wire        PCSrc;
wire        RegWrite;
wire        ALUSrc;
wire        Branch_control;
wire [3:0]  ALUControl;
wire [2:0]  ImmSrc;
wire [1:0]  MemWrite;
wire        MemtoReg;
wire        WD3Control;
wire        SrcAControl;
wire [1:0]  shamt_control;
wire [1:0]  shifter_control;
wire        ResultSrc;
wire [31:0] Instr;
wire Equal,Zero,CO,OVF,less_than;


datapath my_datapath (
    .PCSrc(PCSrc),
    .clock(clk),
    .RESET(reset),
    .RegWrite(RegWrite),
    .ALUSrc(ALUSrc),
    .ALUControl(ALUControl),
    .ImmSrc(ImmSrc),
    .MemWrite(MemWrite),
    .MemtoReg(MemtoReg),
    .PC(PC),
    .instr_debug(Instr),
    // additional control signals
    .WD3Control(WD3Control),
    .SrcAControl(SrcAControl),
    .shamt_control(shamt_control),
    .shifter_control(shifter_control),
    .Equal(Equal),
    .Zero(Zero),
    .CO(CO),
    .OVF(OVF),
    .less_than(less_than),
    .Branch_control(Branch_control),
    .uart_tx_serial_output(uart_tx_serial_output),
    .busy(),
    .start(),
    .Debug_Source_select(Debug_Source_select),
    .Debug_out(Debug_out),
    .uart_rx_serial_input(uart_rx_serial_input),
    .CLK100MHZ(CLK100MHZ)
    );

Controller my_controller (
    .INSTR(Instr),
    .PCSrc(PCSrc),
    .MemWrite(MemWrite),
    .ImmSrc(ImmSrc),
    .ALUControl(ALUControl),
    .WD3Control(WD3Control),
    .SrcAcontrol(SrcAControl),
    .ALUSrc(ALUSrc),
    .RegWrite(RegWrite),
    .MemtoReg(MemtoReg),
    .shamt_control(shamt_control),
    .shifter_control(shifter_control),
    .funct3(),
    .op(),
    .funct7(),
    .Equal(Equal),
    .Zero(Zero),
    .CO(CO),
    .OVF(OVF),
    .less_than(less_than),
    .Branch_control(Branch_control)

);






endmodule
