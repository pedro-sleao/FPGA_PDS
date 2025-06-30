module somador_modular #(
    parameter N = 12,
	 parameter [N-1:0] q = 12'd3329
)(
    input  wire [N-1:0] a, b,
    output wire [N-1:0] y
);

    wire [N:0] sum;    // N+1 bits para somar sem overflow
    assign sum = a + b;
    assign y = (sum >= q) ? sum - q : sum;
	 
endmodule
