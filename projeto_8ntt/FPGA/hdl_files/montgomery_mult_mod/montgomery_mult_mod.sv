//----------------------------------------------------------------------------- 
// Descrição: Multiplicação de Montgomery utilizando o algoritmo descrito no artigo 
//            2023 Conceptual_Review_on_Number_Theoretic_Transform_and_Comprehensive_Review_on_Its_Implementations 
//----------------------------------------------------------------------------- 

`include "./montgomery_mult_mod_defines.sv"

module montgomery_mult_mod (
    input  clk,
    input  rst,
    input  start,
    input  [11:0] a,
    input  [11:0] b,
    output [11:0] result,
    output done
);

// INTERNAL REGS ###################### 

registrador
	#(
	.DATA_WIDTH(24)
	)
	reg_am_inst
		(
		.clk (clk),
		.reset (rst),
		.data_i (am_i_w),
		.data_o (am_o_w)
		);

registrador
	#(
	.DATA_WIDTH(24)
	)
	reg_bm_inst
		(
		.clk (clk),
		.reset (rst),
		.data_i (bm_i_w),
		.data_o (bm_o_w)
		);

registrador
	#(
	.DATA_WIDTH(24)
	)
	reg_t_inst
		(
		.clk (clk),
		.reset (rst),
		.data_i (t_i_w),
		.data_o (t_o_w)
		);
		
registrador
	#(
	.DATA_WIDTH(24)
	)
	reg_u_inst
		(
		.clk (clk),
		.reset (rst),
		.data_i (u_i_w),
		.data_o (u_o_w)
		);
			
registrador
	#(
	.DATA_WIDTH(24)
	)
	reg_cm_inst
		(
		.clk (clk),
		.reset (rst),
		.data_i (cm_i_w),
		.data_o (cm_o_w)
		);
		
registrador
	#(
	.DATA_WIDTH(12)
	)
	reg_c_inst
		(
		.clk (clk),
		.reset (rst),
		.data_i (c_i_w),
		.data_o (c_o_w)
		);
		
registrador
	#(
	.DATA_WIDTH(1)
	)
	reg_done_inst
		(
		.clk (clk),
		.reset (rst),
		.data_i (done_i_w),
		.data_o (done_o_w)
		);

// INTERNAL SIGNALS ###################
estado_mmm_t state, next_state;
wire [23:0] am_i_w, am_o_w, bm_i_w, bm_o_w, t_i_w, t_o_w, u_i_w, u_o_w, cm_i_w, cm_o_w;
wire [11:0] c_i_w, c_o_w;
wire done_i_w, done_o_w;

always @(posedge clk, negedge rst) begin
	if (rst == 1'b0)
		state <= ST_IDLE;
	else
		state <= next_state;
end

always @(start, state) begin
	case (state)
		ST_IDLE: next_state <= start ? ST_CONVERT : ST_IDLE;
		ST_CONVERT: next_state <= ST_MULTIPLY;
		ST_MULTIPLY: next_state <= ST_CALC_COEFF;
		ST_CALC_COEFF: next_state <= ST_REDUCE;
		ST_REDUCE: next_state <= ST_CONVERT_BACK;
		ST_CONVERT_BACK: next_state <= ST_END;
		ST_END: next_state <= !start ? ST_IDLE : ST_END;
		default: next_state <= ST_IDLE;
	endcase
end

// Logica de atualizacao dos registradores
assign am_i_w = (state == ST_CONVERT) ? (a << k) % q : am_o_w;
assign bm_i_w = (state == ST_CONVERT) ? (b << k) % q : bm_o_w;
assign t_i_w = (state == ST_MULTIPLY) ? am_o_w * bm_o_w : t_o_w;
assign u_i_w = (state == ST_CALC_COEFF) ? (t_o_w * q_invn_r) & (r - 1) : u_o_w;
assign cm_i_w = (state == ST_REDUCE) ? (t_o_w + u_o_w * q) >> k : cm_o_w;
assign c_i_w = (state == ST_END) ? (cm_o_w * r_inv) % q : c_o_w;
assign done_i_w = (state == ST_END) ? 1 : 0;

// Saidas
assign done = done_o_w;
assign result = c_o_w;
	 
endmodule

