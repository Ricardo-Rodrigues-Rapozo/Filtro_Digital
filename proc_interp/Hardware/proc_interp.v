module proc_interp (

input  clk, rst,
input  signed [31:0] in ,
output signed [31:0] out,
output [0:0] req_in,
output [0:0] out_en,
input  itr);

wire proc_req_in, proc_out_en;
wire [0:0] addr_in;
wire [0:0] addr_out;

`ifdef __ICARUS__
wire mem_wr;
wire [5:0] mem_addr_wr;
wire [7:0] pc_sim_val;
`endif

processor#(.NUBITS(32),
.NBMANT(23),
.NBEXPO(8),
.NBOPER(8),
.NUGAIN(128),
.MDATAS(54),
.MINSTS(215),
.SDEPTH(5),
.DDEPTH(5),
.NBIOIN(1),
.NBIOOU(1),
.FFTSIZ(8),
.ITRADD(30),
.LOD(1),
.SET(1),
.PF_NEG_M(1),
.STI(1),
.P_LOD(1),
.INN(1),
.I2F(1),
.SF_DIV(1),
.LDI(1),
.SF_MLT(1),
.SF_ADD(1),
.F_SU2(1),
.F_DIV(1),
.GRE(1),
.JIZ(1),
.SF_LES(1),
.F_MLT(1),
.F_NEG(1),
.SF_SU2(1),
.F_ADD(1),
.I2F_M(1),
.F2I(1),
.OUT(1),
.F_SU1(1),
.ADD(1),
.DFILE("C:/Users/S/Documents/Projeto_banco_quartus/Projeto_banco/proc_interp/Hardware/proc_interp_data.mif"),
.IFILE("C:/Users/S/Documents/Projeto_banco_quartus/Projeto_banco/proc_interp/Hardware/proc_interp_inst.mif"))

`ifdef __ICARUS__
p_proc_interp (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, mem_wr, mem_addr_wr,pc_sim_val);
`else
p_proc_interp (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr);
`endif

assign req_in = proc_req_in;
assign out_en = proc_out_en;

// ----------------------------------------------------------------------------
// Simulacao ------------------------------------------------------------------
// ----------------------------------------------------------------------------

`ifdef __ICARUS__

// I/O ------------------------------------------------------------------------

reg signed [31:0] in_sim_0 = 0;
reg req_in_sim_0 = 0;

reg signed [31:0] out_sig_0 = 0;
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

integer sm_me2; always @ (*) sm_me2 = (out[31]) ? -out[22:0] : out[22:0];
integer  e_me2; always @ (*)  e_me2 = $signed(out[30:23]);
real me2_f_main_v_alfa_e_ = 0.0;
reg [31:0] me1_f_main_v_cnt_e_ = 0;
real me2_f_main_v_x_e_ = 0.0;
real me2_f_main_v_dot_result_e_ = 0.0;
real me2_f_main_v_freq_smoothed_e_ = 0.0;
real me2_f_main_v_lambda_val_e_ = 0.0;
real me2_f_main_v_y_e_ = 0.0;
real me2_f_main_v_H0_e_ = 0.0;
real me2_f_main_v_H1_e_ = 0.0;
real me2_f_main_v_H2_e_ = 0.0;
real me2_f_main_v_H3_e_ = 0.0;

always @ (posedge clk) begin
   if (mem_addr_wr == 21 && mem_wr) me2_f_main_v_alfa_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 23 && mem_wr) me1_f_main_v_cnt_e_ <= out;
   if (mem_addr_wr == 38 && mem_wr) me2_f_main_v_x_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 39 && mem_wr) me2_f_main_v_dot_result_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 41 && mem_wr) me2_f_main_v_freq_smoothed_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 43 && mem_wr) me2_f_main_v_lambda_val_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 44 && mem_wr) me2_f_main_v_y_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 48 && mem_wr) me2_f_main_v_H0_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 49 && mem_wr) me2_f_main_v_H1_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 50 && mem_wr) me2_f_main_v_H2_e_ <= sm_me2*$pow(2.0,e_me2);
   if (mem_addr_wr == 52 && mem_wr) me2_f_main_v_H3_e_ <= sm_me2*$pow(2.0,e_me2);
end

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

reg [19:0] min [0:215-1];

reg signed [19:0] linetab =-1;
reg signed [19:0] linetabs=-1;

initial	$readmemb("pc_proc_interp_mem.txt",min);

always @ (posedge clk) begin
if (pc_sim_val < 215) linetab <= min[pc_sim_val];
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