module uart_tx(
    input        clk,
    input        start,
    input  [7:0] data_in,
    output reg   uart_tx,
    output reg   busy
);

    // 9600 baud with 100 MHz clock
    parameter BAUD_DIV = 10416;

    reg [3:0] bit_index = 0;
    reg [9:0] tx_shift = 10'b1111111111;
    reg [1:0] state = 0;
    reg [13:0] baud_cnt = 0;

    always @(posedge clk) begin
        case (state)
            0: begin // IDLE
                uart_tx <= 1;
                busy    <= 0;
                baud_cnt <= 0;
                if (start) begin
                    tx_shift <= {1'b1, data_in, 1'b0}; // stop, data[7:0], start
                    bit_index <= 0;
                    busy <= 1;
                    state <= 1;
                end
            end
            1: begin // SEND (1 bit every BAUD_DIV cycles)
                if (baud_cnt == BAUD_DIV - 1) begin
                    baud_cnt <= 0;
                    uart_tx <= tx_shift[bit_index];
                    bit_index <= bit_index + 1;
                    if (bit_index == 9)
                        state <= 2;
                end else begin
                    baud_cnt <= baud_cnt + 1;
                end
            end
            2: begin // DONE
                uart_tx <= 1;
                busy <= 0;
                state <= 0;
            end
        endcase
    end
endmodule
