module Memory#(BYTE_SIZE=4, ADDR_WIDTH=32)(
input clk,
input [1:0] WE,
input [31:0] ADDR,
input [31:0] WD,
input [31:0] UART_RX_data,
output reg [31:0] RD,
output reg start_UART,
output reg start_UART_rx,
output reg  [7:0] data_in_UART
);

reg [7:0] mem [255:0];


//////////// uart related
//UART SENT 
always @(*) begin
     start_UART = 0;
     if(WE == 2'b00 && ADDR == 32'h00000400)begin
        start_UART = 1;
        data_in_UART = WD[7:0];
     end
end
//UART RECEIVE 
always @(*) begin
     start_UART_rx = 0;
     if(ADDR == 32'h00000404)begin  
        start_UART_rx = 1;
     end
end
/////////////

always @(*) begin
    if (ADDR == 32'h00000404) begin
        RD = {24'b0, UART_RX_data};  // Read from UART buffer (LSB)
    end else begin
        RD = {mem[ADDR+3], mem[ADDR+2], mem[ADDR+1], mem[ADDR]};
    end
end

integer k;
always @(posedge clk) begin

    if(WE == 2'b10) begin	// 4byte (default) sw
        for (k = 0; k < 4; k = k + 1) begin
            mem[ADDR+k] <= WD[8*k+:8];
        end
    end
	 if(WE == 2'b01) begin	//2 byte sh
        for (k = 0; k <2; k = k + 1) begin
            mem[ADDR+k] <= WD[8*k+:8];
        end
    end
	 if(WE == 2'b00) begin	//1 byte sb
        for (k = 0; k < 1; k = k + 1) begin
            mem[ADDR+k] <= WD[8*k+:8];
        end
    end
end

endmodule
