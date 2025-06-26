`include "./dp_ram_defines.sv"

module dp_ram
    #(      
        parameter  BUS_WIDTH  = 1,
        parameter  DATA_WIDTH = 160,
        parameter  BE_WIDTH   = 10
    )
    (
    //Common signal:
    input clk, 
    input reset, 
    //Wishbone interface:
    input  [BUS_WIDTH-1:0]  adr_i,  //Address In
    input  [DATA_WIDTH-1:0] data_i, //Data In
    output [DATA_WIDTH-1:0] data_o, //Data Out
    input                   we_i,   //Write Enable In
    input  [BE_WIDTH-1:  0] sel_i,  //Select Input array
    input                   stb_i,  //Strobe In
    output                  ack_o,  //Acknowledged Out
    input                   cyc_i,  //Cycle Output
    output [4:0]            status_o,
    //NTT:
	 output [11:0] 			 A_o[7:0],
    output       				 en_o,
    input  [7:0]            Y_i,
    input                   fim_i
    ); 

// Sinais do registrador de controle
wire dpram_control_reg_i_w;
wire dpram_control_reg_o_w;

// Logica de atualizacao do registrador de controle
assign dpram_control_reg_i_w = (we_i && sel_i[`SEL_CONTROL_BIT])? data_i[0]: dpram_control_reg_o_w;

registrador
	#(
	.DATA_WIDTH(1)
	)
	control_reg_inst2
		(
		.clk (clk),
		.reset (reset),
		.data_i (dpram_control_reg_i_w),
		.data_o (dpram_control_reg_o_w)
		);
		
// Registradores dos numeros
reg [11:0] A[7:0];

// Sinais dos registradores dos numeros
wire [11:0] A_i_w[7:0];

// Logica de atualizacao dos resgistradores dos numeros
genvar j;
generate
	for (j = 0; j < 8; j = j + 1) begin: regs_w
		assign A_i_w[j] = (we_i && sel_i[`SEL_DATA_IN_BIT])? data_i[((j+2)*16)-1:(j+1)*16]: A[j];
	end
endgenerate

// Atualizacao dos registradores
integer i;
always @(posedge clk, negedge reset)
begin
	if (reset == 1'b0)
	begin
		for (i = 0; i < 8; i = i + 1)
			A[i] <= 12'd0;
	end
	else
	begin
		for (i = 0; i < 8; i = i + 1)
			A[i] <= A_i_w[i];
	end
end

// Saida
assign A_o = A;
assign en_o = dpram_control_reg_o_w;
assign data_o = {15'd0,fim_i,4'd0,A[7],4'd0,A[6],4'd0,A[5],4'd0,A[4],4'd0,A[3],4'd0,A[2],4'd0,A[1],4'd0,A[0],15'd0,dpram_control_reg_o_w};

endmodule
