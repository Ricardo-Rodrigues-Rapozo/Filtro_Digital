NOP
#PRNAME proc_banco
#NUBITS 32
#NDSTAC 5
#SDEPTH 5
#NUIOIN 2
#NUIOOU 4
#NBMANT 23
#NBEXPO 8
#FFTSIZ 8
#NUGAIN 128
#array E0 3 256
#array E0_i 4 256
#arrays wpv 3 128 "wpv.txt"
#arrays wpv_i 4 128 "wpv.txt"
@main LOD 0
SET main_frequencia_from_int
LOD 0
SET main_sample_count
LOD 0
SET main_output_count
#array main_output_buffer_real 2 256
#array main_output_buffer_imag 2 256
#array main_buffer 2 256
#array main_E 2 2048
LOD 8
SET main_E_arr_size
LOD 0
SET main_freq_count
#arrays main_Ehh 2 2048 "Ehh.txt"
LOD 8
SET main_Ehh_arr_size
LOD 0
SET main_freq_started
LOD 256
SET main_M
SET main_fft_limit
NEG_M 1
ADD main_M
SET main_sample_count
LOD 0
SET main_output_count
I2F_M 0
SET main_vector_count
LOD 0
SET main_buffer_head
@fim JMP fim
#ITRAD
LOD 1
OUT 1
NEG_M 1
ADD main_buffer_head
SET main_buffer_head
LOD 0
LES main_buffer_head
JIZ Lif1else
NEG_M 1
ADD main_M
SET main_buffer_head
@Lif1else LOD main_buffer_head
P_INN 0
I2F
P_LOD 1000000.0
SF_DIV
STI main_buffer
INN 1
SET main_frequencia_from_int
LOD 0
EQU main_freq_started
JIZ Lif2else
LOD 0
GRE main_frequencia_from_int
JIZ Lif3else
LOD main_frequencia_from_int
OUT 0
LOD 1
SET main_freq_started
LOD 0
SET main_freq_count
@Lif3else JMP Lif2end
@Lif2else LOD main_freq_count
ADD 1
SET main_freq_count
LOD 256
EQU main_freq_count
JIZ Lif4else
LOD main_frequencia_from_int
OUT 0
LOD 0
SET main_freq_count
@Lif4else @Lif2end NEG_M 1
ADD main_M
EQU main_sample_count
JIZ Lif5else
LOD 0
SET main_sample_count
LOD 0
SET main_mm
LOD main_buffer_head
SET main_ii
@Lwh1 LOD main_M
LES main_mm
JIZ Lwh1end
LOD  main_mm
MLT  main_E_arr_size
ADD  7
P_LOD main_mm
MLT main_E_arr_size
ADD 6
LDI main_E
STI main_E
LOD  main_mm
MLT  main_E_arr_size
ADD  6
P_LOD main_mm
MLT main_E_arr_size
ADD 5
LDI main_E
STI main_E
LOD  main_mm
MLT  main_E_arr_size
ADD  5
P_LOD main_mm
MLT main_E_arr_size
ADD 4
LDI main_E
STI main_E
LOD  main_mm
MLT  main_E_arr_size
ADD  4
P_LOD main_mm
MLT main_E_arr_size
ADD 3
LDI main_E
STI main_E
LOD  main_mm
MLT  main_E_arr_size
ADD  3
P_LOD main_mm
MLT main_E_arr_size
ADD 2
LDI main_E
STI main_E
LOD  main_mm
MLT  main_E_arr_size
ADD  2
P_LOD main_mm
MLT main_E_arr_size
ADD 1
LDI main_E
STI main_E
LOD  main_mm
MLT  main_E_arr_size
ADD  1
P_LOD main_mm
MLT main_E_arr_size
ADD 0
LDI main_E
STI main_E
LOD  main_mm
MLT  main_E_arr_size
ADD  0
P_LOD main_ii
LDI main_buffer
STI main_E
LOD main_mm
P_LOD main_mm
MLT main_Ehh_arr_size
ADD 0
LDI main_Ehh
P_LOD main_mm
MLT main_E_arr_size
ADD 0
LDI main_E
SF_MLT
P_LOD main_mm
MLT main_Ehh_arr_size
ADD 1
LDI main_Ehh
P_LOD main_mm
MLT main_E_arr_size
ADD 1
LDI main_E
SF_MLT
SF_ADD
P_LOD main_mm
MLT main_Ehh_arr_size
ADD 2
LDI main_Ehh
P_LOD main_mm
MLT main_E_arr_size
ADD 2
LDI main_E
SF_MLT
SF_ADD
P_LOD main_mm
MLT main_Ehh_arr_size
ADD 3
LDI main_Ehh
P_LOD main_mm
MLT main_E_arr_size
ADD 3
LDI main_E
SF_MLT
SF_ADD
P_LOD main_mm
MLT main_Ehh_arr_size
ADD 4
LDI main_Ehh
P_LOD main_mm
MLT main_E_arr_size
ADD 4
LDI main_E
SF_MLT
SF_ADD
P_LOD main_mm
MLT main_Ehh_arr_size
ADD 5
LDI main_Ehh
P_LOD main_mm
MLT main_E_arr_size
ADD 5
LDI main_E
SF_MLT
SF_ADD
P_LOD main_mm
MLT main_Ehh_arr_size
ADD 6
LDI main_Ehh
P_LOD main_mm
MLT main_E_arr_size
ADD 6
LDI main_E
SF_MLT
SF_ADD
P_LOD main_mm
MLT main_Ehh_arr_size
ADD 7
LDI main_Ehh
P_LOD main_mm
MLT main_E_arr_size
ADD 7
LDI main_E
SF_MLT
SF_ADD
SET_P aux_var
SET   aux_var2
P_LOD aux_var
STI E0
LOD   aux_var2
P_LOD 0.0
STI E0_i
LOD main_mm
ADD 1
SET main_mm
LOD main_ii
ADD 1
SET main_ii
LOD main_M
LES main_ii
LIN
JIZ Lif6else
LOD 0
SET main_ii
@Lif6else JMP Lwh1
@Lwh1end LOD 1
SET main_mmax
@Lwh2 LOD main_M
LES main_mmax
JIZ Lwh2end
LOD main_mmax
MLT 2
SET main_istep
LOD 0
SET main_m
LOD 0
SET main_ind
LOD 0
SET main_sind
@Lwh3 LOD main_mmax
LES main_m
JIZ Lwh3end
LOD main_m
SET main_q
@Lwh4 LOD main_M
LES main_q
JIZ Lwh4end
LOD main_q
ADD main_mmax
SET main_j
LOD main_sind
LDI wpv
P_LOD main_sind
LDI wpv_i
P_LOD main_j
ILI E0
P_LOD main_j
ILI E0_i
SET_P aux_var 
SET_P aux_var1
SET_P aux_var2
SET   aux_var3
F_MLT aux_var1
P_LOD aux_var 
F_MLT aux_var2
SF_SU2
P_LOD aux_var1
F_MLT aux_var2
P_LOD aux_var 
F_MLT aux_var3
SF_ADD
SET_P main_temp_i
SET main_temp
LOD main_j
P_LOD main_q
ILI E0
P_LOD main_q
ILI E0_i
SET_P aux_var
F_SU1 main_temp
P_LOD aux_var
F_SU1 main_temp_i
SET_P aux_var
SET_P aux_var2
SET   aux_var3
P_LOD aux_var2
ISI E0
LOD   aux_var3
P_LOD aux_var
ISI E0_i
LOD main_q
P_LOD main_q
ILI E0
P_LOD main_q
ILI E0_i
SET_P aux_var
F_ADD main_temp
P_LOD aux_var
F_ADD main_temp_i
SET_P aux_var
SET_P aux_var2
SET   aux_var3
P_LOD aux_var2
ISI E0
LOD   aux_var3
P_LOD aux_var
ISI E0_i
LOD main_q
ADD main_istep
SET main_q
LOD main_ind
ADD 1
SET main_ind
JMP Lwh4
@Lwh4end LOD main_ind
SET main_sind
LOD main_m
ADD 1
SET main_m
JMP Lwh3
@Lwh3end LOD main_istep
SET main_mmax
JMP Lwh2
@Lwh2end @Lwh5 LOD main_vector_count
P_I2F_M 50
SF_GRE
LIN
JIZ Lwh5end
F2I_M main_vector_count
SET   aux_var
ILI E0
P_LOD aux_var
ILI E0_i
SET_P aux_var
P_I2F_M 1000000
SF_MLT
P_LOD aux_var
P_I2F_M 1000000
SF_MLT
POP
F2I
OUT 0
F2I_M main_vector_count
SET   aux_var
ILI E0
P_LOD aux_var
ILI E0_i
SET_P aux_var
P_I2F_M 1000000
SF_MLT
P_LOD aux_var
P_I2F_M 1000000
SF_MLT
SET_P aux_var
LOD   aux_var
F2I
OUT 0
I2F_M 1
F_ADD main_vector_count
SET main_vector_count
JMP Lwh5
@Lwh5end I2F_M 0
SET main_vector_count
JMP Lif5end
@Lif5else LOD main_sample_count
ADD 1
SET main_sample_count
@Lif5end LOD 0
OUT 1
@fim JMP fim
