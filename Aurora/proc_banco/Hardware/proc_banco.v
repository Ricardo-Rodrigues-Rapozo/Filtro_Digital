module proc_banco (

input  clk, rst,
input  signed [31:0] in ,
output signed [31:0] out,
output [1:0] req_in,
output [3:0] out_en,
input  itr);

/* verilator tracing_off */

wire cheguei;
wire proc_req_in, proc_out_en;
wire [0:0] addr_in;
wire [1:0] addr_out;

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
wire [12:0] mem_addr_wr;
wire [8:0] pc_sim_val;
`endif

processor#(.NUBITS(32),
.NBMANT(23),
.NBEXPO(8),
.NBOPER(13),
.NUGAIN(128),
.MDATAS(5672),
.MINSTS(390),
.SDEPTH(5),
.DDEPTH(5),
.NBIOIN(1),
.NBIOOU(2),
.FFTSIZ(8),
.ITRADD(28),
.LOD(1),
.SET(1),
.NEG_M(1),
.ADD(1),
.I2F_M(1),
.OUT(1),
.LES(1),
.JIZ(1),
.P_INN(1),
.I2F(1),
.P_LOD(1),
.SF_DIV(1),
.STI(1),
.INN(1),
.EQU(1),
.GRE(1),
.MLT(1),
.LDI(1),
.SF_MLT(1),
.SF_ADD(1),
.SET_P(1),
.LIN(1),
.ILI(1),
.F_MLT(1),
.SF_SU2(1),
.F_SU1(1),
.ISI(1),
.F_ADD(1),
.P_I2F_M(1),
.SF_GRE(1),
.F2I_M(1),
.POP(1),
.F2I(1),
.DFILE("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_banco/Hardware/proc_banco_data.mif"),
.IFILE("C:/Users/Ricardo/Documents/Dissertacao/Aurora/proc_banco/Hardware/proc_banco_inst.mif"))

`ifdef YANC_SIM_VIS
p_proc_banco (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, cheguei, mem_wr, mem_addr_wr,pc_sim_val);
`else
p_proc_banco (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, cheguei);
`endif

addr_dec #(2) dec_in (proc_req_in, addr_in , req_in);
addr_dec #(4) dec_out(proc_out_en, addr_out, out_en);

/* verilator tracing_on */

// ----------------------------------------------------------------------------
// Simulation -----------------------------------------------------------------
// ----------------------------------------------------------------------------

