module proc_interp (

input  clk, rst,
input  signed [31:0] in ,
output signed [31:0] out,
output [0:0] req_in,
output [4:0] out_en,
input  itr);

wire cheguei;
wire proc_req_in, proc_out_en;
wire [0:0] addr_in;
wire [2:0] addr_out;

`ifdef __ICARUS__
wire mem_wr;
wire [9:0] mem_addr_wr;
wire [9:0] pc_sim_val;
`endif

processor#(.NUBITS(32),
.NBMANT(23),
.NBEXPO(8),
.NBOPER(10),
.NUGAIN(128),
.MDATAS(814),
.MINSTS(837),
.SDEPTH(5),
.DDEPTH(5),
.NBIOIN(1),
.NBIOOU(3),
.FFTSIZ(8),
.ITRADD(227),
.LOD(1),
.SET(1),
.P_LOD(1),
.STI(1),
.I2F_M(1),
.SF_DIV(1),
.PF_NEG_M(1),
.INN(1),
.I2F(1),
.LDI(1),
.SF_MLT(1),
.SF_ADD(1),
.SF_SU2(1),
.F_MLT(1),
.F2I(1),
.OUT(1),
.F_DIV(1),
.F_ADD(1),
.P_I2F_M(1),
.SF_LES(1),
.JIZ(1),
.F_SU1(1),
.GRE(1),
.ADD(1),
.LES(1),
.LIN(1),
.SF_GRE(1),
.F_SU2(1),
.S_EQU(1),
.F_NEG(1),
.DFILE("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Hardware/proc_interp_data.mif"),
.IFILE("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_interp/Hardware/proc_interp_inst.mif"))

`ifdef __ICARUS__
p_proc_interp (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, cheguei, mem_wr, mem_addr_wr,pc_sim_val);
`else
p_proc_interp (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, cheguei);
`endif

assign req_in = proc_req_in;
addr_dec #(5) dec_out(proc_out_en, addr_out, out_en);

// ----------------------------------------------------------------------------
// Simulation -----------------------------------------------------------------
// ----------------------------------------------------------------------------

`ifdef __ICARUS__

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

always @ (*) begin
   if (req_in == 1) in_sim_0 = in;
   req_in_sim_0 = req_in == 1;
end

always @ (*) begin
   if (out_en == 1) out_sig_0 <= out;
   out_en_sim_0 = out_en == 1;
   if (out_en == 2) out_sig_1 <= out;
   out_en_sim_1 = out_en == 2;
   if (out_en == 4) out_sig_2 <= out;
   out_en_sim_2 = out_en == 4;
   if (out_en == 8) out_sig_3 <= out;
   out_en_sim_3 = out_en == 8;
   if (out_en == 16) out_sig_4 <= out;
   out_en_sim_4 = out_en == 16;
end

// variables ------------------------------------------------------------------

