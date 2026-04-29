module maq_estados
(
	input	clk, rst_geral, flag_proc_banco,
	input [3:0] usedw_fifo,
	output reg rst_proc_banco// out[1] o enable do registrador used_w - 1; out[0] o rst do proc dtw ;
);

	// Declare the state register to be "safe" to implement
	// a safe state machine that can recover gracefully from
	// an illegal state (by returning to the reset state).
	(* syn_encoding = "safe" *) reg [2:0] state;

	// Declare states
	parameter S0 = 0, S1 = 1, S2 = 2, S3=3, S4=4;

	// Output depends only on the state
	always @ (state) begin
		case (state)
			S0:
			    begin
				rst_proc_banco = 1'b0;
				end
			S1:
			    begin
				rst_proc_banco = 1'b0;
				end
			S2: 
			    begin
				rst_proc_banco = 1'b1;
				end
			S3:
			    begin
			    rst_proc_banco = 1'b0;
				end			
			default:
			    begin
				rst_proc_banco = 1'b0;
				end 
		endcase
	end

	// Determine the next state
	always @ (posedge clk or posedge rst_geral) begin
		if (rst_geral)
			state <= S0;
		else
			case (state)
				S0:    //que que o S0 faz? pula 1 clock
					if (flag_proc_banco==0)// o que é esse estimulo 
						state <= S1;
				S1:
				    if(usedw_fifo>=1)//ta o codigo da ultima vez ate o momento ate porque inverteu a ordem da ordem que a conferencia ta sendo executada
					    state <= S2;
				S2: 
					state <= S3;
				S3:
				    if(flag_proc_banco==1)
					state <= S0;
				   
			endcase
	end
endmodule
