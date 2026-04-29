`timescale 1ns/1ps

module top_level_tb();

// Variaveis da instancia
reg clk, rst_geral, rst_proc_interp;
reg [13:0] cont_rst_proc;
reg signed [31:0] data = 32'd0;
wire signed [31:0] out0_interp;
wire signed [31:0] out0_banco;
wire               out_en_interp;
wire        [1:0]  out_en_banco;


// Variaveis intermediarias para Leitura

// Clock
always #2 clk <= ~clk;

// Teste do reset
initial
fork
	clk <= 1'b0;
	rst_proc_interp <= 1'b0;
	rst_geral <= 1'b1;
	#40 rst_geral <= 1'b0;
join

integer i, data_in1,data_out_0,data_out_1;
initial begin
	//sempre que for simular na sua maquina colocar o caminho do arquivo que a simulação vai ler
	data_in1 = $fopen("C:\\Users\\S\\Documents\\Projeto_banco_quartus\\Projeto_banco\\TopLevel\\sinal_teste.txt", "r");
	data_out_1 = $fopen("C:\\Users\\S\\Documents\\Projeto_banco_quartus\\Projeto_banco\\TopLevel\\saida_banco.txt", "w");
	data_out_0 = $fopen("C:\\Users\\S\\Documents\\\Projeto_banco_quartus\\Projeto_banco\\TopLevel\\saida_interp.txt", "w");
end

integer scan_result;
always @(posedge clk)
begin
//	if (req_in[1] == 1'b1)
	if (rst_proc_interp)
	begin
		// Coloca o dado no barramento
		scan_result = $fscanf(data_in1, "%d", data);
	end
end

// Contador de reset proc
always@(posedge clk or posedge rst_geral)
begin
	if (rst_geral == 1'b1)
	begin
		cont_rst_proc <= 14'd0;
	end
	
	else 
	begin
		cont_rst_proc <= cont_rst_proc + 14'd1;
	end
	
end

always@(posedge clk)
begin
	if (cont_rst_proc == 14'd16383)
	begin
		rst_proc_interp <= 1'b1;
	end
	
	else 
	begin
		rst_proc_interp <= 1'b0;
	end
end
        
always@(posedge clk)
		begin
			if (out_en_interp == 1'b1) $fdisplay(data_out_0, "%0d", out0_interp);
			if (out_en_banco[0]  == 1'b1) $fdisplay(data_out_1, "%0d", out0_banco);
		end


top_level top_level_inst(

				
					          .clk(clk),
					          .rst_geral(rst_geral),
					          .rst_proc_interp(rst_proc_interp),
					          .out0_interp(out0_interp),
							  .out0_banco(out0_banco),
					          .in0_interp(data),
							  .out_en_interp(out_en_interp),
							  .out_en_banco(out_en_banco)   
					          );

integer progress, chrys;
initial begin
    $dumpfile("top_level_tb.vcd");
    $dumpvars(0, top_level_tb);
    progress = $fopen("C:\\Users\\S\\AppData\\Local\\Programs\\aurora-ide\\saphoComponents\\Temp\\progress.txt", "w");
    for (chrys = 10; chrys <= 100; chrys = chrys + 10) begin
        #200000;
        $fdisplay(progress,"%0d",chrys);
        $fflush(progress);
    end
    $fclose(progress);
    $finish;
end



endmodule 