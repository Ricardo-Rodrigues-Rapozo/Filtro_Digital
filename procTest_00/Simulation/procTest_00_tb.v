`timescale 1ns/1ps

module procTest_00_tb();

// geracao de clock e reset ---------------------------------------------------

reg clk, rst;

initial begin
    clk = 0;
    rst = 1;
    #100.000000;
    rst = 0;
end

always #50.000000 clk = ~clk;

// instancia do processador ---------------------------------------------------

reg  signed [22:0] proc_io_in = 0;
wire signed [22:0] proc_io_out;
wire [0:0] proc_req_in;
wire [1:0] proc_out_en;

procTest_00 proc(clk,rst,proc_io_in,proc_io_out,proc_req_in,proc_out_en);

// portas de entrada ----------------------------------------------------------

// variaveis da porta 0
integer data_in_0; // para ver no simulador
reg signed [22:0] in_0 = 0;
reg req_in_0 = 0;

// abre um arquivo para leitura em cada porta
initial begin
    data_in_0 = $fopen("C:/Users/Ricardo/Documents/Codigos_C/primeiro/procTest_00/Simulation/input_0.txt", "r"); // coloque os seus dados de entrada neste arquivo
end

// decodifica portas de entrada
always @ (*) begin
    // decodificacao da porta 0
    if (proc_req_in == 1) proc_io_in = in_0; // dado aparece no simulador
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
reg signed [22:0] out_sig_0 = 0; // para ver no simulador
reg out_en_0 = 0;

// abre um arquivo para escrita de cada porta
initial begin
    data_out_0 = $fopen("C:/Users/Ricardo/Documents/Codigos_C/primeiro/procTest_00/Simulation/output_0.txt", "w"); // veja os dados de saida neste arquivo
end

// decodifica portas de saida
always @ (*) begin
    // decodificacao da porta 0
    if (proc_out_en == 1) out_sig_0 <= proc_io_out; // dado aparece no simulador
    out_en_0 = proc_out_en == 1;
end

// implementa escrita no arquivo
always @ (posedge clk) begin
    // escreve na porta 0
    if (out_en_0 == 1'b1) $fdisplay(data_out_0, "%0d", out_sig_0);
end

// barra de progresso e finish ------------------------------------------------

integer progress, chrys;
initial begin

    $dumpfile("procTest_00_tb.vcd");
    $dumpvars(0,procTest_00_tb);

    progress = $fopen("progress.txt", "w");
    for (chrys = 10; chrys <= 100; chrys = chrys + 10) begin
        #1000000.000000;
        $fdisplay(progress,"%0d",chrys);
        $fflush(progress);
    end

    $fclose(progress);
    $finish;

end

endmodule
