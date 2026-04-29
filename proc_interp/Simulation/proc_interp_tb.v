`timescale 1ns/1ps

module proc_interp_tb();

// geracao de clock e reset ---------------------------------------------------

reg clk, rst;

initial begin
    clk = 0;
    rst = 1;
    #1000.000000;
    rst = 0;
end

always #500.000000 clk = ~clk;

// instancia do processador ---------------------------------------------------

reg  signed [31:0] proc_io_in = 0;
wire signed [31:0] proc_io_out;
wire [0:0] proc_req_in;
wire [0:0] proc_out_en;

proc_interp proc(clk,rst,proc_io_in,proc_io_out,proc_req_in,proc_out_en,1'b0);

// portas de entrada ----------------------------------------------------------

// variaveis da porta 0
integer data_in_0;
reg signed [31:0] in_0 = 0;
reg req_in_0 = 0;

// abre um arquivo para leitura em cada porta
initial begin
    data_in_0 = $fopen("C:/Users/S/Documents/Projeto_banco_quartus/Projeto_banco/proc_interp/Simulation/input_0.txt", "r"); // coloque os seus dados de entrada neste arquivo
end

// decodifica portas de entrada
always @ (*) begin
    // decodificacao da porta 0
    if (proc_req_in == 1) proc_io_in = in_0;
    req_in_0 = proc_req_in == 1;
end

// implementa a leitura dos dados de entrada
integer scan_result;
always @ (negedge clk) begin  
    // lendo a porta 0
    if (data_in_0 != 0 && proc_req_in == 1) scan_result = $fscanf(data_in_0, "%d", in_0);
end

// portas de saida ------------------------------------------------------------

// variaveis da porta 0
integer data_out_0;
reg signed [31:0] out_sig_0 = 0;
reg out_en_0 = 0;

// abre um arquivo para escrita de cada porta
initial begin
    data_out_0 = $fopen("C:/Users/S/Documents/Projeto_banco_quartus/Projeto_banco/proc_interp/Simulation/output_0.txt", "w"); // veja os dados de saida neste arquivo
end

// decodifica portas de saida
always @ (*) begin
    // decodificacao da porta 0
    if (proc_out_en == 1) out_sig_0 <= proc_io_out;
    out_en_0 = proc_out_en == 1;
end

// implementa escrita no arquivo
always @ (posedge clk) begin
    // escreve na porta 0
    if (out_en_0 == 1'b1) $fdisplay(data_out_0, "%0d", out_sig_0);
end

// cadastro de sinais, barra de progresso e finish ----------------------------

integer progress, chrys;
initial begin

    $dumpfile("proc_interp_tb.vcd");

    $dumpvars(0,proc_interp_tb.clk);
    $dumpvars(0,proc_interp_tb.rst);
    $dumpvars(0,proc_interp_tb.proc.req_in_sim_0);
    $dumpvars(0,proc_interp_tb.proc.in_sim_0);
    $dumpvars(0,proc_interp_tb.proc.out_en_sim_0);
    $dumpvars(0,proc_interp_tb.proc.out_sig_0);
    $dumpvars(0,proc_interp_tb.proc.valr2);
    $dumpvars(0,proc_interp_tb.proc.linetabs);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_alfa_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_cnt_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_x_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_dot_result_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_freq_smoothed_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_lambda_val_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_y_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_H0_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_H1_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_H2_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_H3_e_);
    $dumpvars(0,proc_interp_tb.proc.p_proc_interp.core.sp.pointeri);
    $dumpvars(0,proc_interp_tb.proc.p_proc_interp.core.sp.fl_max);
    $dumpvars(0,proc_interp_tb.proc.p_proc_interp.core.sp.fl_full);
    $dumpvars(0,proc_interp_tb.proc.p_proc_interp.core.ula.delta_float);
    $dumpvars(0,proc_interp_tb.proc.p_proc_interp.core.ula.delta_int);

    progress = $fopen("progress.txt", "w");
    for (chrys = 10; chrys <= 100; chrys = chrys + 10) begin
        #3000000000.000000;
        $fdisplay(progress,"%0d",chrys);
        $fflush(progress);
    end

    $fclose(progress);
    $finish;

end

endmodule
