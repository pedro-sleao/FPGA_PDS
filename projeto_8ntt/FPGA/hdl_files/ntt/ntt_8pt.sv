`include "./ntt_defines.sv"

module ntt_8pt
    (
    input clk, 
    input reset,
	 input start,
    input [11:0] in[7:0],
	 output [11:0] out[7:0],
	 output estagio1_done,
	 output estagio2_done
    ); 
	 
// Sinais das operacoes
wire [11:0] out_estagio1_w[7:0];
wire fim_estagio1_w, fim1_w, fim2_w;
	 
ntt_bf8 ntt_bf8_inst (
    .clk (clk),
    .reset (reset),
    .start (start),
    .in (in),
	 .twf (ZETA[1]),
    .out (out_estagio1_w),
    .done (fim_estagio1_w)
);

ntt_bf4 ntt_bf4_inst1 (
    .clk (clk),
    .reset (reset),
    .start (fim_estagio1_w),
    .in (out_estagio1_w[3:0]),
	 .twf (ZETA[2]),
    .out (out[3:0]),
    .done (fim1_w)
);

ntt_bf4 ntt_bf4_inst2 (
    .clk (clk),
    .reset (reset),
    .start (fim_estagio1_w),
    .in (out_estagio1_w[7:4]),
	 .twf (ZETA[3]),
    .out (out[7:4]),
    .done (fim2_w)
);

// Saidas
assign estagio1_done = fim_estagio1_w;
assign estagio2_done = fim1_w & fim2_w;

endmodule
