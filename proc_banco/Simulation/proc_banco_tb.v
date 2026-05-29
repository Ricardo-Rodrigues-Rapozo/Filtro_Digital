`timescale 1ns/1ps

module proc_banco_tb();

// clock and reset generation -------------------------------------------------

reg clk, rst;

initial begin
    clk = 0;
    rst = 1;
    #10.000000;
    rst = 0;
end

always #5.000000 clk = ~clk;

// processor instance ---------------------------------------------------------

reg  signed [31:0] proc_io_in = 0;
wire signed [31:0] proc_io_out;
wire [0:0] proc_req_in;
wire [1:0] proc_out_en;

proc_banco proc(clk,rst,proc_io_in,proc_io_out,proc_req_in,proc_out_en);

// input ports ----------------------------------------------------------------

// port 0 variables
integer data_in_0;
reg signed [31:0] in_0 = 0;
reg req_in_0 = 0;

// open a file for reading on each port
initial begin
    data_in_0 = $fopen("C:/Users/Ricardo/Documents/Dissertacao/proc_banco/Simulation/input_0.txt", "r"); // place your input data in this file
end

// decode input ports
always @ (*) begin
    // port 0 decoding
    if (proc_req_in == 1) proc_io_in = in_0;
    req_in_0 = proc_req_in == 1;
end

// implement reading of the input data
integer scan_result;
always @ (negedge clk) begin  
    // reading port 0
    if (data_in_0 != 0 && proc_req_in == 1) scan_result = $fscanf(data_in_0, "%d", in_0);
end

// output ports ---------------------------------------------------------------

// port 0 variables
integer data_out_0;
reg signed [31:0] out_sig_0 = 0;
reg out_en_0 = 0;

// port 1 variables
integer data_out_1;
reg signed [31:0] out_sig_1 = 0;
reg out_en_1 = 0;

// open a file for writing on each port
initial begin
    data_out_0 = $fopen("C:/Users/Ricardo/Documents/Dissertacao/proc_banco/Simulation/output_0.txt", "w"); // check the output data in this file
    data_out_1 = $fopen("C:/Users/Ricardo/Documents/Dissertacao/proc_banco/Simulation/output_1.txt", "w"); // check the output data in this file
end

// decode output ports
always @ (*) begin
    // port 0 decoding
    if (proc_out_en == 1) out_sig_0 <= proc_io_out;
    out_en_0 = proc_out_en == 1;
    // port 1 decoding
    if (proc_out_en == 2) out_sig_1 <= proc_io_out;
    out_en_1 = proc_out_en == 2;
end

// implement writing to the file
always @ (posedge clk) begin
    // write to port 0
    if (out_en_0 == 1'b1) begin $fdisplay(data_out_0, "%0d", out_sig_0); $fflush(data_out_0); end
    // write to port 1
    if (out_en_1 == 1'b1) begin $fdisplay(data_out_1, "%0d", out_sig_1); $fflush(data_out_1); end
end

integer progress, chrys;

always @ (posedge clk) if (proc.valr10 == 353) begin
    $display("Info: end of program!");
    $fclose(progress);
    $finish;
end

// signal registration, progress bar and finish ------------------------------

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
        #2000.000000;
        $fdisplay(progress,"%0d",chrys);
        $fflush(progress);
    end

    $fclose(progress);
    $finish;

end

endmodule
