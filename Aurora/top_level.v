module top_level(input clk, rst_geral, rst_proc_interp,
			input  signed [31:0] in0_interp,
			output signed [31:0] out0_interp, 
			output signed [31:0] out1_interp,
			output signed [31:0] out2_interp,
			output signed [31:0] out3_interp,
			output signed [31:0] out4_interp,
			output signed [31:0] out0_banco,
			output        [4:0]  out_en_interp,
			output        [3:0]  out_en_banco
		 );

wire req_in_interp;

top_proc_interp top_proc_interp_inst(
			.clk(clk),
			.rst_geral(rst_geral), 
			.rst_proc(rst_proc_interp),
			.in0(in0_interp),
			.out0(out0_interp),
			.out1(out1_interp),
			.out2(out2_interp),
			.out3(out3_interp),
			.out4(out4_interp),
			.req_in(req_in_interp),
			.out_en(out_en_interp)

		 );
		 
//wire almost_empty;
wire signed[31:0] saida_fifo;
wire signed[31:0] saida_fifo_freq;
wire signed[31:0] out1_banco;
wire signed[31:0] out2_banco;
wire [7:0] usedw;
wire [1:0]req_in_banco;
wire rst_proc_banco;

myFIFO	#(.WORD(32), .LENGTH(256), .ALMOST(2))
	FIFO16x32_inst_my (
	.clk ( clk ),
	.data ( out0_interp ), // dado que entra na fifo 
	.rdreq ( req_in_banco[0] ), //  momento para exportar arquivo da fifo 
	.sclr ( rst_geral ),    // 
	.wrreq ( out_en_interp[0] ),
	.almost_empty (  ), // vai para 1 qu
	.empty (  ),
	.full (  ),
	.q (saida_fifo),  // saida da fifo 
	.usedw ( usedw )  // numero de dados que exisetm na fifo
	);



myFIFO	#(.WORD(32), .LENGTH(256), .ALMOST(2))
	FIFO16x32_freq (
	.clk ( clk ),
	.data ( out2_interp ), // dado que entra na fifo 
	.rdreq ( req_in_banco[1] ), //  momento para exportar arquivo da fifo 
	.sclr ( rst_geral ),    // 
	.wrreq ( out_en_interp[2] ),
	.almost_empty (  ), // vai para 1 qu
	.empty (  ),
	.full (  ),
	.q (saida_fifo_freq),  // saida da fifo 
	.usedw (  )  // numero de dados que exisetm na fifo
	);


maq_estados apelido_maq_estados(
			.clk(clk),
			.rst_geral(rst_geral), 
			.flag_proc_banco(out1_banco[0]),
           .usedw_fifo(usedw),
           .rst_proc_banco(rst_proc_banco)
		 );

top_proc_banco top_proc_banco_inst(
			.clk(clk),
			.rst_geral(rst_geral), 
			.rst_proc(rst_proc_banco),
			.in0(saida_fifo),
			.in1(saida_fifo_freq),
			.out0(out0_banco),
            .out1(out1_banco),
			.out2(out2_banco),
			.req_in(req_in_banco),
			.out_en(out_en_banco)
		 );

endmodule 
