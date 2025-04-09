`include "./multiplicador_defines.sv"

module controlador_ram
(
    input          clk_i,
    input          rst_i,
	 input          control_i,
	 input          end_mult_i,
    output [2:0]   state_o
);

// INTERNAL SIGNALS ################################

estado_ram_t  state, next_state;

assign state_o = state;

// INTERNAL LOGIC ##################################

//#################### SEQUENTIAL LOGIC

    // state update and reset
    always @(posedge clk_i, negedge rst_i) 
	 begin
        if (rst_i == 1'b0)
            state <= ST_RAM_IDLE;
        else
            state <= next_state;
    end

    // transiction logic
    always @(control_i, end_mult_i, state) begin
        case (state)
            ST_RAM_IDLE:
            begin
                if(control_i)
                    next_state   <=  ST_RAM_READ_NUMBERS;
                else
                    next_state   <=  ST_RAM_IDLE;
            end    
            ST_RAM_READ_NUMBERS:
            begin   
					 next_state   <=  ST_RAM_INIT_CALC;
            end
            
            ST_RAM_INIT_CALC:
				begin		  
					 next_state   <=  ST_RAM_WAIT_CALC;
				end
				ST_RAM_WAIT_CALC:
				begin
					 if(end_mult_i)
                    next_state   <=  ST_RAM_STORE_RESULT;
                else
                    next_state   <=  ST_RAM_WAIT_CALC;
				end
			   ST_RAM_STORE_RESULT:
				begin
					 next_state   <=  ST_RAM_END_CALC;
				end
				ST_RAM_END_CALC:
				begin
					 next_state   <=  ST_RAM_WAIT_CONTROL;
				end
				ST_RAM_WAIT_CONTROL:
				begin
					 if(control_i)
                    next_state   <=  ST_RAM_WAIT_CONTROL;
                else
                    next_state   <=  ST_RAM_RESET_STATUS;
				end
				ST_RAM_RESET_STATUS:
				begin
					 next_state   <=  ST_RAM_IDLE;
				end
            default: 
            begin   
                next_state     <= ST_RAM_IDLE;
            end
        endcase
    end

endmodule
