module toplevel_placa(
							input clk_50,
							input rst_n,
							output teste
);

wire clk;
wire locked_pll;


pll pll (
		  .refclk(clk_50),   //  refclk.clk
		  .rst(~rst_n),      //   reset.reset
		  .outclk_0(clk), // outclk0.clk
		  .locked(locked_pll)    //  locked.export
	);


wire rst_geral = ~(rst_n & locked_pll);

wire sampling;

rst_proc rst_proc(
					  .clk(clk), 
					  .rst_geral(rst_geral),
					  .sampling(sampling)
					  );
					  
wire signed [15:0] input_signal_mem;

sinal_memoria #(.DATA_WIDTH(16), 
					 .ADDR_WIDTH(8)
					)
					(
					.clk(clk), 
					.rst_geral(rst_geral), 
					.sampling(sampling),
					.signal(input_signal_mem)
					);

wire signed [31:0] out0_interp, out1_interp, out2_interp, out3_interp, out4_interp, out0_banco;

assign teste = |(out0_interp|out1_interp|out2_interp|out3_interp|out4_interp|out0_banco);
					
wire signed [31:0] input_signal = input_signal_mem;

top_level top_level(
						 .clk(clk), 
						 .rst_geral(rst_geral), 
						 .rst_proc_interp(sampling),
			          .in0_interp(input_signal),
			          .out0_interp(out0_interp), 
			          .out1_interp(out1_interp),
			          .out2_interp(out2_interp),
			          .out3_interp(out3_interp),
			          .out4_interp(out4_interp),
			          .out0_banco(out0_banco)
			          //.out_en_interp(),
			          //.out_en_banco() 
		 );


endmodule 