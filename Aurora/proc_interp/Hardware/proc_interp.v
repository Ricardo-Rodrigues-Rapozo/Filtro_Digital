module proc_interp (

input  clk, rst,
input  signed [31:0] in ,
output signed [31:0] out,
output [0:0] req_in,
output [4:0] out_en,
input  itr);

/* verilator tracing_off */

wire cheguei;
wire proc_req_in, proc_out_en;
wire [0:0] addr_in;
wire [2:0] addr_out;

`ifdef __ICARUS__
 `ifndef YANC_SIM_VIS
  `define YANC_SIM_VIS
 `endif
`endif
`ifdef YANC_TRACE
 `ifndef YANC_SIM_VIS
  `define YANC_SIM_VIS
 `endif
`endif

`ifdef YANC_SIM_VIS
wire mem_wr;
wire [9:0] mem_addr_wr;
wire [9:0] pc_sim_val;
`endif

processor#(.NUBITS(32),
.NBMANT(23),
.NBEXPO(8),
.NBOPER(10),
.NUGAIN(128),
.MDATAS(705),
.MINSTS(834),
.SDEPTH(5),
.DDEPTH(5),
.NBIOIN(1),
.NBIOOU(3),
.FFTSIZ(8),
.ITRADD(276),
.LOD(1),
.SET(1),
.P_LOD(1),
.STI(1),
.I2F_M(1),
.SF_DIV(1),
.P_I2F_M(1),
.SF_MLT(1),
.F_MLT(1),
.F_DIV(1),
.PF_NEG_M(1),
.INN(1),
.I2F(1),
.LDI(1),
.SF_ADD(1),
.SF_SU2(1),
.F_ADD(1),
.SF_LES(1),
.JIZ(1),
.F_SU1(1),
.F2I(1),
.OUT(1),
.LES(1),
.LIN(1),
.F_SU2(1),
.GRE(1),
.ADD(1),
.S_EQU(1),
.F_NEG(1),
.DFILE("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Hardware/proc_interp_data.mif"),
.IFILE("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Hardware/proc_interp_inst.mif"))

`ifdef YANC_SIM_VIS
p_proc_interp (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, cheguei, mem_wr, mem_addr_wr,pc_sim_val);
`else
p_proc_interp (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, cheguei);
`endif

assign req_in = proc_req_in;
addr_dec #(5) dec_out(proc_out_en, addr_out, out_en);

/* verilator tracing_on */

// ----------------------------------------------------------------------------
// Simulation -----------------------------------------------------------------
// ----------------------------------------------------------------------------

`ifdef YANC_SIM_VIS

// I/O ------------------------------------------------------------------------

reg signed [31:0] in_sim_0 = 0;
reg req_in_sim_0 = 0;

reg signed [31:0] out_sig_0 = 0;
reg out_en_sim_0 = 0;
reg signed [31:0] out_sig_1 = 0;
reg out_en_sim_1 = 0;
reg signed [31:0] out_sig_2 = 0;
reg out_en_sim_2 = 0;
reg signed [31:0] out_sig_3 = 0;
reg out_en_sim_3 = 0;
reg signed [31:0] out_sig_4 = 0;
reg out_en_sim_4 = 0;

always @ (posedge clk) begin
   if (req_in == 1) in_sim_0 <= in;
end
always @ (*) begin
   req_in_sim_0 = req_in == 1;
end

always @ (posedge clk) begin
   if (out_en == 1) out_sig_0 <= out;
   if (out_en == 2) out_sig_1 <= out;
   if (out_en == 4) out_sig_2 <= out;
   if (out_en == 8) out_sig_3 <= out;
   if (out_en == 16) out_sig_4 <= out;
end
always @ (*) begin
   out_en_sim_0 = out_en == 1;
   out_en_sim_1 = out_en == 2;
   out_en_sim_2 = out_en == 4;
   out_en_sim_3 = out_en == 8;
   out_en_sim_4 = out_en == 16;
end

// variables ------------------------------------------------------------------

/* verilator tracing_off */  // float decode helpers (not traced)
reg signed [23:0] sm_me2; always @ (*) sm_me2 = (out[31]) ? -$signed({1'b0, out[22:0]}) : $signed({1'b0, out[22:0]});
reg signed [7:0] e_me2; always @ (*)  e_me2 = $signed(out[30:23]);
/* verilator tracing_on */

