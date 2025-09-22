module Nexys_A7(
    //////////// GCLK //////////
    input wire                  CLK100MHZ,
	//////////// BTN //////////
	input wire		     		BTNU, 
	                      BTNL, BTNC, BTNR,
	                            BTND,
	//////////// SW //////////
	input wire	     [15:0]		SW,
	//////////// LED //////////
	output wire		 [15:0]		LED,
    //////////// 7 SEG //////////
    output wire [7:0] AN,
    output wire CA, CB, CC, CD, CE, CF, CG, DP,
    /////////////UART //////////////
    input wire UART_TXD_IN,
    output wire UART_RXD_OUT
);

wire [31:0] reg_out;
wire [7:0] PC;
wire [4:0] buttons;

assign LED = SW;

MSSD mssd_0(
        .clk        (CLK100MHZ                      ),
        .value      ({PC[7:0], reg_out[23:0]}       ),
        .dpValue    (8'b01000000                    ),
        .display    ({CG, CF, CE, CD, CC, CB, CA}   ),
        .DP         (DP                             ),
        .AN         (AN                             )
    );

debouncer debouncer_0(
        .clk        (CLK100MHZ                      ),
        .buttons    ({BTNU, BTNL, BTNC, BTNR, BTND} ),
        .out        (buttons                        )
    );

top my_top(
        .clk                (buttons[4]             ),
        .CLK100MHZ     (       CLK100MHZ         ),
        .reset              (buttons[0]             ),
        .Debug_Source_select   (SW[4:0]                ),
        .Debug_out      (reg_out                ),
        .PC            (PC                     ),
        .uart_tx_serial_output             (         UART_RXD_OUT          ),
        .uart_rx_serial_input            (  UART_TXD_IN                    )
    );

endmodule
