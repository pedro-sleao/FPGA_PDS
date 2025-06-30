`ifndef MONTGOMERY_MULT_MOD_SV
`define MONTGOMERY_MULT_MOD_SV

// Estados
typedef enum logic [1:0] {
	IDLE = 2'b00,
	CONVERT = 2'b01,
	MULTIPLY = 2'b10,
	END = 2'b11
} estado_mmm_t;

// Valores pre-calculados
parameter logic k = 12;
parameter logic q = 12'd3329;
parameter logic r = 13'd4096;
parameter logic r_inv = 12'd2704;
parameter logic q_invn_r = 12'd3327;

`endif