`ifdef YANC_SIM_VIS

// I/O ------------------------------------------------------------------------

reg signed [31:0] in_sim_0 = 0;
reg req_in_sim_0 = 0;
reg signed [31:0] in_sim_1 = 0;
reg req_in_sim_1 = 0;

reg signed [31:0] out_sig_0 = 0;
reg out_en_sim_0 = 0;
reg signed [31:0] out_sig_1 = 0;
reg out_en_sim_1 = 0;

always @ (posedge clk) begin
   if (req_in == 1) in_sim_0 <= in;
   if (req_in == 2) in_sim_1 <= in;
end
always @ (*) begin
   req_in_sim_0 = req_in == 1;
   req_in_sim_1 = req_in == 2;
end

always @ (posedge clk) begin
   if (out_en == 1) out_sig_0 <= out;
   if (out_en == 2) out_sig_1 <= out;
end
always @ (*) begin
   out_en_sim_0 = out_en == 1;
   out_en_sim_1 = out_en == 2;
end

// variables ------------------------------------------------------------------

/* verilator tracing_off */  // float decode helpers (not traced)
reg signed [23:0] sm_me2; always @ (*) sm_me2 = (out[31]) ? -$signed({1'b0, out[22:0]}) : $signed({1'b0, out[22:0]});
reg signed [7:0] e_me2; always @ (*)  e_me2 = $signed(out[30:23]);
/* verilator tracing_on */

reg [31:0] me1_f_main_v_frequencia_from_int_e_ = 0;
reg [31:0] me1_f_main_v_sample_count_e_ = 0;
reg [31:0] me1_f_main_v_output_count_e_ = 0;
reg [31:0] me1_f_main_v_freq_count_e_ = 0;
reg [31:0] me1_f_main_v_freq_started_e_ = 0;
reg [31:0] me1_f_main_v_M_e_ = 0;
reg [31:0] me1_f_main_v_fft_limit_e_ = 0;
real me2_f_main_v_vector_count_e_ = 0.0;
reg [31:0] me1_f_main_v_buffer_head_e_ = 0;
reg [31:0] me1_f_main_v_mm_e_ = 0;
reg [31:0] me1_f_main_v_ii_e_ = 0;
reg [31:0] me1_f_main_v_mmax_e_ = 0;
reg [31:0] me1_f_main_v_istep_e_ = 0;
reg [31:0] me1_f_main_v_m_e_ = 0;
reg [31:0] me1_f_main_v_ind_e_ = 0;
reg [31:0] me1_f_main_v_sind_e_ = 0;
reg [31:0] me1_f_main_v_q_e_ = 0;
reg [31:0] me1_f_main_v_j_e_ = 0;
/* verilator tracing_off */  // comp raw halves (joined below, not traced)
reg [31:0] me3_f_main_v_temp_i_e_ /* verilator public_flat */ = 32'dx;
reg [31:0] me3_f_main_v_temp_e_ /* verilator public_flat */ = 32'dx;
/* verilator tracing_on */

always @ (posedge clk) begin
   if (mem_addr_wr == 769 && mem_wr) me1_f_main_v_frequencia_from_int_e_ <= out;
   if (mem_addr_wr == 770 && mem_wr) me1_f_main_v_sample_count_e_ <= out;
   if (mem_addr_wr == 771 && mem_wr) me1_f_main_v_output_count_e_ <= out;
   if (mem_addr_wr == 3590 && mem_wr) me1_f_main_v_freq_count_e_ <= out;
   if (mem_addr_wr == 5640 && mem_wr) me1_f_main_v_freq_started_e_ <= out;
   if (mem_addr_wr == 5642 && mem_wr) me1_f_main_v_M_e_ <= out;
   if (mem_addr_wr == 5643 && mem_wr) me1_f_main_v_fft_limit_e_ <= out;
   if (mem_addr_wr == 5645 && mem_wr) me2_f_main_v_vector_count_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 5646 && mem_wr) me1_f_main_v_buffer_head_e_ <= out;
   if (mem_addr_wr == 5648 && mem_wr) me1_f_main_v_mm_e_ <= out;
   if (mem_addr_wr == 5649 && mem_wr) me1_f_main_v_ii_e_ <= out;
   if (mem_addr_wr == 5659 && mem_wr) me1_f_main_v_mmax_e_ <= out;
   if (mem_addr_wr == 5660 && mem_wr) me1_f_main_v_istep_e_ <= out;
   if (mem_addr_wr == 5661 && mem_wr) me1_f_main_v_m_e_ <= out;
   if (mem_addr_wr == 5662 && mem_wr) me1_f_main_v_ind_e_ <= out;
   if (mem_addr_wr == 5663 && mem_wr) me1_f_main_v_sind_e_ <= out;
   if (mem_addr_wr == 5664 && mem_wr) me1_f_main_v_q_e_ <= out;
   if (mem_addr_wr == 5665 && mem_wr) me1_f_main_v_j_e_ <= out;
   if (mem_addr_wr == 5668 && mem_wr) me3_f_main_v_temp_i_e_ <= out;
   if (mem_addr_wr == 5669 && mem_wr) me3_f_main_v_temp_e_ <= out;
end

wire [16+32*2-1:0] comp_me3_f_main_v_temp_e_ = {8'd23, 8'd8, me3_f_main_v_temp_e_, me3_f_main_v_temp_i_e_};

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

reg [19:0] min [0:390-1];

/* verilator tracing_off */ reg signed [19:0] linetab /* verilator public_flat */ =-1; /* verilator tracing_on */
reg signed [19:0] linetabs=-1;

initial	$readmemb("pc_proc_banco_mem.txt",min);

always @ (posedge clk) begin
if (pc_sim_val < 390) linetab <= min[pc_sim_val];
linetabs <= linetab;   
valr1    <= {{(23){1'b0}}, pc_sim_val};
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