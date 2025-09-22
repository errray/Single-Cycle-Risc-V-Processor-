module uart_rx (
    input        clk,
    input        rst,
    input        uart_rx_serial_input,          // UART RX pin (serial data input) 1 bit 
    input        read_enable,       // memory read strobe (from address 0x00000404)
    output reg [31:0] read_data     // output to processor's memory bus
);

    // === UART Baud Timing (9600 baud @ 100 MHz) ===
    parameter BAUD_DIV = 10416;

    reg [12:0] baud_cnt = 0;
    reg [3:0]  bit_cnt = 0;
    reg [9:0]  rx_shift = 0;
    reg        receiving = 0;

    // === FIFO Buffer ===
    reg [7:0] fifo [15:0];      // 16-byte circular buffer
    reg [3:0] head = 0;         // read index
    reg [3:0] tail = 0;         // write index
    reg [4:0] count = 0;        // number of stored bytes

    // === UART Receiver Logic ===
    always @(posedge clk) begin
        if (rst) begin
            baud_cnt   <= 0;
            bit_cnt    <= 0;
            receiving  <= 0;
        end else begin
            if (!receiving && !uart_rx_serial_input) begin  // Start bit detected
                receiving <= 1;
                baud_cnt  <= BAUD_DIV / 2;      // Sample in middle of start bit
                bit_cnt   <= 0;
            end else if (receiving) begin
                if (baud_cnt == BAUD_DIV - 1) begin
                    baud_cnt <= 0;
                    rx_shift <= {uart_rx_serial_input, rx_shift[9:1]};
                    bit_cnt  <= bit_cnt + 1;

                    if (bit_cnt == 9) begin     // All 10 bits (start, 8 data, stop)
                        receiving <= 0;
                        if (count < 16) begin   // Only write if buffer not full
                            fifo[tail] <= rx_shift[8:1]; // Store data bits
                            tail <= tail + 1;
                            count <= count + 1;
                        end
                    end
                end else begin
                    baud_cnt <= baud_cnt + 1;
                end
            end
        end
    end

    // === Combinational Memory Read Interface ===
    always @(*) begin
        if (read_enable) begin
            if (count > 0)
                read_data = {24'b0,fifo[head]};   // Output oldest byte
            else
                read_data = 32'hFFFFFFFF;          // No data available
        end else begin
            read_data = 32'hZZZZZZZZ;              // Tri-state when not reading
        end
    end

    // === Read Acknowledgment (advance head) ===
    always @(posedge clk) begin
        if (read_enable && count > 0) begin
            head  <= head + 1;
            count <= count - 1;
        end
    end

endmodule