reg [31:0] me1_f_main_v_cont_global_e_ = 0;
reg [31:0] me1_f_main_v_b_index_e_ = 0;
reg [31:0] me1_f_main_v_k_idx_e_ = 0;
integer sm_me2; always @ (*) sm_me2 = (out[31]) ? -out[22:0] : out[22:0];
integer  e_me2; always @ (*)  e_me2 = $signed(out[30:23]);
real me2_f_main_v_acc_b_e_ = 0.0;
real me2_f_main_v_acc_a_e_ = 0.0;
reg [31:0] me1_f_main_v_atraso_amotras_filtro_pre_zc_e_ = 0;
reg [31:0] me1_f_main_v_bm_index_e_ = 0;
reg [31:0] me1_f_main_v_km_idx_e_ = 0;
real me2_f_main_v_accm_b_e_ = 0.0;
real me2_f_main_v_accm_a_e_ = 0.0;
real me2_f_main_v_fcc_e_ = 0.0;
reg [31:0] me1_f_main_v_atraso_pos_zc_e_ = 0;
real me2_f_main_v_va_e_ = 0.0;
real me2_f_main_v_Tsc_e_ = 0.0;
real me2_f_main_v_T1_e_ = 0.0;
real me2_f_main_v_fzc_e_ = 0.0;
real me2_f_main_v_freq_amostragem_e_ = 0.0;
real me2_f_main_v_sig_e_ = 0.0;
real me2_f_main_v_Nb_e_ = 0.0;
real me2_f_main_v_T2_e_ = 0.0;
reg [31:0] me1_f_main_v_atraso_ZC_e_ = 0;
reg [31:0] me1_f_main_v_j_e_ = 0;
reg [31:0] me1_f_main_v_read_idx_e_ = 0;
real me2_f_main_v_acc_e_ = 0.0;
real me2_f_main_v_freq_instant_e_ = 0.0;
real me2_f_main_v_Tsc_total_e_ = 0.0;
real me2_f_main_v_denom_e_ = 0.0;
real me2_f_main_v_ESCALA_e_ = 0.0;
real me2_f_main_v_x_atrasado_e_ = 0.0;
real me2_f_main_v_discard_samples_e_ = 0.0;
reg [31:0] me1_f_main_v_atraso_geral_e_ = 0;
reg [31:0] me1_f_main_v_c_index_e_ = 0;
reg [31:0] me1_f_main_v_read_c_idx_e_ = 0;
real me2_f_main_v_alfa_e_ = 0.0;
reg [31:0] me1_f_main_v_cnt_e_ = 0;
real me2_f_main_v_x_e_ = 0.0;
real me2_f_main_v_Ts_e_ = 0.0;
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
   if (mem_addr_wr == 1 && mem_wr) me1_f_main_v_cont_global_e_ <= out;
   if (mem_addr_wr == 41 && mem_wr) me1_f_main_v_b_index_e_ <= out;
   if (mem_addr_wr == 42 && mem_wr) me1_f_main_v_k_idx_e_ <= out;
   if (mem_addr_wr == 43 && mem_wr) me2_f_main_v_acc_b_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 44 && mem_wr) me2_f_main_v_acc_a_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 46 && mem_wr) me1_f_main_v_atraso_amotras_filtro_pre_zc_e_ <= out;
   if (mem_addr_wr == 83 && mem_wr) me1_f_main_v_bm_index_e_ <= out;
   if (mem_addr_wr == 84 && mem_wr) me1_f_main_v_km_idx_e_ <= out;
   if (mem_addr_wr == 85 && mem_wr) me2_f_main_v_accm_b_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 86 && mem_wr) me2_f_main_v_accm_a_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 87 && mem_wr) me2_f_main_v_fcc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 89 && mem_wr) me1_f_main_v_atraso_pos_zc_e_ <= out;
   if (mem_addr_wr == 90 && mem_wr) me2_f_main_v_va_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 92 && mem_wr) me2_f_main_v_Tsc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 93 && mem_wr) me2_f_main_v_T1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 94 && mem_wr) me2_f_main_v_fzc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 96 && mem_wr) me2_f_main_v_freq_amostragem_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 97 && mem_wr) me2_f_main_v_sig_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 98 && mem_wr) me2_f_main_v_Nb_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 99 && mem_wr) me2_f_main_v_T2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 101 && mem_wr) me1_f_main_v_atraso_ZC_e_ <= out;
   if (mem_addr_wr == 102 && mem_wr) me1_f_main_v_j_e_ <= out;
   if (mem_addr_wr == 103 && mem_wr) me1_f_main_v_read_idx_e_ <= out;
   if (mem_addr_wr == 104 && mem_wr) me2_f_main_v_acc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 105 && mem_wr) me2_f_main_v_freq_instant_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 106 && mem_wr) me2_f_main_v_Tsc_total_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 107 && mem_wr) me2_f_main_v_denom_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 109 && mem_wr) me2_f_main_v_ESCALA_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 110 && mem_wr) me2_f_main_v_x_atrasado_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 112 && mem_wr) me2_f_main_v_discard_samples_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 130 && mem_wr) me1_f_main_v_atraso_geral_e_ <= out;
   if (mem_addr_wr == 131 && mem_wr) me1_f_main_v_c_index_e_ <= out;
   if (mem_addr_wr == 132 && mem_wr) me1_f_main_v_read_c_idx_e_ <= out;
   if (mem_addr_wr == 773 && mem_wr) me2_f_main_v_alfa_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 774 && mem_wr) me1_f_main_v_cnt_e_ <= out;
   if (mem_addr_wr == 795 && mem_wr) me2_f_main_v_x_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 799 && mem_wr) me2_f_main_v_Ts_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 801 && mem_wr) me2_f_main_v_dot_result_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 802 && mem_wr) me2_f_main_v_freq_smoothed_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 803 && mem_wr) me2_f_main_v_freq_atrasada_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 804 && mem_wr) me2_f_main_v_lambda_val_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 805 && mem_wr) me2_f_main_v_y_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 808 && mem_wr) me2_f_main_v_H0_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 809 && mem_wr) me2_f_main_v_H1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 810 && mem_wr) me2_f_main_v_H2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 812 && mem_wr) me2_f_main_v_H3_e_ <= sm_me2*$pow(2.0,e_me2);
end

// instructions ---------------------------------------------------------------

reg [31:0] valr1=0;
reg [31:0] valr2=0;
reg [31:0] valr3=0;
reg [31:0] valr4=0;
reg [31:0] valr5=0;
reg [31:0] valr6=0;
reg [31:0] valr7=0;
reg [31:0] valr8=0;
reg [31:0] valr9=0;
reg [31:0] valr10=0;

reg [19:0] min [0:837-1];

reg signed [19:0] linetab =-1;
reg signed [19:0] linetabs=-1;

initial	$readmemb("pc_proc_interp_mem.txt",min);

always @ (posedge clk) begin
if (pc_sim_val < 837) linetab <= min[pc_sim_val];
linetabs <= linetab;   
valr1    <= pc_sim_val;
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