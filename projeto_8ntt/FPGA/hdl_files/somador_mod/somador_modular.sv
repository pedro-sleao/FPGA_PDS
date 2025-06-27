module somador_modular #(
    parameter N = 12
)(
    input  wire [N-1:0] a, b, q,
    output wire [N-1:0] y
);

    wire [N:0] sum;    // N+1 bits para somar sem overflow
    assign sum = a + b;
    assign y = (sum >= q) ? sum - q : sum;
	 
endmodule
