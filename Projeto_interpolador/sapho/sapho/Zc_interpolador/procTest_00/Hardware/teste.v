module teste (

input  clk, rst,
input  signed [22:0] in ,
output signed [22:0] out,
output [0:0] req_in,
output [0:0] out_en);

wire itr = 1'b0;
wire proc_req_in, proc_out_en;
wire [0:0] addr_in;
wire [0:0] addr_out;

`ifdef __ICARUS__
wire mem_wr;
wire [9:0] mem_addr_wr;
wire [8:0] pc_sim_val;
`endif

processor#(.NUBITS(23),
.NBMANT(16),
.NBEXPO(6),
.NBOPER(10),
.NUGAIN(128),
.MDATAS(850),
.MINSTS(451),
.SDEPTH(5),
.DDEPTH(5),
.NBIOIN(1),
.NBIOOU(1),
.FFTSIZ(8),
.LOD(1),
.SET(1),
.F_NEG_M(1),
.LES(1),
.JIZ(1),
.P_LOD(1),
.STI(1),
.ADD(1),
.F_MLT(1),
.INN(1),
.I2F(1),
.SF_DIV(1),
.NEG_M(1),
.LDI(1),
.SF_MLT(1),
.F_ADD(1),
.LIN(1),
.F_DIV(1),
.SF_LES(1),
.S_LAN(1),
.S_EQU(1),
.PF_NEG_M(1),
.SF_ADD(1),
.SF_GRE(1),
.F_NEG(1),
.EQU(1),
.GRE(1),
.F2I_M(1),
.OUT(1),
.DFILE("C:/Users/S/Documents/f_zc/Zc_interpolador/Zc_interpolador/procTest_00/Hardware/teste_data.mif"),
.IFILE("C:/Users/S/Documents/f_zc/Zc_interpolador/Zc_interpolador/procTest_00/Hardware/teste_inst.mif"))

`ifdef __ICARUS__
p_teste (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, mem_wr, mem_addr_wr,pc_sim_val);
`else
p_teste (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr);
`endif

assign req_in = proc_req_in;
assign out_en = proc_out_en;

// ----------------------------------------------------------------------------
// Simulacao ------------------------------------------------------------------
// ----------------------------------------------------------------------------

`ifdef __ICARUS__

// I/O ------------------------------------------------------------------------

reg signed [22:0] in_sim_0 = 0;
reg req_in_sim_0 = 0;

reg signed [22:0] out_sig_0 = 0;
reg out_en_sim_0 = 0;

always @ (*) begin
   if (req_in == 1) in_sim_0 = in;
   req_in_sim_0 = req_in == 1;
end

always @ (*) begin
   if (out_en == 1) out_sig_0 <= out;
   out_en_sim_0 = out_en == 1;
end

// variaveis ------------------------------------------------------------------

reg [22:0] me1_f_main_v_b_index_e_ = 0;
integer sm_me2; always @ (*) sm_me2 = (out[22]) ? -out[15:0] : out[15:0];
integer  e_me2; always @ (*)  e_me2 = $signed(out[21:16]);
real me2_f_main_v_va_e_ = 0.0;
real me2_f_main_v_Tsc_e_ = 0.0;
real me2_f_main_v_T1_e_ = 0.0;
real me2_f_main_v_last_freq_e_ = 0.0;
real me2_f_main_v_acc_e_ = 0.0;
reg [22:0] me1_f_main_v_w_index_e_ = 0;
real me2_f_main_v_w_sum_e_ = 0.0;
real me2_f_main_v_freq_instant_e_ = 0.0;
real me2_f_main_v_freq_smoothed_e_ = 0.0;
real me2_f_main_v_c0_e_ = 0.0;
real me2_f_main_v_c1_e_ = 0.0;
real me2_f_main_v_c2_e_ = 0.0;
real me2_f_main_v_c3_e_ = 0.0;
real me2_f_main_v_c4_e_ = 0.0;
real me2_f_main_v_alfa_e_ = 0.0;
reg [22:0] me1_f_main_v_cnt_e_ = 0;
real me2_f_main_v_lambda_val_e_ = 0.0;
real me2_f_main_v_y_e_ = 0.0;
real me2_f_main_v_ESCALA_e_ = 0.0;
reg [22:0] me1_f_main_v_j_e_ = 0;
reg [22:0] me1_f_main_v_read_idx_e_ = 0;
reg [22:0] me1_f_main_v_b_read_e_ = 0;
real me2_f_main_v_x_e_ = 0.0;
real me2_f_main_v_Nb_e_ = 0.0;
real me2_f_main_v_T2_e_ = 0.0;
real me2_f_main_v_Tsc_total_e_ = 0.0;
real me2_f_main_v_denom_e_ = 0.0;
real me2_f_main_v_pre_out_e_ = 0.0;
real me2_f_main_v_b0_e_ = 0.0;
real me2_f_main_v_b1_e_ = 0.0;
real me2_f_main_v_b2_e_ = 0.0;
real me2_f_main_v_b3_e_ = 0.0;
real me2_f_main_v_H0_e_ = 0.0;
real me2_f_main_v_H1_e_ = 0.0;
real me2_f_main_v_H2_e_ = 0.0;
real me2_f_main_v_H3_e_ = 0.0;
real me2_f_main_v_a2_e_ = 0.0;
real me2_f_main_v_a3_e_ = 0.0;
reg [22:0] me1_f_main_v_zc_estavel_e_ = 0;
reg [22:0] me1_f_main_v_zc_cnt_e_ = 0;

