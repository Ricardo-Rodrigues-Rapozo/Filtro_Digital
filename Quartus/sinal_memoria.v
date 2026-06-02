module sinal_memoria #(
							 parameter DATA_WIDTH = 16, 
							 parameter ADDR_WIDTH = 8)
							 (
							 input clk, rst_geral, sampling,
							 output reg [DATA_WIDTH-1:0] signal
							 );
							
// Memória
reg [DATA_WIDTH-1:0] rom[2**ADDR_WIDTH-1:0];
reg [ADDR_WIDTH-1:0] addr;

always @ (posedge clk or posedge rst_geral)
begin
	if(rst_geral)
		addr <= {ADDR_WIDTH{1'b0}};
	else if(sampling)
		addr <= addr + {{(ADDR_WIDTH-1){1'b0}}, 1'b1};
end

initial
begin
	$readmemb("sinal_entrada_quartus.txt", rom);
end

always @ (posedge clk)
begin
	signal <= rom[addr];
end



endmodule 