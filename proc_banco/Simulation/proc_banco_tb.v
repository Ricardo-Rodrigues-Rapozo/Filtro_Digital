`timescale 1ns/1ps

module proc_banco_tb();

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
wire [1:0] proc_out_en;

proc_banco proc(clk,rst,proc_io_in,proc_io_out,proc_req_in,proc_out_en,1'b0);

// portas de entrada ----------------------------------------------------------

// variaveis da porta 0
integer data_in_0;
reg signed [31:0] in_0 = 0;
reg req_in_0 = 0;

// abre um arquivo para leitura em cada porta
initial begin
    data_in_0 = $fopen("C:/Users/S/Documents/Projeto_banco_quartus/Projeto_banco/proc_banco/Simulation/input_0.txt", "r"); // coloque os seus dados de entrada neste arquivo
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

// variaveis da porta 1
integer data_out_1;
reg signed [31:0] out_sig_1 = 0;
reg out_en_1 = 0;

// abre um arquivo para escrita de cada porta
initial begin
    data_out_0 = $fopen("C:/Users/S/Documents/Projeto_banco_quartus/Projeto_banco/proc_banco/Simulation/output_0.txt", "w"); // veja os dados de saida neste arquivo
    data_out_1 = $fopen("C:/Users/S/Documents/Projeto_banco_quartus/Projeto_banco/proc_banco/Simulation/output_1.txt", "w"); // veja os dados de saida neste arquivo
end

// decodifica portas de saida
always @ (*) begin
    // decodificacao da porta 0
    if (proc_out_en == 1) out_sig_0 <= proc_io_out;
    out_en_0 = proc_out_en == 1;
    // decodificacao da porta 1
    if (proc_out_en == 2) out_sig_1 <= proc_io_out;
    out_en_1 = proc_out_en == 2;
end

// implementa escrita no arquivo
always @ (posedge clk) begin
    // escreve na porta 0
    if (out_en_0 == 1'b1) $fdisplay(data_out_0, "%0d", out_sig_0);
    // escreve na porta 1
    if (out_en_1 == 1'b1) $fdisplay(data_out_1, "%0d", out_sig_1);
end

// cadastro de sinais, barra de progresso e finish ----------------------------

integer progress, chrys;
initial begin

    $dumpfile("proc_banco_tb.vcd");

    $dumpvars(0,proc_banco_tb.clk);
    $dumpvars(0,proc_banco_tb.rst);
    $dumpvars(0,proc_banco_tb.proc.req_in_sim_0);
    $dumpvars(0,proc_banco_tb.proc.in_sim_0);
    $dumpvars(0,proc_banco_tb.proc.out_en_sim_0);
    $dumpvars(0,proc_banco_tb.proc.out_sig_0);
    $dumpvars(0,proc_banco_tb.proc.out_en_sim_1);
    $dumpvars(0,proc_banco_tb.proc.out_sig_1);
    $dumpvars(0,proc_banco_tb.proc.valr2);
    $dumpvars(0,proc_banco_tb.proc.linetabs);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_sample_count_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_output_count_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_M_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_fft_limit_e_);
    $dumpvars(0,proc_banco_tb.proc.me2_f_main_v_vector_count_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_k_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_mm_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_mmax_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_istep_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_m_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_ind_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_sind_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_q_e_);
    $dumpvars(0,proc_banco_tb.proc.me1_f_main_v_j_e_);
    $dumpvars(0,proc_banco_tb.proc.comp_me3_f_main_v_temp_e_);
    $dumpvars(0,proc_banco_tb.proc.p_proc_banco.core.sp.pointeri);
    $dumpvars(0,proc_banco_tb.proc.p_proc_banco.core.sp.fl_max);
    $dumpvars(0,proc_banco_tb.proc.p_proc_banco.core.sp.fl_full);
    $dumpvars(0,proc_banco_tb.proc.p_proc_banco.core.ula.delta_float);
    $dumpvars(0,proc_banco_tb.proc.p_proc_banco.core.ula.delta_int);

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
