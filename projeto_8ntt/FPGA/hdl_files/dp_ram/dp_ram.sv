`include "./dp_ram_defines.sv"

module dp_ram
    #(      
        parameter  BUS_WIDTH  = 5,
        parameter  DATA_WIDTH = 16,
        parameter  BE_WIDTH   = 2
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
    input  [11:0]           Y_i[16:9],
    input                   fim_estagio1_i,
	 input                   fim_estagio2_i
    ); 

// Registradores dos numeros e de controle
reg [11:0] A[8:1];
reg dpram_control_reg;

// Atualizacao dos registradores
integer i;
always @(posedge clk, negedge reset)
begin
	if (reset == 1'b0)
	begin
		for (i = 1; i < 9; i = i + 1)
			A[i] <= 12'd0;
	end
	else
	begin
		if ((adr_i == 1'b0) && (we_i))
		begin
			dpram_control_reg <= data_i[0];
		end
		else
		begin
			if ((adr_i < 4'b1001) && (we_i))
			begin
				A[adr_i] <= data_i;
			end
		end
	end
end

// Saida
assign A_o = A;
assign en_o = dpram_control_reg;
assign data_o = (adr_i == 1'b0) ? {15'b0, dpram_control_reg} :
					 (adr_i < 4'b1001) ? {4'b0, A[adr_i]} : 
					 (adr_i < 5'b10001) ? {4'b0, Y_i[adr_i]} : 
					 (adr_i == 5'b10001) ? {15'b0, fim_estagio1_i} : {15'b0, fim_estagio2_i};
					 
endmodule