reg [31:0] me1_f_main_v_teste0_e_ = 0;
reg [31:0] me1_f_main_v_cont_global_e_ = 0;
reg [31:0] me1_f_main_v_teste_e_ = 0;
reg [31:0] me1_f_main_v_b_index_e_ = 0;
reg [31:0] me1_f_main_v_k_idx_e_ = 0;
real me2_f_main_v_acc_b_e_ = 0.0;
real me2_f_main_v_acc_a_e_ = 0.0;
real me2_f_main_v_va_e_ = 0.0;
real me2_f_main_v_Tsc_e_ = 0.0;
real me2_f_main_v_T1_e_ = 0.0;
real me2_f_main_v_fzc_e_ = 0.0;
real me2_f_main_v_freq_amostragem_e_ = 0.0;
real me2_f_main_v_sig_e_ = 0.0;
real me2_f_main_v_Nb_e_ = 0.0;
real me2_f_main_v_T2_e_ = 0.0;
reg [31:0] me1_f_main_v_atraso_amotras_filtro_pre_zc_e_ = 0;
real me2_f_main_v_cont_zc_e_ = 0.0;
real me2_f_main_v_w_coeff_e_ = 0.0;
reg [31:0] me1_f_main_v_w_index_e_ = 0;
real me2_f_main_v_w_sum_e_ = 0.0;
reg [31:0] me1_f_main_v_buffer_media_movel_idex_e_ = 0;
real me2_f_main_v_fcc_e_ = 0.0;
reg [31:0] me1_f_main_v_w_media_e_ = 0;
reg [31:0] me1_f_main_v_read_idx_mean_e_ = 0;
reg [31:0] me1_f_main_v_w_index_mean_e_ = 0;
reg [31:0] me1_f_main_v_p_e_ = 0;
reg [31:0] me1_f_main_v_b_index_mean_e_ = 0;
reg [31:0] me1_f_main_v_atraso_amotras_media_movel_e_ = 0;
real me2_f_main_v_fvelho_e_ = 0.0;
real me2_f_main_v_f_nominal_e_ = 0.0;
real me2_f_main_v_dfreq_e_ = 0.0;
real me2_f_main_v_df_e_ = 0.0;
real me2_f_main_v_p00_e_ = 0.0;
real me2_f_main_v_p01_e_ = 0.0;
real me2_f_main_v_p10_e_ = 0.0;
real me2_f_main_v_p11_e_ = 0.0;
real me2_f_main_v_q00_e_ = 0.0;
real me2_f_main_v_q01_e_ = 0.0;
real me2_f_main_v_q10_e_ = 0.0;
real me2_f_main_v_q11_e_ = 0.0;
real me2_f_main_v_dfreq_pred_e_ = 0.0;
real me2_f_main_v_df_pred_e_ = 0.0;
real me2_f_main_v_R_e_ = 0.0;
reg [31:0] me1_f_main_v_cont_kalman_e_ = 0;
reg [31:0] me1_f_main_v_descarte_kalman_e_ = 0;
real me2_f_main_v_erro_e_ = 0.0;
real me2_f_main_v_comp_dfreq_e_ = 0.0;
reg [31:0] me1_f_main_v_j_e_ = 0;
reg [31:0] me1_f_main_v_read_idx_e_ = 0;
real me2_f_main_v_acc_e_ = 0.0;
real me2_f_main_v_freq_instant_e_ = 0.0;
real me2_f_main_v_Tsc_total_e_ = 0.0;
real me2_f_main_v_denom_e_ = 0.0;
real me2_f_main_v_ESCALA_e_ = 0.0;
real me2_f_main_v_x_atrasado_e_ = 0.0;
reg [31:0] me1_f_main_v_c_index_e_ = 0;
reg [31:0] me1_f_main_v_read_c_idx_e_ = 0;
reg [31:0] me1_f_main_v_atraso_geral_e_ = 0;
real me2_f_main_v_alfa_e_ = 0.0;
reg [31:0] me1_f_main_v_cnt_e_ = 0;
real me2_f_main_v_x_e_ = 0.0;
real me2_f_main_v_Ts_e_ = 0.0;
real me2_f_main_v_kah_u_e_ = 0.0;
real me2_f_main_v_kah_t_e_ = 0.0;
real me2_f_main_v_p00_pred_e_ = 0.0;
real me2_f_main_v_p01_pred_e_ = 0.0;
real me2_f_main_v_p10_pred_e_ = 0.0;
real me2_f_main_v_p11_pred_e_ = 0.0;
real me2_f_main_v_y_kalman_e_ = 0.0;
real me2_f_main_v_S_incerteza_e_ = 0.0;
real me2_f_main_v_K0_e_ = 0.0;
real me2_f_main_v_K1_e_ = 0.0;
real me2_f_main_v_dot_result_e_ = 0.0;
real me2_f_main_v_freq_smoothed_e_ = 0.0;
real me2_f_main_v_freq_atrasada_e_ = 0.0;
real me2_f_main_v_lambda_val_e_ = 0.0;
real me2_f_main_v_y_e_ = 0.0;
real me2_f_main_v_H0_e_ = 0.0;
real me2_f_main_v_H1_e_ = 0.0;
real me2_f_main_v_H2_e_ = 0.0;
real me2_f_main_v_H3_e_ = 0.0;

