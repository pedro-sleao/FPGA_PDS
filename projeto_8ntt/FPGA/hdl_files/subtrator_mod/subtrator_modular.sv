module subtrator_modular #(
    parameter N = 12,
	 parameter [N-1:0] q = 12'd3329
)(
    input  wire [N-1:0] a, b,
    output wire [N-1:0] y
);

    wire [N-1:0] aminusb;
    assign aminusb = a - b;
    assign y = (a >= b) ? aminusb : aminusb + q;
	 
endmodule
