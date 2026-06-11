`timescale 1ns/1ps

module proc_interp_tb();

// clock and reset generation -------------------------------------------------

reg clk, rst;

initial begin
    clk = 0;
    rst = 1;
    #1000.000000;
    rst = 0;
end

always #500.000000 clk = ~clk;

// processor instance ---------------------------------------------------------

reg  signed [31:0] proc_io_in = 0;
wire signed [31:0] proc_io_out;
wire [0:0] proc_req_in;
wire [4:0] proc_out_en;

proc_interp proc(clk,rst,proc_io_in,proc_io_out,proc_req_in,proc_out_en,1'b0);

// input ports ----------------------------------------------------------------

// port 0 variables
integer data_in_0;
reg signed [31:0] in_0 = 0;
reg req_in_0 = 0;

// open a file for reading on each port
initial begin
    data_in_0 = $fopen("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Simulation/input_0.txt", "r"); // place your input data in this file
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

// port 2 variables
integer data_out_2;
reg signed [31:0] out_sig_2 = 0;
reg out_en_2 = 0;

// port 3 variables
integer data_out_3;
reg signed [31:0] out_sig_3 = 0;
reg out_en_3 = 0;

// port 4 variables
integer data_out_4;
reg signed [31:0] out_sig_4 = 0;
reg out_en_4 = 0;

// open a file for writing on each port
initial begin
    data_out_0 = $fopen("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Simulation/output_0.txt", "w"); // check the output data in this file
    data_out_1 = $fopen("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Simulation/output_1.txt", "w"); // check the output data in this file
    data_out_2 = $fopen("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Simulation/output_2.txt", "w"); // check the output data in this file
    data_out_3 = $fopen("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Simulation/output_3.txt", "w"); // check the output data in this file
    data_out_4 = $fopen("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Simulation/output_4.txt", "w"); // check the output data in this file
end

// decode output ports
always @ (*) begin
    // port 0 decoding
    if (proc_out_en == 1) out_sig_0 <= proc_io_out;
    out_en_0 = proc_out_en == 1;
    // port 1 decoding
    if (proc_out_en == 2) out_sig_1 <= proc_io_out;
    out_en_1 = proc_out_en == 2;
    // port 2 decoding
    if (proc_out_en == 4) out_sig_2 <= proc_io_out;
    out_en_2 = proc_out_en == 4;
    // port 3 decoding
    if (proc_out_en == 8) out_sig_3 <= proc_io_out;
    out_en_3 = proc_out_en == 8;
    // port 4 decoding
    if (proc_out_en == 16) out_sig_4 <= proc_io_out;
    out_en_4 = proc_out_en == 16;
end

// implement writing to the file
always @ (posedge clk) begin
    // write to port 0
    if (out_en_0 == 1'b1) begin $fdisplay(data_out_0, "%0d", out_sig_0); $fflush(data_out_0); end
    // write to port 1
    if (out_en_1 == 1'b1) begin $fdisplay(data_out_1, "%0d", out_sig_1); $fflush(data_out_1); end
    // write to port 2
    if (out_en_2 == 1'b1) begin $fdisplay(data_out_2, "%0d", out_sig_2); $fflush(data_out_2); end
    // write to port 3
    if (out_en_3 == 1'b1) begin $fdisplay(data_out_3, "%0d", out_sig_3); $fflush(data_out_3); end
    // write to port 4
    if (out_en_4 == 1'b1) begin $fdisplay(data_out_4, "%0d", out_sig_4); $fflush(data_out_4); end
end

integer progress, chrys;

always @ (posedge clk) if (proc.valr10 == 780) begin
    $display("Info: end of program!");
    $fclose(progress);
    $finish;
end

// signal registration, progress bar and finish ------------------------------

initial begin

    $dumpfile("proc_interp_tb.vcd");

    $dumpvars(0,proc_interp_tb.clk);
    $dumpvars(0,proc_interp_tb.rst);
    $dumpvars(0,proc_interp_tb.proc.req_in_sim_0);
    $dumpvars(0,proc_interp_tb.proc.in_sim_0);
    $dumpvars(0,proc_interp_tb.proc.out_en_sim_0);
    $dumpvars(0,proc_interp_tb.proc.out_sig_0);
    $dumpvars(0,proc_interp_tb.proc.out_en_sim_1);
    $dumpvars(0,proc_interp_tb.proc.out_sig_1);
    $dumpvars(0,proc_interp_tb.proc.out_en_sim_2);
    $dumpvars(0,proc_interp_tb.proc.out_sig_2);
    $dumpvars(0,proc_interp_tb.proc.out_en_sim_3);
    $dumpvars(0,proc_interp_tb.proc.out_sig_3);
    $dumpvars(0,proc_interp_tb.proc.out_en_sim_4);
    $dumpvars(0,proc_interp_tb.proc.out_sig_4);
    $dumpvars(0,proc_interp_tb.proc.valr2);
    $dumpvars(0,proc_interp_tb.proc.linetabs);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_teste0_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_cont_global_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_teste_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_b_index_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_k_idx_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_acc_b_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_acc_a_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_va_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_Tsc_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_T1_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_fzc_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_freq_amostragem_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_sig_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_Nb_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_T2_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_atraso_amotras_filtro_pre_zc_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_w_coeff_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_w_index_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_w_sum_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_buffer_media_movel_idex_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_fcc_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_w_media_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_read_idx_mean_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_w_index_mean_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_p_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_b_index_mean_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_atraso_amotras_media_movel_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_fvelho_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_freq_kalman_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_df_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_p00_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_p01_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_p10_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_p11_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_q00_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_q01_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_q10_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_q11_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_freq_pred_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_df_pred_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_R_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_cont_kalman_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_descarte_kalman_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_j_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_read_idx_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_acc_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_freq_instant_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_Tsc_total_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_denom_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_ESCALA_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_x_atrasado_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_c_index_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_read_c_idx_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_atraso_geral_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_alfa_e_);
    $dumpvars(0,proc_interp_tb.proc.me1_f_main_v_cnt_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_x_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_Ts_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_p00_pred_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_p01_pred_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_p10_pred_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_p11_pred_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_y_kalman_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_erro_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_S_incerteza_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_K0_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_K1_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_dot_result_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_freq_smoothed_e_);
    $dumpvars(0,proc_interp_tb.proc.me2_f_main_v_freq_atrasada_e_);
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
        #9000000.000000;
        $fdisplay(progress,"%0d",chrys);
        $fflush(progress);
    end

    $fclose(progress);
    $finish;

end

endmodule