always @ (posedge clk) begin
   if (mem_addr_wr == 1 && mem_wr) me1_f_main_v_teste0_e_ <= out;
   if (mem_addr_wr == 3 && mem_wr) me1_f_main_v_cont_global_e_ <= out;
   if (mem_addr_wr == 4 && mem_wr) me1_f_main_v_teste_e_ <= out;
   if (mem_addr_wr == 44 && mem_wr) me1_f_main_v_b_index_e_ <= out;
   if (mem_addr_wr == 45 && mem_wr) me1_f_main_v_k_idx_e_ <= out;
   if (mem_addr_wr == 46 && mem_wr) me2_f_main_v_acc_b_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 47 && mem_wr) me2_f_main_v_acc_a_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 48 && mem_wr) me2_f_main_v_va_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 50 && mem_wr) me2_f_main_v_Tsc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 51 && mem_wr) me2_f_main_v_T1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 52 && mem_wr) me2_f_main_v_fzc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 54 && mem_wr) me2_f_main_v_freq_amostragem_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 55 && mem_wr) me2_f_main_v_sig_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 56 && mem_wr) me2_f_main_v_Nb_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 57 && mem_wr) me2_f_main_v_T2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 59 && mem_wr) me1_f_main_v_atraso_amotras_filtro_pre_zc_e_ <= out;
   if (mem_addr_wr == 60 && mem_wr) me2_f_main_v_cont_zc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 62 && mem_wr) me2_f_main_v_w_coeff_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 63 && mem_wr) me1_f_main_v_w_index_e_ <= out;
   if (mem_addr_wr == 64 && mem_wr) me2_f_main_v_w_sum_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 321 && mem_wr) me1_f_main_v_buffer_media_movel_idex_e_ <= out;
   if (mem_addr_wr == 322 && mem_wr) me2_f_main_v_fcc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 324 && mem_wr) me1_f_main_v_w_media_e_ <= out;
   if (mem_addr_wr == 325 && mem_wr) me1_f_main_v_read_idx_mean_e_ <= out;
   if (mem_addr_wr == 326 && mem_wr) me1_f_main_v_w_index_mean_e_ <= out;
   if (mem_addr_wr == 327 && mem_wr) me1_f_main_v_p_e_ <= out;
   if (mem_addr_wr == 328 && mem_wr) me1_f_main_v_b_index_mean_e_ <= out;
   if (mem_addr_wr == 330 && mem_wr) me1_f_main_v_atraso_amotras_media_movel_e_ <= out;
   if (mem_addr_wr == 331 && mem_wr) me2_f_main_v_fvelho_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 332 && mem_wr) me2_f_main_v_f_nominal_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 333 && mem_wr) me2_f_main_v_dfreq_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 334 && mem_wr) me2_f_main_v_df_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 336 && mem_wr) me2_f_main_v_p00_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 337 && mem_wr) me2_f_main_v_p01_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 338 && mem_wr) me2_f_main_v_p10_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 339 && mem_wr) me2_f_main_v_p11_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 342 && mem_wr) me2_f_main_v_q00_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 344 && mem_wr) me2_f_main_v_q01_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 345 && mem_wr) me2_f_main_v_q10_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 346 && mem_wr) me2_f_main_v_q11_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 347 && mem_wr) me2_f_main_v_dfreq_pred_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 348 && mem_wr) me2_f_main_v_df_pred_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 350 && mem_wr) me2_f_main_v_R_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 351 && mem_wr) me1_f_main_v_cont_kalman_e_ <= out;
   if (mem_addr_wr == 353 && mem_wr) me1_f_main_v_descarte_kalman_e_ <= out;
   if (mem_addr_wr == 354 && mem_wr) me2_f_main_v_erro_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 355 && mem_wr) me2_f_main_v_comp_dfreq_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 356 && mem_wr) me1_f_main_v_j_e_ <= out;
   if (mem_addr_wr == 357 && mem_wr) me1_f_main_v_read_idx_e_ <= out;
   if (mem_addr_wr == 358 && mem_wr) me2_f_main_v_acc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 359 && mem_wr) me2_f_main_v_freq_instant_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 360 && mem_wr) me2_f_main_v_Tsc_total_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 361 && mem_wr) me2_f_main_v_denom_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 363 && mem_wr) me2_f_main_v_ESCALA_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 364 && mem_wr) me2_f_main_v_x_atrasado_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 365 && mem_wr) me1_f_main_v_c_index_e_ <= out;
   if (mem_addr_wr == 366 && mem_wr) me1_f_main_v_read_c_idx_e_ <= out;
   if (mem_addr_wr == 639 && mem_wr) me1_f_main_v_atraso_geral_e_ <= out;
   if (mem_addr_wr == 644 && mem_wr) me2_f_main_v_alfa_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 645 && mem_wr) me1_f_main_v_cnt_e_ <= out;
   if (mem_addr_wr == 673 && mem_wr) me2_f_main_v_x_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 676 && mem_wr) me2_f_main_v_Ts_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 679 && mem_wr) me2_f_main_v_kah_u_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 680 && mem_wr) me2_f_main_v_kah_t_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 681 && mem_wr) me2_f_main_v_p00_pred_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 682 && mem_wr) me2_f_main_v_p01_pred_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 683 && mem_wr) me2_f_main_v_p10_pred_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 684 && mem_wr) me2_f_main_v_p11_pred_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 685 && mem_wr) me2_f_main_v_y_kalman_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 686 && mem_wr) me2_f_main_v_S_incerteza_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 687 && mem_wr) me2_f_main_v_K0_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 688 && mem_wr) me2_f_main_v_K1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 690 && mem_wr) me2_f_main_v_dot_result_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 691 && mem_wr) me2_f_main_v_freq_smoothed_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 692 && mem_wr) me2_f_main_v_freq_atrasada_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 693 && mem_wr) me2_f_main_v_lambda_val_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 695 && mem_wr) me2_f_main_v_y_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 698 && mem_wr) me2_f_main_v_H0_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 699 && mem_wr) me2_f_main_v_H1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 700 && mem_wr) me2_f_main_v_H2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 702 && mem_wr) me2_f_main_v_H3_e_ <= sm_me2*$pow(2.0,e_me2);