always @ (posedge clk) begin
   if (mem_addr_wr == 515 && mem_wr) me1_f_main_v_b_index_e_ <= out;
   if (mem_addr_wr == 517 && mem_wr) me2_f_main_v_va_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 518 && mem_wr) me2_f_main_v_Tsc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 519 && mem_wr) me2_f_main_v_T1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 521 && mem_wr) me2_f_main_v_last_freq_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 522 && mem_wr) me2_f_main_v_acc_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 779 && mem_wr) me1_f_main_v_w_index_e_ <= out;
   if (mem_addr_wr == 780 && mem_wr) me2_f_main_v_w_sum_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 781 && mem_wr) me2_f_main_v_freq_instant_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 782 && mem_wr) me2_f_main_v_freq_smoothed_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 789 && mem_wr) me2_f_main_v_c0_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 791 && mem_wr) me2_f_main_v_c1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 793 && mem_wr) me2_f_main_v_c2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 794 && mem_wr) me2_f_main_v_c3_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 795 && mem_wr) me2_f_main_v_c4_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 800 && mem_wr) me2_f_main_v_alfa_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 801 && mem_wr) me1_f_main_v_cnt_e_ <= out;
   if (mem_addr_wr == 803 && mem_wr) me2_f_main_v_lambda_val_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 804 && mem_wr) me2_f_main_v_y_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 806 && mem_wr) me2_f_main_v_ESCALA_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 807 && mem_wr) me1_f_main_v_j_e_ <= out;
   if (mem_addr_wr == 808 && mem_wr) me1_f_main_v_read_idx_e_ <= out;
   if (mem_addr_wr == 809 && mem_wr) me1_f_main_v_b_read_e_ <= out;
   if (mem_addr_wr == 810 && mem_wr) me2_f_main_v_x_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 811 && mem_wr) me2_f_main_v_Nb_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 812 && mem_wr) me2_f_main_v_T2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 813 && mem_wr) me2_f_main_v_Tsc_total_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 814 && mem_wr) me2_f_main_v_denom_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 815 && mem_wr) me2_f_main_v_pre_out_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 816 && mem_wr) me2_f_main_v_b0_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 817 && mem_wr) me2_f_main_v_b1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 818 && mem_wr) me2_f_main_v_b2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 819 && mem_wr) me2_f_main_v_b3_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 820 && mem_wr) me2_f_main_v_H0_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 821 && mem_wr) me2_f_main_v_H1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 822 && mem_wr) me2_f_main_v_H2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 823 && mem_wr) me2_f_main_v_H3_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 824 && mem_wr) me2_f_main_v_a2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 825 && mem_wr) me2_f_main_v_a3_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 826 && mem_wr) me1_f_main_v_zc_estavel_e_ <= out;
   if (mem_addr_wr == 827 && mem_wr) me1_f_main_v_zc_cnt_e_ <= out;
end

// instrucoes -----------------------------------------------------------------

reg [22:0] valr1=0;
reg [22:0] valr2=0;
reg [22:0] valr3=0;
reg [22:0] valr4=0;
reg [22:0] valr5=0;
reg [22:0] valr6=0;
reg [22:0] valr7=0;
reg [22:0] valr8=0;
reg [22:0] valr9=0;
reg [22:0] valr10=0;

reg [19:0] min [0:451-1];

reg signed [19:0] linetab =-1;
reg signed [19:0] linetabs=-1;

initial	$readmemb("pc_teste_mem.txt",min);

always @ (posedge clk) begin
if (pc_sim_val < 451) linetab <= min[pc_sim_val];
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

always @ (posedge clk) if (valr10 == 450) begin
   $display("Info: end of program!");
   $finish;
end

`endif

endmodule