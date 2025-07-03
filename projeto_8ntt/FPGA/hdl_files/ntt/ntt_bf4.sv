module ntt_bf4
    #(      
		  parameter  LENGTH = 2
    )
    (
    input clk, 
    input reset,
	 input start,
    input [11:0] in[3:0],
	 input [11:0] twf,
	 output [11:0] out[3:0],
	 output done
    ); 

// Sinais das operacoes
wire [LENGTH-1:0] ctbf_done_w;

// Operacoes borboleta
genvar i;
generate
	for (i = 0; i < LENGTH; i = i + 1) begin: ctbf_block
		ctbf ctbf_inst (
			 .clk (clk),
			 .reset (reset),
			 .start (start),
			 .in_1 (in[i]),
			 .in_2 (in[i + LENGTH]),
			 .twf (twf),
			 .out_1 (out[i]),
			 .out_2 (out[i + LENGTH]),
			 .done (ctbf_done_w[i])
		);
	end
endgenerate

assign done = (ctbf_done_w == 2'h3);

endmodule
