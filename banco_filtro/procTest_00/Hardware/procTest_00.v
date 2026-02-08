module procTest_00 (

input  clk, rst,
input  signed [31:0] in ,
output signed [31:0] out,
output [0:0] req_in,
output [6:0] out_en);

wire itr = 1'b0;
wire proc_req_in, proc_out_en;
wire [0:0] addr_in;
wire [2:0] addr_out;

`ifdef __ICARUS__
wire mem_wr;
wire [12:0] mem_addr_wr;
wire [8:0] pc_sim_val;
`endif

processor#(.NUBITS(32),
.NBMANT(23),
.NBEXPO(8),
.NBOPER(13),
.NUGAIN(128),
.MDATAS(5667),
.MINSTS(396),
.SDEPTH(5),
.DDEPTH(5),
.NBIOIN(1),
.NBIOOU(3),
.FFTSIZ(8),
.CAL(1),
.SET(1),
.LOD(1),
.LES(1),
.JIZ(1),
.MLT(1),
.ADD(1),
.LDI(1),
.P_LOD(1),
.ILI(1),
.SET_P(1),
.F_MLT(1),
.SF_SU2(1),
.SF_ADD(1),
.F_SU1(1),
.ISI(1),
.F_ADD(1),
.NEG_M(1),
.GRE(1),
.P_NEG_M(1),
.STI(1),
.P_INN(1),
.I2F(1),
.SF_DIV(1),
.EQU(1),
.SF_MLT(1),
.P_I2F_M(1),
.POP(1),
.F2I(1),
.OUT(1),
.DFILE("C:/Users/Ricardo/Documents/Dissertacao/banco_filtro/procTest_00/Hardware/procTest_00_data.mif"),
.IFILE("C:/Users/Ricardo/Documents/Dissertacao/banco_filtro/procTest_00/Hardware/procTest_00_inst.mif"))

`ifdef __ICARUS__
p_procTest_00 (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, mem_wr, mem_addr_wr,pc_sim_val);
`else
p_procTest_00 (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr);
`endif

assign req_in = proc_req_in;
addr_dec #(7) dec_out(proc_out_en, addr_out, out_en);

// ----------------------------------------------------------------------------
// Simulacao ------------------------------------------------------------------
// ----------------------------------------------------------------------------

`ifdef __ICARUS__

// I/O ------------------------------------------------------------------------

reg signed [31:0] in_sim_0 = 0;
reg req_in_sim_0 = 0;

reg signed [31:0] out_sig_1 = 0;
reg out_en_sim_1 = 0;
reg signed [31:0] out_sig_2 = 0;
reg out_en_sim_2 = 0;
reg signed [31:0] out_sig_3 = 0;
reg out_en_sim_3 = 0;
reg signed [31:0] out_sig_4 = 0;
reg out_en_sim_4 = 0;
reg signed [31:0] out_sig_5 = 0;
reg out_en_sim_5 = 0;
reg signed [31:0] out_sig_6 = 0;
reg out_en_sim_6 = 0;

always @ (*) begin
   if (req_in == 1) in_sim_0 = in;
   req_in_sim_0 = req_in == 1;
end

always @ (*) begin
   if (out_en == 2) out_sig_1 <= out;
   out_en_sim_1 = out_en == 2;
   if (out_en == 4) out_sig_2 <= out;
   out_en_sim_2 = out_en == 4;
   if (out_en == 8) out_sig_3 <= out;
   out_en_sim_3 = out_en == 8;
   if (out_en == 16) out_sig_4 <= out;
   out_en_sim_4 = out_en == 16;
   if (out_en == 32) out_sig_5 <= out;
   out_en_sim_5 = out_en == 32;
   if (out_en == 64) out_sig_6 <= out;
   out_en_sim_6 = out_en == 64;
end

// variaveis ------------------------------------------------------------------

reg [31:0] me1_f_ifft_v_N_e_ = 0;
reg [31:0] me1_f_ifft_v_mmax_e_ = 0;
reg [31:0] me1_f_ifft_v_istep_e_ = 0;
reg [31:0] me1_f_ifft_v_m_e_ = 0;
reg [31:0] me1_f_ifft_v_ind_e_ = 0;
reg [31:0] me1_f_ifft_v_sind_e_ = 0;
reg [31:0] me1_f_ifft_v_k_e_ = 0;
reg [31:0] me1_f_ifft_v_j_e_ = 0;
reg [31:0] me3_f_ifft_v_temp_i_e_ = 31'dx;
reg [31:0] me3_f_ifft_v_temp_e_ = 31'dx;
reg [31:0] me1_f_main_v_sample_count_e_ = 0;
reg [31:0] me1_f_main_v_output_count_e_ = 0;
reg [31:0] me1_f_main_v_M_e_ = 0;
reg [31:0] me1_f_main_v_fft_limit_e_ = 0;
reg [31:0] me1_f_main_v_k_e_ = 0;
reg [31:0] me1_f_main_v_mm_e_ = 0;

always @ (posedge clk) begin
   if (mem_addr_wr == 768 && mem_wr) me1_f_ifft_v_N_e_ <= out;
   if (mem_addr_wr == 770 && mem_wr) me1_f_ifft_v_mmax_e_ <= out;
   if (mem_addr_wr == 772 && mem_wr) me1_f_ifft_v_istep_e_ <= out;
   if (mem_addr_wr == 774 && mem_wr) me1_f_ifft_v_m_e_ <= out;
   if (mem_addr_wr == 775 && mem_wr) me1_f_ifft_v_ind_e_ <= out;
   if (mem_addr_wr == 776 && mem_wr) me1_f_ifft_v_sind_e_ <= out;
   if (mem_addr_wr == 777 && mem_wr) me1_f_ifft_v_k_e_ <= out;
   if (mem_addr_wr == 778 && mem_wr) me1_f_ifft_v_j_e_ <= out;
   if (mem_addr_wr == 783 && mem_wr) me3_f_ifft_v_temp_i_e_ <= out;
   if (mem_addr_wr == 784 && mem_wr) me3_f_ifft_v_temp_e_ <= out;
   if (mem_addr_wr == 785 && mem_wr) me1_f_main_v_sample_count_e_ <= out;
   if (mem_addr_wr == 786 && mem_wr) me1_f_main_v_output_count_e_ <= out;
   if (mem_addr_wr == 5655 && mem_wr) me1_f_main_v_M_e_ <= out;
   if (mem_addr_wr == 5656 && mem_wr) me1_f_main_v_fft_limit_e_ <= out;
   if (mem_addr_wr == 5657 && mem_wr) me1_f_main_v_k_e_ <= out;
   if (mem_addr_wr == 5659 && mem_wr) me1_f_main_v_mm_e_ <= out;
end

wire [16+32*2-1:0] comp_me3_f_ifft_v_temp_e_ = {8'd23, 8'd8, me3_f_ifft_v_temp_e_, me3_f_ifft_v_temp_i_e_};

// instrucoes -----------------------------------------------------------------

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

reg [19:0] min [0:396-1];

reg signed [19:0] linetab =-1;
reg signed [19:0] linetabs=-1;

initial	$readmemb("pc_procTest_00_mem.txt",min);

always @ (posedge clk) begin
if (pc_sim_val < 396) linetab <= min[pc_sim_val];
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

always @ (posedge clk) if (valr10 == 2) begin
   $display("Info: end of program!");
   $finish;
end

`endif

endmodule