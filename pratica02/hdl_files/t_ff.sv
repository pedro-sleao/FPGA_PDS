module t_ff (
	input clk_i,
	input rstn_i,
	input t_i,
	output reg q_o
);

always @ (posedge clk_i) begin
 if (!rstn_i)
	q_o <= 0;
 else
	if (t_i)
			q_o <= ~q_o;
	else
			q_o <= q_o;
end

endmodule
