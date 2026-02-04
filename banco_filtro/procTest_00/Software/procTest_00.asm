NOP
#PRNAME procTest_00
#NUBITS 32
#NDSTAC 5
#SDEPTH 5
#NUIOIN 1
#NUIOOU 7
#NBMANT 23
#NBEXPO 8
#FFTSIZ 7
#NUGAIN 128
#array E0 3 128
#array E0_i 4 128
#arrays wpv 3 64 "wpv.txt"
#arrays wpv_i 4 64 "wpv.txt"
CAL main
@fim JMP fim
@ifft SET ifft_N
LOD 1
SET ifft_mmax
@L1 LOD ifft_N
LES ifft_mmax
JIZ L1end
LOD ifft_mmax
MLT 2
SET ifft_istep
LOD 0
SET ifft_m
LOD 0
SET ifft_ind
LOD 0
SET ifft_sind
@L2 LOD ifft_mmax
LES ifft_m
JIZ L2end
LOD ifft_m
SET ifft_k
@L3 LOD ifft_N
LES ifft_k
JIZ L3end
LOD ifft_k
ADD ifft_mmax
SET ifft_j
LOD ifft_sind
LDI wpv
P_LOD ifft_sind
LDI wpv_i
P_LOD ifft_j
ILI E0
P_LOD ifft_j
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
SET_P ifft_temp_i
SET ifft_temp
LOD ifft_j
P_LOD ifft_k
ILI E0
P_LOD ifft_k
ILI E0_i
SET_P aux_var
F_SU1 ifft_temp
P_LOD aux_var
F_SU1 ifft_temp_i
SET_P aux_var
SET_P aux_var2
SET   aux_var3
P_LOD aux_var2
ISI E0
LOD   aux_var3
P_LOD aux_var
ISI E0_i
LOD ifft_k
P_LOD ifft_k
ILI E0
P_LOD ifft_k
ILI E0_i
SET_P aux_var
F_ADD ifft_temp
P_LOD aux_var
F_ADD ifft_temp_i
SET_P aux_var
SET_P aux_var2
SET   aux_var3
P_LOD aux_var2
ISI E0
LOD   aux_var3
P_LOD aux_var
ISI E0_i
LOD ifft_k
ADD ifft_istep
SET ifft_k
LOD ifft_ind
ADD 1
SET ifft_ind
JMP L3
@L3end LOD ifft_ind
SET ifft_sind
LOD ifft_m
ADD 1
SET ifft_m
JMP L2
@L2end LOD ifft_istep
SET ifft_mmax
JMP L1
@L1end RET
@main LOD 0
SET main_sample_count
LOD 0
SET main_output_count
#array main_output_buffer_real 2 128
#array main_output_buffer_imag 2 128
#array main_buffer 2 128
#array main_E 2 1024
LOD 8
SET main_E_arr_size
#arrays main_Ehh 2 1024 "Ehh.txt"
LOD 8
SET main_Ehh_arr_size
LOD 128
SET main_M
LOD main_M
SET main_fft_limit
NEG_M 1
ADD main_M
SET main_sample_count
LOD 0
SET main_output_count
@L4 LOD 1
JIZ L4end
NEG_M 1
ADD main_M
SET main_k
@L5 LOD 0
GRE main_k
JIZ L5end
LOD main_k
P_NEG_M 1
ADD main_k
LDI main_buffer
STI main_buffer
NEG_M 1
ADD main_k
SET main_k
JMP L5
@L5end LOD 0
P_INN 0
I2F
P_LOD 16384.0
SF_DIV
STI main_buffer
NEG_M 1
ADD main_M
EQU main_sample_count
JIZ L6else
LOD 0
SET main_sample_count
LOD 0
SET main_mm
@L7 LOD main_M
LES main_mm
JIZ L7end
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
P_LOD main_mm
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
JMP L7
@L7end LOD main_M
CAL ifft
LOD 1
ILI E0
P_LOD 1
ILI E0_i
SET_P aux_var
P_I2F_M 1000000
SF_MLT
P_LOD aux_var
P_I2F_M 1000000
SF_MLT
POP
F2I
OUT 1
LOD 1
ILI E0
P_LOD 1
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
OUT 2
LOD 3
ILI E0
P_LOD 3
ILI E0_i
SET_P aux_var
P_I2F_M 1000000
SF_MLT
P_LOD aux_var
P_I2F_M 1000000
SF_MLT
POP
F2I
OUT 3
LOD 3
ILI E0
P_LOD 3
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
OUT 4
LOD 5
ILI E0
P_LOD 5
ILI E0_i
SET_P aux_var
P_I2F_M 1000000
SF_MLT
P_LOD aux_var
P_I2F_M 1000000
SF_MLT
POP
F2I
OUT 5
LOD 5
ILI E0
P_LOD 5
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
OUT 6
JMP L6end
@L6else LOD main_sample_count
ADD 1
SET main_sample_count
@L6end JMP L4
@L4end RET
