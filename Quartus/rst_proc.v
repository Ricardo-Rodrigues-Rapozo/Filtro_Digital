module rst_proc(
					input clk, rst_geral,
					output sampling
					);

// Contador de reset proc
reg [31:0] cont_rst_proc;

always@(posedge clk or posedge rst_geral)
begin
	if (rst_geral == 1'b1)
	begin
		cont_rst_proc <= 32'd0;
	end
	
	else 
	begin
		if(cont_rst_proc < 32'd650)   // tempo de processamento do código interp.cmm
			cont_rst_proc <= cont_rst_proc + 32'd1;
		else
			cont_rst_proc <= 32'd0;
	end
	
end

assign sampling = (cont_rst_proc == 32'd649) ? 1'b1 : 1'b0;

endmodule 