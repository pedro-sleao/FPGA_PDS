module mult_4bits (
	input 		clk_i,
	input			rst_i,
	input 		en_i,
	input [3:0] A_i,
	input [3:0] B_i,
	output [7:0] Y_o
);

estado_t state_o_w;

wire [3:0] B_i_w, B_o_w;
wire [7:0] A_i_w, A_o_w, Y_i_w, Y_o_w;

assign A_i_w = (state_o_w == ST_IDLE)? {4'h0, A_i}: A_o_w << 1;
assign B_i_w = (state_o_w == ST_IDLE)? B_i: B_o_w >> 1;
assign Y_i_w = (state_o_w == ST_IDLE)? 8'd0:
					(state_o_w == ST_END)? Y_o_w:
					(B_o_w[0] == 1'b1)? Y_o_w + A_o_w: Y_o_w;

registrador
	#(
	.DATA_WIDTH(8)
	)
	reg_A_inst
		(
		.clk (clk_i),
		.reset (rst_i),
		.data_i (A_i_w),
		.data_o (A_o_w)
		);

registrador
	#(
	.DATA_WIDTH(4)
	)
	reg_B_inst
		(
		.clk (clk_i),
		.reset (rst_i),
		.data_i (B_i_w),
		.data_o (B_o_w)
		);
		
registrador
	#(
	.DATA_WIDTH(8)
	)
	reg_Y_inst
		(
		.clk (clk_i),
		.reset (rst_i),
		.data_i (Y_i_w),
		.data_o (Y_o_w)
		);
	
controlador_mult controlador_inst (
	 .clk_i (clk_i),
	 .rst_i (rst_i),
	 .strt_cmpt_i (en_i),
	 .state_o (state_o_w)
);

assign Y_o = Y_o_w;


endmodule
