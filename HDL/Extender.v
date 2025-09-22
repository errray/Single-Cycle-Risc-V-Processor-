module Extender(
input [31:0] A,
input [2:0]select,
output reg [31:0] Q

);
//To add the for U I need to increase selection bits to 3. Or can do it with a shifter 
// To add {A[31:12],12'b0} it is for U instructions

always @(*) begin
	case(select)
	    3'b000: Q=  {{20{A[31]}}, A[31:20]};                               //For I
	    3'b001: Q = {{19{A[31]}}, A[31], A[7], A[30:25],A[11:8], 1'b0};    //For B
		3'b010: Q = {{20{A[31]}}, A[31:25], A[11:7]};                      //For S
		3'b011: Q = {{12{A[31]}}, A[19:12], A[20], A[30:21], 1'b0};        //For J
		3'b100: Q = {A[31:12], 12'b0};                                    //For U
		default: Q = {32'b0};
	endcase
end

endmodule