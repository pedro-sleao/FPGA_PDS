`include "./hdl_files/multiplicador_defines.sv"

module controlador
(
    input          clk_i,
    input          rst_i,
    input          strt_cmpt_i,      
    output [2:0]   state_o
);

// INTERNAL SIGNALS ################################

estado_t  state, next_state;

assign state_o = state;

// INTERNAL LOGIC ##################################

//#################### SEQUENTIAL LOGIC

    // state update and reset
    always @(posedge clk_i, negedge rst_i) 
	 begin
        if (rst_i == 1'b0)
            state <= ST_IDLE;
        else
            state <= next_state;
    end

    // transiction logic
    always @(strt_cmpt_i, state) begin
        case (state)
            ST_IDLE:
            begin
                if(strt_cmpt_i)
                    next_state   <=  ST_BIT0;
                else
                    next_state   <=  ST_IDLE;
            end    
            ST_BIT0:
            begin   
					 next_state   <=  ST_BIT1;
            end
            
            ST_BIT1:
				begin		  
					 next_state   <=  ST_BIT2;
				end
				ST_BIT2:
				begin
					 next_state   <=  ST_BIT3;
				end
			   ST_BIT3:
				begin
					 next_state   <=  ST_END;
				end
				ST_END:
				begin
					 if (strt_cmpt_i == 1'b0)
					 begin
						  next_state <= ST_IDLE;
					 end
					 else
					 begin
						  next_state <= ST_END;
					 end
				end
            default: 
            begin   
                next_state     <= ST_IDLE;
            end
        endcase
    end

endmodule
