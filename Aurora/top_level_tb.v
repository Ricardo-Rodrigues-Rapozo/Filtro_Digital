`timescale 1ns/1ps

module top_level_tb();

// Variaveis da instancia
reg clk, rst_geral;
reg [31:0] cont_rst_proc, cnt_amostras;
reg signed [31:0] data = 32'd0;
wire signed [31:0] out0_interp,out1_interp,out2_interp,out3_interp,out4_interp;
wire signed [31:0] out0_banco;
wire signed [31:0] out2_banco;
wire        [4:0]  out_en_interp;
wire        [3:0]  out_en_banco;


// Variaveis intermediarias para Leitura

// Clock
always #2 clk <= ~clk;


initial
fork
	clk <= 1'b0;
	rst_geral <= 1'b1;
	#40 rst_geral <= 1'b0;
	#480000000 $finish; // outros testes
	//#420000000 $finish; // outros testes
	//#120000000 $finish; // outros testes

	$display ("termionou");
	// off-nominal e modulações fm=5 ou fm=0.5
                  //#220000000 $finish;

// rampa M class 55 -> 65 Hz
                  //#420000000 $finish;

// rampa subida + descida
#7987200000 $finish;
join

integer i, data_in1,data_out_interp0, data_out_interp1, data_out_interp2, data_out_interp3, data_out_interp4, data_out_banco0,data_out_banco2;//,data_out_1;
initial begin
	//sempre que for simular na sua maquina colocar o caminho do arquivo que a simulação vai ler
	data_in1 = $fopen("C:\\Users\\Ricardo\\Documents\\Dissertacao\\Aurora\\dados_simulacao\\sinal_teste.txt", "r");
	data_out_interp0 = $fopen("C:\\Users\\Ricardo\\Documents\\Dissertacao\\Aurora\\dados_simulacao\\saida_interp0.txt", "w");
	data_out_interp1 = $fopen("C:\\Users\\Ricardo\\Documents\\Dissertacao\\Aurora\\dados_simulacao\\saida_interp1.txt", "w");
	data_out_interp2 = $fopen("C:\\Users\\Ricardo\\Documents\\Dissertacao\\Aurora\\dados_simulacao\\saida_interp2.txt", "w");
	data_out_interp3 = $fopen("C:\\Users\\Ricardo\\Documents\\Dissertacao\\Aurora\\dados_simulacao\\saida_interp3.txt", "w");
	data_out_interp4 = $fopen("C:\\Users\\Ricardo\\Documents\\Dissertacao\\Aurora\\dados_simulacao\\saida_interp4.txt", "w");
	data_out_banco0  = $fopen("C:\\Users\\Ricardo\\Documents\\Dissertacao\\Aurora\\dados_simulacao\\saida_banco0.txt", "w");
	data_out_banco2  =
	$fopen("C:\\Users\\Ricardo\\Documents\\Dissertacao\\Aurora\\dados_simulacao\\saida_banco2.txt", "w");
end

integer scan_result;
always @(negedge clk)
begin
	if (data_in1 != 0 && top_level_inst.req_in_interp)
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
		cont_rst_proc <= 32'd0;
	end
	
	else 
	begin
		if(cont_rst_proc < 32'd1000)   // tempo de processamento do código interp.cmm
			cont_rst_proc <= cont_rst_proc + 32'd1;
		else
			cont_rst_proc <= 32'd0;
	end
	
end

wire rst_proc_interp = (cont_rst_proc == 32'd999) ? 1 : 0;

always@(posedge clk)
begin
	if (rst_geral == 1'b1)
		cnt_amostras <= 32'd0;
	else
		if(rst_proc_interp)
			cnt_amostras <= cnt_amostras + 32'd1;
end
        
always@(posedge clk)
		begin
			if (out_en_interp[0] == 1'b1) $fdisplay(data_out_interp0, "%0d", out0_interp);
			if (out_en_interp[1] == 1'b1) $fdisplay(data_out_interp1, "%0d", out1_interp);
			if (out_en_interp[2] == 1'b1) $fdisplay(data_out_interp2, "%0d", out2_interp);
			if (out_en_interp[3] == 1'b1) $fdisplay(data_out_interp3, "%0d", out3_interp);
			if (out_en_interp[4] == 1'b1) $fdisplay(data_out_interp4, "%0d", out4_interp);
			if (out_en_banco[0] == 1'b1) $fdisplay(data_out_banco0, "%0d", out0_banco);
		    if (out_en_banco[2] == 1'b1) $fdisplay(data_out_banco2, "%0d", out2_banco);

		end


top_level top_level_inst(
						.clk(clk),
						.rst_geral(rst_geral),
						.rst_proc_interp(rst_proc_interp),
						.in0_interp(data),
						.out0_interp(out0_interp),
						.out1_interp(out1_interp),
						.out2_interp(out2_interp),
						.out3_interp(out3_interp),
						.out4_interp(out4_interp),					          
						.out_en_interp(out_en_interp),
						.out0_banco(out0_banco),
						.out2_banco(out2_banco),
						.out_en_banco(out_en_banco)
						);


endmodule 
