module procTest_00 (

input  clk, rst,
input  signed [22:0] in ,
output signed [22:0] out,
output [0:0] req_in,
output [1:0] out_en);

wire itr = 1'b0;
wire proc_req_in, proc_out_en;
wire [0:0] addr_in;
wire [0:0] addr_out;

`ifdef __ICARUS__
wire mem_wr;
wire [5:0] mem_addr_wr;
wire [6:0] pc_sim_val;
`endif

processor#(.PIPELN(3),
.NUBITS(23),
.NBMANT(16),
.NBEXPO(6),
.NBOPER(7),
.NUGAIN(128),
.MDATAS(48),
.MINSTS(94),
.SDEPTH(5),
.DDEPTH(5),
.NBIOIN(1),
.NBIOOU(1),
.FFTSIZ(8),
.LOD(1),
.P_LOD(1),
.STI(1),
.SET(1),
.JIZ(1),
.P_INN(1),
.I2F(1),
.F_MLT(1),
.I2F_M(1),
.LES(1),
.LDI(1),
.SF_MLT(1),
.F_ADD(1),
.ADD(1),
.NEG_M(1),
.F2I(1),
.OUT(1),
.EQU(1),
.DFILE("C:/Users/Ricardo/Documents/Codigos_C/primeiro/procTest_00/Hardware/procTest_00_data.mif"),
.IFILE("C:/Users/Ricardo/Documents/Codigos_C/primeiro/procTest_00/Hardware/procTest_00_inst.mif"))

`ifdef __ICARUS__
p_procTest_00 (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr, mem_wr, mem_addr_wr,pc_sim_val);
`else
p_procTest_00 (clk, rst, in, out, addr_in, addr_out, proc_req_in, proc_out_en, itr);
`endif

assign req_in = proc_req_in;
addr_dec #(2) dec_out(proc_out_en, addr_out, out_en);

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

reg [23-1:0] me1_f_global_v_tam_buff_input_e_=0;
reg [23-1:0] me1_f_global_v_tam_buff_coeffs_e_=0;
reg [23-1:0] me1_f_global_v_buff_circ_cont_e_=0;
reg [23-1:0] me1_f_global_v_coeffs_cont_e_=0;
reg [23-1:0] me1_f_global_v_pos_e_=0;
reg [16+23-1:0] me2_f_global_v_y_e_=0;

always @ (posedge clk) begin
   if (mem_addr_wr == 40 && mem_wr) me1_f_global_v_tam_buff_input_e_ <= out;
   if (mem_addr_wr == 41 && mem_wr) me1_f_global_v_tam_buff_coeffs_e_ <= out;
   if (mem_addr_wr == 42 && mem_wr) me1_f_global_v_buff_circ_cont_e_ <= out;
   if (mem_addr_wr == 43 && mem_wr) me1_f_global_v_coeffs_cont_e_ <= out;
   if (mem_addr_wr == 44 && mem_wr) me1_f_global_v_pos_e_ <= out;
   if (mem_addr_wr == 46 && mem_wr) me2_f_global_v_y_e_ <= {8'd16,8'd6,out};
end


// instrucoes -----------------------------------------------------------------

reg [23-1:0] valr1=0;
reg [23-1:0] valr2=0;
reg [23-1:0] valr3=0;
reg [23-1:0] valr4=0;
reg [23-1:0] valr5=0;
reg [23-1:0] valr6=0;
reg [23-1:0] valr7=0;
reg [23-1:0] valr8=0;
reg [23-1:0] valr9=0;
reg [23-1:0] valr10=0;

reg [19:0] min [0:94-1];

reg signed [19:0] linetab =-1;
reg signed [19:0] linetabs=-1;

initial	$readmemb("pc_procTest_00_mem.txt",min);

always @ (posedge clk) begin
if (pc_sim_val < 94) linetab <= min[pc_sim_val];
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

always @ (posedge clk) if (valr10 == 93) begin
$display("Info: end of program!");
$finish;
end

`endif

endmodule