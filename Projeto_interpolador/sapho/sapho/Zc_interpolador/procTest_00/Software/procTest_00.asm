NOP
#PRNAME procTest_00
#NUBITS 32
#NDSTAC 5
#SDEPTH 5
#NUIOIN 1
#NUIOOU 6
#NBMANT 23
#NBEXPO 8
#NUGAIN 128
@main LOD 0
SET main_cont_global
#arrays main_b_coeffs 2 1025 "b_coeffs"
#array main_b_buffer 2 1025
LOD 0
SET main_b_index
LOD 0.0
SET main_va
I2F_M 1
P_LOD 60.0
SF_DIV
SET main_Tsc
LOD 0.0
SET main_T1
LOD 0.0
SET main_fzc
LOD 15360.0
SET main_freq_amostragem
LOD 0.0
SET main_sig
LOD 0.0
SET main_Nb
LOD 0.0
SET main_T2
LOD 512
SET main_atraso_amotras_filtro_pre_zc
#arrays main_w_coeffs 2 1024 "w_coeffs"
LOD 0
SET main_w_index
LOD 0.0
SET main_w_sum
#array main_buffer_media_movel 2 1025
LOD 0
SET main_buffer_media_movel_idex
LOD 0.0
SET main_fcc
LOD 1024
SET main_w_media
LOD 0
SET main_read_idx_mean
LOD 0
SET main_w_index_mean
LOD 0
SET main_p
LOD 0
SET main_b_index_mean
LOD 512
SET main_atraso_amotras_media_movel
LOD 0
SET main_j
LOD 0
SET main_read_idx
LOD 0.0
SET main_acc
LOD 60.0
SET main_freq_instant
LOD 0.0
SET main_Tsc_total
LOD 0.0
SET main_denom
LOD 1000.0
SET main_ESCALA
LOD 0.0
SET main_x_atrasado
LOD 0
SET main_c_index
LOD 0
SET main_read_c_idx
#array main_buffer_atraso_x 2 1152
#array main_num_pre_BSP 2 6
#array main_den_pre_BSP 2 2
#array main_buffer_entrada_prefiltro 2 6
#array main_buffer_saida_prefiltro 2 2
LOD 1152
SET main_atraso_geral
#array main_buffer_entrada_farrow 2 4
LOD 0.0
SET main_alfa
LOD 0
SET main_cnt
#array main_buffer_freq 2 7
LOD 0
P_LOD 0.0
STI main_buffer_freq
LOD 1
P_LOD 0.0
STI main_buffer_freq
LOD 2
P_LOD 0.0
STI main_buffer_freq
LOD 3
P_LOD 0.0
STI main_buffer_freq
LOD 4
P_LOD 0.0
STI main_buffer_freq
LOD 5
P_LOD 0.0
STI main_buffer_freq
LOD 6
P_LOD 0.0
STI main_buffer_freq
LOD 5
PF_NEG_M 0.00222058
STI main_num_pre_BSP
LOD 4
P_LOD 0.00828731
STI main_num_pre_BSP
LOD 3
PF_NEG_M 0.03092866
STI main_num_pre_BSP
LOD 2
P_LOD 0.11542732
STI main_num_pre_BSP
LOD 1
PF_NEG_M 0.43078062
STI main_num_pre_BSP
LOD 0
P_LOD 1.60769515
STI main_num_pre_BSP
LOD 0
P_LOD 1.0
STI main_den_pre_BSP
LOD 1
P_LOD 0.26794919
STI main_den_pre_BSP
@L1 LOD 1
JIZ L1end
INN 0
I2F
P_LOD 32768.0
SF_DIV
SET main_x
LOD main_b_index
P_LOD main_x
STI main_b_buffer
LOD 0.0
SET main_acc
LOD 0
SET main_j
@L2 LOD 1025
LES main_j
JIZ L2end
NEG_M main_j
ADD main_b_index
SET main_read_idx
LOD 0
LES main_read_idx
JIZ L3else
LOD main_read_idx
ADD 1025
SET main_read_idx
@L3else LOD main_j
LDI main_b_coeffs
P_LOD main_read_idx
LDI main_b_buffer
SF_MLT
F_ADD main_acc
SET main_acc
LOD main_j
ADD 1
SET main_j
JMP L2
@L2end I2F_M 1000000
F_MLT main_acc
F2I
OUT 0
LOD main_b_index
ADD 1
SET main_b_index
LOD 1025
LES main_b_index
LIN
JIZ L4else
LOD 0
SET main_b_index
@L4else LOD main_freq_amostragem
F_DIV 1.0
SET main_Ts
LOD main_va
F_MLT main_acc
SET main_sig
LOD main_Ts
F_ADD main_Tsc
SET main_Tsc
LOD main_sig
P_I2F_M 0
SF_LES
JIZ L5else
LOD main_acc
F_SU1 main_va
F_DIV main_acc
SET main_Nb
LOD main_Nb
F_MLT main_Ts
SET main_T2
LOD main_Tsc
F_ADD main_T1
F_SU1 main_T2
SET main_Tsc
I2F_M 2
F_MLT main_Tsc
SET   aux_var
I2F_M 1
P_LOD aux_var
SF_DIV
SET main_fzc
LOD main_T2
SET main_T1
I2F_M 0
SET main_Tsc
@L5else LOD main_acc
SET main_va
I2F_M 1000000
F_MLT main_fzc
F2I
OUT 1
LOD main_buffer_media_movel_idex
P_LOD main_fzc
STI main_buffer_media_movel
LOD 0.0
SET main_fcc
LOD 0
SET main_p
@L6 LOD main_w_media
LES main_p
JIZ L6end
NEG_M main_p
ADD main_buffer_media_movel_idex
SET main_read_idx_mean
LOD 0
LES main_read_idx_mean
JIZ L7else
LOD main_read_idx_mean
ADD main_w_media
SET main_read_idx_mean
@L7else LOD main_p
LDI main_w_coeffs
P_LOD main_read_idx_mean
LDI main_buffer_media_movel
SF_MLT
F_ADD main_fcc
SET main_fcc
LOD main_p
ADD 1
SET main_p
JMP L6
@L6end I2F_M 1000000
F_MLT main_fcc
F2I
OUT 2
LOD main_buffer_media_movel_idex
ADD 1
SET main_buffer_media_movel_idex
LOD main_w_media
LES main_buffer_media_movel_idex
LIN
JIZ L8else
LOD 0
SET main_buffer_media_movel_idex
@L8else LOD 0
GRE main_atraso_geral
JIZ L9else
LOD main_c_index
LDI main_buffer_atraso_x
SET main_x_atrasado
LOD main_c_index
P_LOD main_x
STI main_buffer_atraso_x
LOD main_c_index
ADD 1
SET main_c_index
LOD main_atraso_geral
LES main_c_index
LIN
JIZ L10else
LOD 0
SET main_c_index
@L10else JMP L9end
@L9else LOD main_x
SET main_x_atrasado
@L9end I2F_M 1000000
F_MLT main_x_atrasado
F2I
OUT 3
LOD 1023
GRE main_cont_global
JIZ L11else
LOD 0
P_LOD 1
LDI main_buffer_entrada_prefiltro
STI main_buffer_entrada_prefiltro
LOD 1
P_LOD 2
LDI main_buffer_entrada_prefiltro
STI main_buffer_entrada_prefiltro
LOD 2
P_LOD 3
LDI main_buffer_entrada_prefiltro
STI main_buffer_entrada_prefiltro
LOD 3
P_LOD 4
LDI main_buffer_entrada_prefiltro
STI main_buffer_entrada_prefiltro
LOD 4
P_LOD 5
LDI main_buffer_entrada_prefiltro
STI main_buffer_entrada_prefiltro
LOD 5
P_LOD main_x_atrasado
STI main_buffer_entrada_prefiltro
LOD 0
LDI main_buffer_entrada_prefiltro
P_LOD 0
LDI main_num_pre_BSP
SF_MLT
P_LOD 1
LDI main_buffer_entrada_prefiltro
P_LOD 1
LDI main_num_pre_BSP
SF_MLT
SF_ADD
P_LOD 2
LDI main_buffer_entrada_prefiltro
P_LOD 2
LDI main_num_pre_BSP
SF_MLT
SF_ADD
P_LOD 3
LDI main_buffer_entrada_prefiltro
P_LOD 3
LDI main_num_pre_BSP
SF_MLT
SF_ADD
P_LOD 4
LDI main_buffer_entrada_prefiltro
P_LOD 4
LDI main_num_pre_BSP
SF_MLT
SF_ADD
P_LOD 5
LDI main_buffer_entrada_prefiltro
P_LOD 5
LDI main_num_pre_BSP
SF_MLT
SF_ADD
SET main_dot_result
LOD 1
P_LOD 1
LDI main_den_pre_BSP
P_LOD 0
LDI main_buffer_saida_prefiltro
SF_MLT
F_SU2 main_dot_result
STI main_buffer_saida_prefiltro
LOD 0
P_LOD 1
LDI main_buffer_saida_prefiltro
STI main_buffer_saida_prefiltro
LOD 0
P_LOD 1
LDI main_buffer_entrada_farrow
STI main_buffer_entrada_farrow
LOD 1
P_LOD 2
LDI main_buffer_entrada_farrow
STI main_buffer_entrada_farrow
LOD 2
P_LOD 3
LDI main_buffer_entrada_farrow
STI main_buffer_entrada_farrow
LOD 3
P_LOD 1
LDI main_buffer_saida_prefiltro
STI main_buffer_entrada_farrow
LOD main_fcc
SET main_freq_smoothed
LOD 0
P_LOD 1
LDI main_buffer_freq
STI main_buffer_freq
LOD 1
P_LOD 2
LDI main_buffer_freq
STI main_buffer_freq
LOD 2
P_LOD 3
LDI main_buffer_freq
STI main_buffer_freq
LOD 3
P_LOD 4
LDI main_buffer_freq
STI main_buffer_freq
LOD 4
P_LOD 5
LDI main_buffer_freq
STI main_buffer_freq
LOD 5
P_LOD 6
LDI main_buffer_freq
STI main_buffer_freq
LOD 6
P_LOD main_freq_smoothed
STI main_buffer_freq
LOD 0
LDI main_buffer_freq
SET main_freq_atrasada
LOD main_freq_atrasada
P_LOD 0.0
S_EQU
LIN
JIZ L12else
LOD main_freq_atrasada
F_DIV 60.0
SET main_lambda_val
JMP L12end
@L12else LOD 0.0
SET main_lambda_val
@L12end I2F_M 1000000
F_MLT main_freq_smoothed
F2I
OUT 4
LOD 0.0
SET main_y
LOD 6
GRE main_cnt
JIZ L13else
@L14 LOD main_alfa
P_LOD 1.0
SF_LES
JIZ L14end
LOD 0
LDI main_buffer_entrada_farrow
F_MLT 0.1666666667
F_NEG
P_LOD 1
LDI main_buffer_entrada_farrow
F_MLT 0.5
SF_ADD
P_LOD 2
LDI main_buffer_entrada_farrow
F_MLT 0.5
F_NEG
SF_ADD
P_LOD 3
LDI main_buffer_entrada_farrow
F_MLT 0.1666666667
SF_ADD
SET main_H0
LOD 0
LDI main_buffer_entrada_farrow
F_MLT 0.5
P_LOD 1
LDI main_buffer_entrada_farrow
SF_SU2
P_LOD 2
LDI main_buffer_entrada_farrow
F_MLT 0.5
SF_ADD
SET main_H1
LOD 0
LDI main_buffer_entrada_farrow
F_MLT 0.5
F_NEG
P_LOD 2
LDI main_buffer_entrada_farrow
F_MLT 0.5
SF_ADD
SET main_H2
LOD 0
LDI main_buffer_entrada_farrow
F_MLT 0.1666666667
P_LOD 1
LDI main_buffer_entrada_farrow
F_MLT 0.6666666667
SF_ADD
P_LOD 2
LDI main_buffer_entrada_farrow
F_MLT 0.1666666667
SF_ADD
SET main_H3
LOD main_H0
F_MLT main_alfa
F_ADD main_H1
F_MLT main_alfa
F_ADD main_H2
F_MLT main_alfa
F_ADD main_H3
SET main_y
I2F_M 1000000
F_MLT main_y
F2I
OUT 5
LOD main_alfa
F_ADD main_lambda_val
SET main_alfa
JMP L14
@L14end LOD main_alfa
F_SU1 1.0
SET main_alfa
JMP L13end
@L13else LOD main_cnt
ADD 1
SET main_cnt
@L13end @L11else LOD 10000
LES main_cont_global
JIZ L15else
LOD main_cont_global
ADD 1
SET main_cont_global
@L15else JMP L1
@L1end @fim JMP fim
