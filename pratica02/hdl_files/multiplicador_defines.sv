`ifndef MULTIPLICADOR_DEFINES_V
`define MULTIPLICADOR_DEFINES_V

typedef enum logic [2:0] {
   ST_IDLE = 3'b000, 
	ST_BIT0 = 3'b001,
	ST_BIT1 = 3'b011,
	ST_BIT2 = 3'b010,
	ST_BIT3 = 3'b110,
	ST_END = 3'b111
} estado_t;

`endif
