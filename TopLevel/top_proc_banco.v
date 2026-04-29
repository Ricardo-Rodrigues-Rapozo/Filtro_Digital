module top_proc_banco(input clk, rst_geral, rst_proc,
			input signed [31:0] in0,
			output reg signed [31:0] out0, out1,
			output wire req_in,
			output wire [1:0]out_en
		 );
		 

reg signed [31:0] in_proc;

// Multiplex
always @(*)
begin
		case(req_in)
		1'b1: in_proc = in0;
		default : in_proc = 31'd0;
		endcase
end

wire signed [31:0] out_proc;


//Instancia do Processador
proc_banco proc_banco_inst(
								 .clk(clk),
								 .rst(rst_geral),
								 .in(in_proc),
								 .out(out_proc),
								 .req_in(req_in),
								 .out_en(out_en),
								 .itr(rst_proc)
								 );
always @(posedge clk)
begin
	if (rst_geral)
	begin
		out0 <= 32'd0;
		out1 <= 32'd0;
	end
	else
	begin
		if(out_en[0])
			out0 <= out_proc;
	end
	begin
		if(out_en[1])
			out1 <= out_proc;
	end
end

endmodule