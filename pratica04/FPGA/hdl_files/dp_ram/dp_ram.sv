`include "./dp_ram_defines.sv"

module dp_ram
    #(      
        parameter  BUS_WIDTH  = 1,
        parameter  DATA_WIDTH = 32,
        parameter  BE_WIDTH   = 4
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
    //Mult4bits:
	 output [3:0] 				 A_o,
    output [3:0] 				 B_o,
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

// Sinais do registrador de A e B
wire [7:0] AB_i_w;
wire [7:0] AB_o_w;

// Logica de atualizacao do resgistrador de A e B
assign AB_i_w = (we_i && sel_i[`SEL_DATA_IN_BIT])? data_i[17:8]: AB_o_w;

registrador
	#(
	.DATA_WIDTH(8)
	)
	AB_reg_inst
		(
		.clk (clk),
		.reset (reset),
		.data_i (AB_i_w),
		.data_o (AB_o_w)
		);

// Saida
assign A_o = AB_o_w[3:0];
assign B_o = AB_o_w[7:4];
assign en_o = dpram_control_reg_o_w;
assign data_o = {7'd0,fim_i,Y_i,AB_o_w,7'd0,dpram_control_reg_o_w};

endmodule
