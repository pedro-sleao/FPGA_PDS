module ctbf
    #(      
        parameter  N = 12,
        parameter  Q = 3329
    )
    (
    input clk, 
    input reset,
	 input start,
    input [11:0] in_1,
	 input [11:0] in_2,
	 input [11:0] twf,
	 output [11:0] out_1,
	 output [11:0] out_2,
	 output done
    ); 

// Sinais das operacoes
wire [11:0] mmm_o_w, mmm_done_w;	 
	 
montgomery_mult_mod mmm_inst(
	 .clk (clk),
	 .rst (reset),
	 .start (start),
	 .a (in_2),
	 .b (twf),
	 .result (mmm_o_w),
	 .done (mmm_done_w)
);	 

somador_modular somador_inst(
	 .a (in_1),
	 .b (mmm_o_w),
	 .y (out_1)
);

subtrator_modular subtrator_inst(
	 .a (in_1),
	 .b (mmm_o_w),
	 .y (out_2)
);

// Saidas
assign done = mmm_done_w;
					 
endmodule
