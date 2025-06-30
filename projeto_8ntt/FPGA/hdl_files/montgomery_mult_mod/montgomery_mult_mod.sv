//----------------------------------------------------------------------------- 
// Descrição: Multiplicação de Montgomery utilizando o algoritmo descrito no artigo 
//            2023 Conceptual_Review_on_Number_Theoretic_Transform_and_Comprehensive_Review_on_Its_Implementations 
//----------------------------------------------------------------------------- 

`include "./montgomery_mult_mod_defines.sv"

module montgomery_mult_mod (
    input  clk,
    input  rst,
    input  start,
    input  [k-1:0] a,
    input  [k-1:0] b,
    output [k-1:0] result,
    output done
);

// INTERNAL REGS ###################### 
reg [2*k-1:0] am, bm, t, u, cm;
reg [k-1:0] c;
reg done_reg;

// INTERNAL SIGNALS ###################
estado_mmm_t state, next_state;

always @(posedge clk or negedge rst) begin
	if (rst == 1'b0)
		state <= IDLE;
	else
		state <= next_state;
end

always @(*) begin
	case (state)
		IDLE: next_state = start ? CONVERT : IDLE;
		CONVERT: next_state = MULTIPLY;
		MULTIPLY: next_state = END;
		END: next_state = !start ? IDLE : END;
		default: next_state = IDLE;
	endcase
end

always @(posedge clk or negedge rst) begin
	if (rst == 1'b0) begin
		am <= 0;
		bm <= 0;
		t <= 0;
		u <= 0;
		cm <= 0;
		c <= 0;
		done_reg <= 0;
	end else begin
		case (state)
			 IDLE: begin
				  done_reg <= 0;
			 end

			 CONVERT: begin
				  am = (a << k) % q;   // a * R mod q
				  bm = (b << k) % q;   // b * R mod q
			 end

			 MULTIPLY: begin
				  t = am * bm; 
				  u = (t * q_invn_r) & (r - 1); // mod R
				  cm = (t + u * q) >> k;
			 end

			 END: begin
				  c <= (cm * r_inv) % q; // volta para domínio normal
				  done_reg <= 1;
			 end
		endcase
	end
end

// Saidas
assign done = done_reg;
assign result = c;
	 
endmodule

