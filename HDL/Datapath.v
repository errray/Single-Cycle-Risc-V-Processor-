module datapath (
	input PCSrc,
	input clock,
	input RESET,
	input RegWrite,
	input ALUSrc,
	input CLK100MHZ,
	input [3:0] ALUControl,
	input [2:0] ImmSrc, // 3 bit, tekrar kontrol edilmeli (değiştirilebilir)
	input [1:0]MemWrite,
	input MemtoReg,
	output [31:0] PC,
	output [31:0] instr_debug,
	//additional control signals 
	input WD3Control,
	input SrcAControl,Branch_control,
	output Equal,Zero,CO,OVF,less_than,
		//additional control signals 
	input [1:0] shamt_control,
	input [1:0] shifter_control,
	input [4:0] Debug_Source_select,
	output [31:0] Debug_out,
	//uart outputs 
	output uart_tx_serial_output,
	output busy,
	output start,
	input uart_rx_serial_input
);

wire [31:0] Instr;
assign instr_debug = Instr;
wire [31:0] PCPlus4,PCTarget;
wire [31:0] Result;
wire [31:0] PC_prime;
wire [31:0] WD3;
wire [31:0] RD1;
wire [31:0] WriteData;
wire [31:0] ExtImm;
wire [31:0] SrcA;
wire [31:0] SrcB;
wire [31:0] SrcAShifted;
wire [31:0] ALUResult;
wire [31:0] ReadData;
wire [31:0] ReadDataMasked,PC_change;
wire [4:0] shamt;

Mux_2to1 #(32) m1(
	.select(PCSrc),
	.input_0(PC_change),
	.input_1(Result),
	.output_value(PC_prime)
);
Mux_2to1 #(32) branch(
	.select(Branch_control),
	.input_0(PCPlus4), 
	.input_1(PCTarget), 
	.output_value(PC_change)
);
Register_rsten_neg #(.WIDTH(32)) PCReg ( //
   .clk(clock), 
   .reset(RESET),
   .we(1'b1),
	.DATA(PC_prime),
	.OUT(PC)
);

Instruction_memory #(4,32) im(
	.ADDR(PC),
	.RD(Instr)
);

Adder #(32) a1(
	.DATA_A(PC), 
	.DATA_B(4),
	.OUT(PCPlus4)
);

Adder #(32) pctarget(
	.DATA_A(PC), 
	.DATA_B(ExtImm),
	.OUT(PCTarget)
);

Mux_2to1 #(32) m5(
	.select(WD3Control),
	.input_0(Result), 
	.input_1(PCPlus4), 
	.output_value(WD3)
);

Register_file #(32) reg_file_dp  (       
    .clk(clock), 
    .write_enable(RegWrite), 
    .reset(RESET),
    .Source_select_0(Instr[19:15]), 
    .Source_select_1(Instr[24:20]), 
    .Debug_Source_select(Debug_Source_select), //debug
    .Destination_select(Instr[11:7]),
    .DATA(WD3), 
    .out_0(RD1),
    .out_1(WriteData), 
    .Debug_out(Debug_out)   //debug
);

Extender e(									
    .Q(ExtImm), 
    .A(Instr), 
    .select(ImmSrc)
);

Mux_2to1 #(32) m6(
	.select(SrcAControl),
	.input_0(RD1), 
	.input_1(PC), 
	.output_value(SrcA)	
);

Mux_2to1 #(32) m7(
	.select(ALUSrc),
	.input_0(WriteData), 
	.input_1(ExtImm), 
	.output_value(SrcB)	
);

Mux_4to1 #(5) m12(
	.select(shamt_control),
	.input_0(5'b00000),
	.input_1(WriteData[4:0]),
	.input_2(ExtImm[4:0]),
	.input_3(5'b01100),
	.output_value(shamt)
);

shifter #(32) shf ( 
    .control(shifter_control), 
    .shamt(shamt), 
    .DATA(SrcA), 
    .OUT(SrcAShifted)
);

ALU my_alu (
    .A_in(SrcAShifted),         // First operand (e.g., from rs1)
    .B_in(SrcB),         // Second operand 
    .ALU_Sel(ALUControl),      // ALU operation select (from control unit)
    .ALU_Out(ALUResult),      // Output result to WriteData or ALUResult
    .Carry_Out(CO),    // Optional: useful for add/sub (can be left unconnected)////////////
    .Equal(Equal),        // Used for branch equal comparison
    .less_than(less_than),    // Used for SLT/SLTU
    .Zero(Zero),         // Zero flag (useful for BEQ, BNE)
    .Overflow(OVF)      // Optional: overflow detection////////////////////////
);

wire [7:0] data_in;
wire [31:0] read_data;
wire rx_starting_signal;

Memory #(4, 32) mem (                        
    .clk(clock), 
    .WE(MemWrite), 
    .ADDR(ALUResult), 
    .WD(WriteData), 
    .RD(ReadData),
	.data_in_UART(data_in),
	.start_UART(start),
	.UART_RX_data(read_data),
	.start_UART_rx(rx_starting_signal)
);

uart_tx uart_T (
	.clk(CLK100MHZ),
	.start(start),
	.data_in(data_in),
	.uart_tx(uart_tx_serial_output),
	.busy(busy)
);

uart_rx uart_R(
	.clk(CLK100MHZ),
	.rst(RESET),
	.uart_rx_serial_input(uart_rx_serial_input),
	.read_enable(rx_starting_signal),
	.read_data(read_data)
);

DMDATA memory_masking_after_memory (
	.ReadData(ReadData),                  
	.Funct3(Instr[14:12]),                
	.ReadDataMasked(ReadDataMasked)       //Proper word size is selected and sign/zero extended. 
);

Mux_2to1 #(32) m8(
	.select(MemtoReg),
	.input_0(ALUResult), 
	.input_1(ReadDataMasked), 
	.output_value(Result)	
);

endmodule 