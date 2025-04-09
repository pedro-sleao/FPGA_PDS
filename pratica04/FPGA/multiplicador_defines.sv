`ifndef MULTIPLICADOR_DEFINES_V
`define MULTIPLICADOR_DEFINES_V

`define CONTROL_ADDR 0
`define NUMBERS_ADDR 1
`define RESULT_ADDR 2'b10
`define STATUS_ADDR 2'b11

typedef enum logic [2:0] {
   ST_IDLE = 3'b000, 
	ST_BIT0 = 3'b001,
	ST_BIT1 = 3'b011,
	ST_BIT2 = 3'b010,
	ST_BIT3 = 3'b110,
	ST_END = 3'b111
} estado_mult_t;

typedef enum logic [2:0] {
   ST_RAM_IDLE = 3'b000, 
	ST_RAM_READ_NUMBERS,
	ST_RAM_INIT_CALC,
	ST_RAM_WAIT_CALC,
	ST_RAM_STORE_RESULT,
	ST_RAM_END_CALC,
	ST_RAM_WAIT_CONTROL,
	ST_RAM_RESET_STATUS
} estado_ram_t;

`endif