end

// instructions ---------------------------------------------------------------

reg [31:0] valr2=0;
/* verilator tracing_off */
reg [31:0] valr1 /* verilator public_flat */=0;
reg [31:0] valr3 /* verilator public_flat */=0;
reg [31:0] valr4 /* verilator public_flat */=0;
reg [31:0] valr5 /* verilator public_flat */=0;
reg [31:0] valr6 /* verilator public_flat */=0;
reg [31:0] valr7 /* verilator public_flat */=0;
reg [31:0] valr8 /* verilator public_flat */=0;
reg [31:0] valr9 /* verilator public_flat */=0;
reg [31:0] valr10 /* verilator public_flat */=0;
/* verilator tracing_on */

reg [19:0] min [0:834-1];

/* verilator tracing_off */ reg signed [19:0] linetab /* verilator public_flat */ =-1; /* verilator tracing_on */
reg signed [19:0] linetabs=-1;

initial	$readmemb("pc_proc_interp_mem.txt",min);

always @ (posedge clk) begin
if (pc_sim_val < 834) linetab <= min[pc_sim_val];
linetabs <= linetab;   
valr1    <= {{(22){1'b0}}, pc_sim_val};
valr2    <= valr1;
valr3    <= valr2;
valr4    <= valr3;
valr5    <= valr4;
valr6    <= valr5;
valr7    <= valr6;
valr8    <= valr7;
valr9    <= valr8;
valr10   <= valr9;
end

`endif

endmodule