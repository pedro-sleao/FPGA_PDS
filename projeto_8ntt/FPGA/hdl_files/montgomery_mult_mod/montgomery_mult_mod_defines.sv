`ifndef MONTGOMERY_MULT_MOD_DEFINES_SV
`define MONTGOMERY_MULT_MOD_DEFINES_SV

// Estados
typedef enum logic [2:0] {
	ST_IDLE,
	ST_CONVERT,
	ST_MULTIPLY,
	ST_CALC_COEFF,
	ST_REDUCE,
	ST_CONVERT_BACK,
	ST_END
} estado_mmm_t;

// Valores pre-calculados
parameter logic [3:0] k = 4'd12;
parameter logic [11:0] q = 12'd3329;
parameter logic [12:0] r = 13'd4096;
parameter logic [11:0] r_inv = 12'd2704;
parameter logic [11:0] q_invn_r = 12'd3327;

`endif
