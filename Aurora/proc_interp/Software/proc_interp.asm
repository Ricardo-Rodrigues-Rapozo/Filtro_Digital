NOP
#PRNAME proc_interp
#NUBITS 32
#NDSTAC 5
#SDEPTH 5
#NUIOIN 1
#NUIOOU 5
#NBMANT 23
#NBEXPO 8
#NUGAIN 128
@main LOD 0
SET main_cont_global
#arrays main_b_sos 2 9 "b_sos.txt"
#arrays main_a_sos 2 9 "a_sos.txt"
#array main_x1 2 3
LOD 0
P_LOD 0.0
STI main_x1
LOD 1
P_LOD 0.0
STI main_x1
LOD 2
P_LOD 0.0
STI main_x1
#array main_y1 2 3
LOD 0
P_LOD 0.0
STI main_y1
LOD 1
P_LOD 0.0
STI main_y1
LOD 2
P_LOD 0.0
STI main_y1
#array main_x2 2 3
LOD 0
P_LOD 0.0
STI main_x2
LOD 1
P_LOD 0.0
STI main_x2
LOD 2
P_LOD 0.0
STI main_x2
#array main_y2 2 3
LOD 0
P_LOD 0.0
STI main_y2
LOD 1
P_LOD 0.0
STI main_y2
LOD 2
P_LOD 0.0
STI main_y2
#array main_x3 2 3
LOD 0
P_LOD 0.0
STI main_x3
LOD 1
P_LOD 0.0
STI main_x3
LOD 2
P_LOD 0.0
STI main_x3
#array main_y3 2 3
LOD 0
P_LOD 0.0
STI main_y3
LOD 1
P_LOD 0.0
STI main_y3
LOD 2
P_LOD 0.0
STI main_y3
LOD 0
SET main_b_index
LOD 0
SET main_k_idx
LOD 0.0
SET main_acc_b
LOD 0.0
SET main_acc_a
LOD 127
SET main_atraso_amotras_filtro_pre_zc
#arrays main_bm_sos 2 9 "bm_sos.txt"
#arrays main_am_sos 2 9 "am_sos.txt"
#array main_xm1 2 3
LOD 0
P_LOD 0.0
STI main_xm1
LOD 1
P_LOD 0.0
STI main_xm1
LOD 2
P_LOD 0.0
STI main_xm1
#array main_ym1 2 3
LOD 0
P_LOD 0.0
STI main_ym1
LOD 1
P_LOD 0.0
STI main_ym1
LOD 2
P_LOD 0.0
STI main_ym1
#array main_xm2 2 3
LOD 0
P_LOD 0.0
STI main_xm2
LOD 1
P_LOD 0.0
STI main_xm2
LOD 2
P_LOD 0.0
STI main_xm2
#array main_ym2 2 3
LOD 0
P_LOD 0.0
STI main_ym2
LOD 1
P_LOD 0.0
STI main_ym2
LOD 2
P_LOD 0.0
STI main_ym2
#array main_xm3 2 3
LOD 0
P_LOD 0.0
STI main_xm3
LOD 1
P_LOD 0.0
STI main_xm3
LOD 2
P_LOD 0.0
STI main_xm3
#array main_ym3 2 3
LOD 0
P_LOD 0.0
STI main_ym3
LOD 1
P_LOD 0.0
STI main_ym3
LOD 2
P_LOD 0.0
STI main_ym3
LOD 0
SET main_bm_index
LOD 0
SET main_km_idx
LOD 0.0
SET main_accm_b
LOD 0.0
SET main_accm_a
LOD 0.0
SET main_fcc
LOD 381
SET main_atraso_pos_zc
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
LOD 128
SET main_atraso_ZC
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
I2F_M 1024
SET main_discard_samples
#array main_num_pre_BSP 2 6
#array main_den_pre_BSP 2 2
#array main_buffer_entrada_prefiltro 2 6
#array main_buffer_saida_prefiltro 2 2
LOD 445
SET main_atraso_geral
LOD 0
SET main_c_index
LOD 0
SET main_read_c_idx
#array main_buffer_atraso_x 2 445
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
@fim JMP fim
#ITRAD
INN 0
I2F
P_LOD 32768.0
SF_DIV
SET main_x
LOD 0
P_LOD main_x
STI main_x1
LOD 0
P_LOD 0
LDI main_b_sos
P_LOD 0
LDI main_x1
SF_MLT
P_LOD 1
LDI main_b_sos
P_LOD 1
LDI main_x1
SF_MLT
SF_ADD
P_LOD 2
LDI main_b_sos
P_LOD 2
LDI main_x1
SF_MLT
SF_ADD
P_LOD 1
LDI main_a_sos
P_LOD 1
LDI main_y1
SF_MLT
SF_SU2
P_LOD 2
LDI main_a_sos
P_LOD 2
LDI main_y1
SF_MLT
SF_SU2
STI main_y1
LOD 2
P_LOD 1
LDI main_x1
STI main_x1
LOD 1
P_LOD 0
LDI main_x1
STI main_x1
LOD 2
P_LOD 1
LDI main_y1
STI main_y1
LOD 1
P_LOD 0
LDI main_y1
STI main_y1
LOD 0
P_LOD 0
LDI main_y1
STI main_x2
LOD 0
P_LOD 3
LDI main_b_sos
P_LOD 0
LDI main_x2
SF_MLT
P_LOD 4
LDI main_b_sos
P_LOD 1
LDI main_x2
SF_MLT
SF_ADD
P_LOD 5
LDI main_b_sos
P_LOD 2
LDI main_x2
SF_MLT
SF_ADD
P_LOD 4
LDI main_a_sos
P_LOD 1
LDI main_y2
SF_MLT
SF_SU2
P_LOD 5
LDI main_a_sos
P_LOD 2
LDI main_y2
SF_MLT
SF_SU2
STI main_y2
LOD 2
P_LOD 1
LDI main_x2
STI main_x2
LOD 1
P_LOD 0
LDI main_x2
STI main_x2
LOD 2
P_LOD 1
LDI main_y2
STI main_y2
LOD 1
P_LOD 0
LDI main_y2
STI main_y2
LOD 0
P_LOD 0
LDI main_y2
STI main_x3
LOD 0
P_LOD 6
LDI main_b_sos
P_LOD 0
LDI main_x3
SF_MLT
P_LOD 7
LDI main_b_sos
P_LOD 1
LDI main_x3
SF_MLT
SF_ADD
P_LOD 8
LDI main_b_sos
P_LOD 2
LDI main_x3
SF_MLT
SF_ADD
P_LOD 7
LDI main_a_sos
P_LOD 1
LDI main_y3
SF_MLT
SF_SU2
P_LOD 8
LDI main_a_sos
P_LOD 2
LDI main_y3
SF_MLT
SF_SU2
STI main_y3
LOD 2
P_LOD 1
LDI main_x3
STI main_x3
LOD 1
P_LOD 0
LDI main_x3
STI main_x3
LOD 2
P_LOD 1
LDI main_y3
STI main_y3
LOD 1
P_LOD 0
LDI main_y3
STI main_y3
LOD 0
LDI main_y3
SET main_acc
I2F_M 1000000
F_MLT main_acc
F2I
OUT 3
LOD main_freq_amostragem
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
JIZ Lif1else
LOD main_acc
F_SU1 main_va
F_DIV main_acc
SET main_Nb
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
@Lif1else LOD main_acc
SET main_va
I2F_M 1000000
F_MLT main_fzc
F2I
OUT 1
LOD 0
P_LOD main_fzc
STI main_xm1
LOD 0
P_LOD 0
LDI main_bm_sos
P_LOD 0
LDI main_xm1
SF_MLT
P_LOD 1
LDI main_bm_sos
P_LOD 1
LDI main_xm1
SF_MLT
SF_ADD
P_LOD 2
LDI main_bm_sos
P_LOD 2
LDI main_xm1
SF_MLT
SF_ADD
P_LOD 1
LDI main_am_sos
P_LOD 1
LDI main_ym1
SF_MLT
SF_SU2
P_LOD 2
LDI main_am_sos
P_LOD 2
LDI main_ym1
SF_MLT
SF_SU2
STI main_ym1
LOD 2
P_LOD 1
LDI main_xm1
STI main_xm1
LOD 1
P_LOD 0
LDI main_xm1
STI main_xm1
LOD 2
P_LOD 1
LDI main_ym1
STI main_ym1
LOD 1
P_LOD 0
LDI main_ym1
STI main_ym1
LOD 0
P_LOD 0
LDI main_ym1
STI main_xm2
LOD 0
P_LOD 3
LDI main_bm_sos
P_LOD 0
LDI main_xm2
SF_MLT
P_LOD 4
LDI main_bm_sos
P_LOD 1
LDI main_xm2
SF_MLT
SF_ADD
P_LOD 5
LDI main_bm_sos
P_LOD 2
LDI main_xm2
SF_MLT
SF_ADD
P_LOD 4
LDI main_am_sos
P_LOD 1
LDI main_ym2
SF_MLT
SF_SU2
P_LOD 5
LDI main_am_sos
P_LOD 2
LDI main_ym2
SF_MLT
SF_SU2
STI main_ym2
LOD 2
P_LOD 1
LDI main_xm2
STI main_xm2
LOD 1
P_LOD 0
LDI main_xm2
STI main_xm2
LOD 2
P_LOD 1
LDI main_ym2
STI main_ym2
LOD 1
P_LOD 0
LDI main_ym2
STI main_ym2
LOD 0
P_LOD 0
LDI main_ym2
STI main_xm3
LOD 0
P_LOD 6
LDI main_bm_sos
P_LOD 0
LDI main_xm3
SF_MLT
P_LOD 7
LDI main_bm_sos
P_LOD 1
LDI main_xm3
SF_MLT
SF_ADD
P_LOD 8
LDI main_bm_sos
P_LOD 2
LDI main_xm3
SF_MLT
SF_ADD
P_LOD 7
LDI main_am_sos
P_LOD 1
LDI main_ym3
SF_MLT
SF_SU2
P_LOD 8
LDI main_am_sos
P_LOD 2
LDI main_ym3
SF_MLT
SF_SU2
STI main_ym3
LOD 2
P_LOD 1
LDI main_xm3
STI main_xm3
LOD 1
P_LOD 0
LDI main_xm3
STI main_xm3
LOD 2
P_LOD 1
LDI main_ym3
STI main_ym3
LOD 1
P_LOD 0
LDI main_ym3
STI main_ym3
LOD 0
LDI main_ym3
SET main_fcc
I2F_M 1000000
F_MLT main_fcc
F2I
OUT 2
LOD 0
GRE main_atraso_geral
JIZ Lif2else
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
JIZ Lif3else
LOD 0
SET main_c_index
@Lif3else JMP Lif2end
@Lif2else LOD main_x
SET main_x_atrasado
@Lif2end I2F_M main_cont_global
P_LOD main_discard_samples
SF_GRE
JIZ Lif4else
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
P_LOD 0.0
S_EQU
LIN
JIZ Lif5else
LOD main_freq_atrasada
F_DIV 60.0
SET main_lambda_val
JMP Lif5end
@Lif5else LOD 0.0
SET main_lambda_val
@Lif5end I2F_M 1000000
F_MLT main_freq_atrasada
F2I
OUT 4
LOD 0.0
SET main_y
LOD 6
GRE main_cnt
JIZ Lif6else
@Lwh1 LOD main_alfa
P_LOD 1.0
SF_LES
JIZ Lwh1end
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
OUT 0
LOD main_alfa
F_ADD main_lambda_val
SET main_alfa
JMP Lwh1
@Lwh1end LOD main_alfa
F_SU1 1.0
SET main_alfa
JMP Lif6end
@Lif6else LOD main_cnt
ADD 1
SET main_cnt
@Lif6end @Lif4else LOD 10000
LES main_cont_global
JIZ Lif7else
LOD main_cont_global
ADD 1
SET main_cont_global
@Lif7else @fim JMP fim
