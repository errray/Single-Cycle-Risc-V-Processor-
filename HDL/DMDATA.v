module DMDATA(
	input [31:0] ReadData,
	input [2:0] Funct3,
	output reg [31:0] ReadDataMasked
);

always@(*) begin
	case(Funct3)
		3'b000: ReadDataMasked = {{24{ReadData[7]}}, ReadData[7:0]};     // LB
		3'b100: ReadDataMasked = {24'b0, ReadData[7:0]};					 // LBU
		3'b001: ReadDataMasked = {{16{ReadData[15]}}, ReadData[15:0]};   // LH
		3'b101: ReadDataMasked = {16'b0, ReadData[15:0]};                // LHU
		3'b010: ReadDataMasked = ReadData;                              // LW
		default: ReadDataMasked = 32'b0;                               // Safe default  
	endcase 
end

endmodule
