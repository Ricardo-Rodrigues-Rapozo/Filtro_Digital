NOP
#PRNAME proc_interp
#NUBITS 32
#NDSTAC 10
#SDEPTH 10
#NUIOIN 1
#NUIOOU 5
#NBMANT 23
#NBEXPO 8
#NUGAIN 128
#FROUND 2
#SHARE main_teste main_teste0
#SHARE main_b_index main_teste0
#SHARE main_k_idx main_teste0
#SHARE main_acc_b main_teste0
#SHARE main_acc_a main_teste0
#SHARE main_Nb main_sig
#SHARE main_T2 main_sig
#SHARE main_atraso_amotras_filtro_pre_zc main_teste0
#SHARE main_w_coeff main_teste0
#SHARE main_w_index main_teste0
#SHARE main_w_sum main_teste0
#SHARE main_buffer_media_movel_idex main_teste0
#SHARE main_fcc main_Tsc
#SHARE main_w_media main_teste0
#SHARE main_read_idx_mean main_teste0
#SHARE main_w_index_mean main_teste0
#SHARE main_p main_teste0
#SHARE main_b_index_mean main_teste0
#SHARE main_atraso_amotras_media_movel main_teste0
#SHARE main_fvelho main_teste0
#SHARE main_df_pred main_Tsc
#SHARE main_j main_teste0
#SHARE main_read_idx main_teste0
#SHARE main_acc main_dfreq_pred
#SHARE main_freq_instant main_teste0
#SHARE main_Tsc_total main_teste0
#SHARE main_denom main_teste0
#SHARE main_ESCALA main_teste0
#SHARE main_x_atrasado main_dfreq_pred
#SHARE main_read_c_idx main_teste0
#SHARE main_x main_teste0
#SHARE __aux_var main_Tsc
#SHARE main_p00_pred main_sig
#SHARE main_p10_pred main_Ts
#SHARE main_y_kalman main_erro
#SHARE main_S_incerteza main_kah_u
#SHARE main_dot_result main_teste0
#SHARE main_freq_smoothed main_teste0
#SHARE main_freq_atrasada main_teste0
#SHARE main_lambda_val main_teste0
#SHARE main_y main_dfreq_pred
#SHARE main_H0 main_dfreq_pred
#SHARE main_H1 main_Tsc
#SHARE main_H2 main_sig
#SHARE main_H3 main_p01_pred
@main LOD 80
SET main_teste0
LOD 0
SET main_cont_global
LOD 0
SET main_teste
#arrays main_b_sos 2 9 "b_sos.txt"
#arrays main_a_sos 2 9 "a_sos.txt"
#array main_x1 2 3
LOD 0.0
SET_V main_x1 0
LOD 0.0
SET_V main_x1 1
LOD 0.0
SET_V main_x1 2
#array main_y1 2 3
LOD 0.0
SET_V main_y1 0
LOD 0.0
SET_V main_y1 1
LOD 0.0
SET_V main_y1 2
#array main_x2 2 3
LOD 0.0
SET_V main_x2 0
LOD 0.0
SET_V main_x2 1
LOD 0.0
SET_V main_x2 2
#array main_y2 2 3
LOD 0.0
SET_V main_y2 0
LOD 0.0
SET_V main_y2 1
LOD 0.0
SET_V main_y2 2
#array main_x3 2 3
LOD 0.0
SET_V main_x3 0
LOD 0.0
SET_V main_x3 1
LOD 0.0
SET_V main_x3 2
#array main_y3 2 3
LOD 0.0
SET_V main_y3 0
LOD 0.0
SET_V main_y3 1
LOD 0.0
SET_V main_y3 2
LOD 0
SET main_b_index
LOD 0
SET main_k_idx
LOD 0.0
SET main_acc_b
LOD 0.0
SET main_acc_a
LOD 0.0
SET main_va
LOD 1.0
P_LOD 60.0
SF_DIV
NOP
F_QUO
SET main_Tsc
LOD 0.0
SET main_T1
LOD 60.0
SET main_fzc
LOD 15360.0
SET main_freq_amostragem
LOD 0.0
SET main_sig
LOD 0.0
SET main_Nb
LOD 0.0
SET main_T2
LOD 127
SET main_atraso_amotras_filtro_pre_zc
LOD 0.0
SET main_cont_zc
LOD 0.00390625
SET main_w_coeff
LOD 0
SET main_w_index
LOD 0.0
SET main_w_sum
LOD 0
SET main_buffer_media_movel_idex
LOD 0.0
SET main_fcc
LOD 256
SET main_w_media
LOD 0
SET main_read_idx_mean
LOD 0
SET main_w_index_mean
LOD 0
SET main_p
LOD 0
SET main_b_index_mean
LOD 128
SET main_atraso_amotras_media_movel
LOD 0.0
SET main_fvelho
LOD 60.0
SET main_f_nominal
LOD 0.0
SET main_dfreq
LOD 0.0
SET main_df
LOD 1000000.0
SET main_p00
LOD 0.0
SET main_p01
LOD 0.0
SET main_p10
LOD 1000000.0
SET main_p11
LOD 1.0
P_LOD 15360.0
SF_DIV
NOP
F_QUO
P_LOD 1.0
P_LOD 15360.0
SF_DIV
NOP
F_QUO
SF_MLT
P_LOD 1.0
P_LOD 15360.0
SF_DIV
NOP
F_QUO
SF_MLT
F_MLT 0.1
P_LOD 3.0
SF_DIV
NOP
F_QUO
SET main_q00
LOD 1.0
P_LOD 15360.0
SF_DIV
NOP
F_QUO
P_LOD 1.0
P_LOD 15360.0
SF_DIV
NOP
F_QUO
SF_MLT
F_MLT 0.1
P_LOD 2.0
SF_DIV
NOP
F_QUO
SET main_q01
LOD 1.0
P_LOD 15360.0
SF_DIV
NOP
F_QUO
P_LOD 1.0
P_LOD 15360.0
SF_DIV
NOP
F_QUO
SF_MLT
F_MLT 0.1
P_LOD 2.0
SF_DIV
NOP
F_QUO
SET main_q10
LOD 15360.0
F_DIV 0.1
NOP
F_QUO
SET main_q11
LOD 0.0
SET main_dfreq_pred
LOD 0.0
SET main_df_pred
LOD 20.0
SET main_R
LOD 0
SET main_cont_kalman
LOD 1024
SET main_descarte_kalman
LOD 0.0
SET main_erro
LOD 0.0
SET main_comp_dfreq
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
#array main_buffer_atraso_x 2 255
#array main_num_pre_BSP 2 6
#array main_den_pre_BSP 2 2
#array main_buffer_entrada_prefiltro 2 6
#array main_buffer_saida_prefiltro 2 2
LOD 255
SET main_atraso_geral
#array main_buffer_entrada_farrow 2 4
LOD 0.0
SET main_alfa
LOD 0
SET main_cnt
#array main_buffer_freq 2 7
LOD 0.0
SET_V main_buffer_freq 0
LOD 0.0
SET_V main_buffer_freq 1
LOD 0.0
SET_V main_buffer_freq 2
LOD 0.0
SET_V main_buffer_freq 3
LOD 0.0
SET_V main_buffer_freq 4
LOD 0.0
SET_V main_buffer_freq 5
LOD 0.0
SET_V main_buffer_freq 6
LOD -0.00222058
SET_V main_num_pre_BSP 5
LOD 0.00828731
SET_V main_num_pre_BSP 4
LOD -0.03092866
SET_V main_num_pre_BSP 3
LOD 0.11542732
SET_V main_num_pre_BSP 2
LOD -0.43078062
SET_V main_num_pre_BSP 1
LOD 1.60769515
SET_V main_num_pre_BSP 0
LOD 1.0
SET_V main_den_pre_BSP 0
LOD 0.26794919
SET_V main_den_pre_BSP 1
@fim JMP fim
#ITRAD
INN 0
I2F
P_LOD 32768.0
SF_DIV
NOP
F_QUO
SET main_x
SET_V main_x1 0
LOD_V main_b_sos 0
P_LOD_V main_x1 0
SF_MLT
P_LOD_V main_b_sos 1
P_LOD_V main_x1 1
SF_MLT
SF_ADD
P_LOD_V main_b_sos 2
P_LOD_V main_x1 2
SF_MLT
SF_ADD
P_LOD_V main_a_sos 1
P_LOD_V main_y1 1
SF_MLT
SF_SU2
P_LOD_V main_a_sos 2
P_LOD_V main_y1 2
SF_MLT
SF_SU2
SET_V main_y1 0
LOD_V main_x1 1
SET_V main_x1 2
LOD_V main_x1 0
SET_V main_x1 1
LOD_V main_y1 1
SET_V main_y1 2
LOD_V main_y1 0
SET_V main_y1 1
LOD_V main_y1 0
SET_V main_x2 0
LOD_V main_b_sos 3
P_LOD_V main_x2 0
SF_MLT
P_LOD_V main_b_sos 4
P_LOD_V main_x2 1
SF_MLT
SF_ADD
P_LOD_V main_b_sos 5
P_LOD_V main_x2 2
SF_MLT
SF_ADD
P_LOD_V main_a_sos 4
P_LOD_V main_y2 1
SF_MLT
SF_SU2
P_LOD_V main_a_sos 5
P_LOD_V main_y2 2
SF_MLT
SF_SU2
SET_V main_y2 0
LOD_V main_x2 1
SET_V main_x2 2
LOD_V main_x2 0
SET_V main_x2 1
LOD_V main_y2 1
SET_V main_y2 2
LOD_V main_y2 0
SET_V main_y2 1
LOD_V main_y2 0
SET_V main_x3 0
LOD_V main_b_sos 6
P_LOD_V main_x3 0
SF_MLT
P_LOD_V main_b_sos 7
P_LOD_V main_x3 1
SF_MLT
SF_ADD
P_LOD_V main_b_sos 8
P_LOD_V main_x3 2
SF_MLT
SF_ADD
P_LOD_V main_a_sos 7
P_LOD_V main_y3 1
SF_MLT
SF_SU2
P_LOD_V main_a_sos 8
P_LOD_V main_y3 2
SF_MLT
SF_SU2
SET_V main_y3 0
LOD_V main_x3 1
SET_V main_x3 2
LOD_V main_x3 0
SET_V main_x3 1
LOD_V main_y3 1
SET_V main_y3 2
LOD_V main_y3 0
SET_V main_y3 1
LOD_V main_y3 0
SET main_acc
LOD main_freq_amostragem
F_DIV 1.0
NOP
F_QUO
SET main_Ts
LOD main_va
F_MLT main_acc
SET main_sig
LOD 1.0
F_ADD main_cont_zc
SET main_cont_zc
F_MLT main_Ts
SET main_Tsc
LOD 0.0
F_LES main_sig
JIZ __Lif1else
LOD main_acc
F_SU1 main_va
F_DIV main_acc
NOP
F_QUO
SET main_Nb
F_MLT main_Ts
SET main_T2
LOD main_Tsc
F_ADD main_T1
F_SU1 main_T2
SET main_Tsc
LOD 2.0
F_MLT main_Tsc
SET   __aux_var
LOD 1.0
P_LOD __aux_var
SF_DIV
NOP
F_QUO
SET main_fzc
LOD main_T2
SET main_T1
LOD 0.0
SET main_Tsc
LOD 0.0
SET main_cont_zc
@__Lif1else LOD main_acc
SET main_va
LOD 1000000.0
F_MLT main_fzc
F2I
OUT 1
LOD main_descarte_kalman
LES main_cont_kalman
LIN
JIZ __Lif2else
LOD main_Ts
F_MLT main_df
F_SU1 main_comp_dfreq
SET main_kah_u
LOD main_dfreq
F_ADD main_kah_u
SET main_kah_t
F_SU1 main_dfreq
F_SU1 main_kah_u
SET main_comp_dfreq
LOD main_kah_t
SET main_dfreq_pred
LOD main_df
SET main_df_pred
LOD main_Ts
F_MLT main_p10
F_ADD main_p00
P_LOD main_Ts
F_MLT main_p01
SF_ADD
P_LOD main_Ts
F_MLT main_Ts
F_MLT main_p11
SF_ADD
F_ADD main_q00
SET main_p00_pred
LOD main_Ts
F_MLT main_p11
F_ADD main_p01
F_ADD main_q01
SET main_p01_pred
LOD main_Ts
F_MLT main_p11
F_ADD main_p10
F_ADD main_q10
SET main_p10_pred
LOD main_p11
F_ADD main_q11
SET main_p11_pred
LOD main_fzc
F_SU1 main_f_nominal
SET main_y_kalman
F_SU1 main_dfreq_pred
SET main_erro
LOD main_p00_pred
F_ADD main_R
SET main_S_incerteza
F_DIV main_p00_pred
NOP
F_QUO
SET main_K0
LOD main_S_incerteza
F_DIV main_p10_pred
NOP
F_QUO
SET main_K1
LOD main_K0
F_MLT main_erro
F_SU1 main_comp_dfreq
SET main_kah_u
LOD main_dfreq_pred
F_ADD main_kah_u
SET main_kah_t
F_SU1 main_dfreq_pred
F_SU1 main_kah_u
SET main_comp_dfreq
LOD main_kah_t
SET main_dfreq
LOD main_K1
F_MLT main_erro
F_ADD main_df_pred
SET main_df
LOD 1.0
F_SU1 main_K0
F_MLT main_p00_pred
SET main_p00
LOD 1.0
F_SU1 main_K0
F_MLT main_p01_pred
SET main_p01
LOD main_K1
F_MLT main_p00_pred
F_SU2 main_p10_pred
SET main_p10
LOD main_K1
F_MLT main_p01_pred
F_SU2 main_p11_pred
SET main_p11
LOD main_f_nominal
F_ADD main_dfreq
SET main_fcc
LOD 1000000.0
F_MLT main_dfreq
F2I
OUT 2
LOD 0
GRE main_atraso_geral
JIZ __Lif3else
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
JIZ __Lif4else
LOD 0
SET main_c_index
@__Lif4else JMP __Lif3end
@__Lif3else LOD main_x
SET main_x_atrasado
@__Lif3end LOD 307200
LES main_cont_global
LIN
JIZ __Lif5else
LOD_V main_buffer_entrada_prefiltro 1
SET_V main_buffer_entrada_prefiltro 0
LOD_V main_buffer_entrada_prefiltro 2
SET_V main_buffer_entrada_prefiltro 1
LOD_V main_buffer_entrada_prefiltro 3
SET_V main_buffer_entrada_prefiltro 2
LOD_V main_buffer_entrada_prefiltro 4
SET_V main_buffer_entrada_prefiltro 3
LOD_V main_buffer_entrada_prefiltro 5
SET_V main_buffer_entrada_prefiltro 4
LOD main_x_atrasado
SET_V main_buffer_entrada_prefiltro 5
LOD_V main_buffer_entrada_prefiltro 0
P_LOD_V main_num_pre_BSP 0
SF_MLT
P_LOD_V main_buffer_entrada_prefiltro 1
P_LOD_V main_num_pre_BSP 1
SF_MLT
SF_ADD
P_LOD_V main_buffer_entrada_prefiltro 2
P_LOD_V main_num_pre_BSP 2
SF_MLT
SF_ADD
P_LOD_V main_buffer_entrada_prefiltro 3
P_LOD_V main_num_pre_BSP 3
SF_MLT
SF_ADD
P_LOD_V main_buffer_entrada_prefiltro 4
P_LOD_V main_num_pre_BSP 4
SF_MLT
SF_ADD
P_LOD_V main_buffer_entrada_prefiltro 5
P_LOD_V main_num_pre_BSP 5
SF_MLT
SF_ADD
SET main_dot_result
LOD_V main_den_pre_BSP 1
P_LOD_V main_buffer_saida_prefiltro 0
SF_MLT
F_SU2 main_dot_result
SET_V main_buffer_saida_prefiltro 1
LOD_V main_buffer_saida_prefiltro 1
SET_V main_buffer_saida_prefiltro 0
LOD_V main_buffer_entrada_farrow 1
SET_V main_buffer_entrada_farrow 0
LOD_V main_buffer_entrada_farrow 2
SET_V main_buffer_entrada_farrow 1
LOD_V main_buffer_entrada_farrow 3
SET_V main_buffer_entrada_farrow 2
LOD_V main_buffer_saida_prefiltro 1
SET_V main_buffer_entrada_farrow 3
LOD main_fcc
SET main_freq_smoothed
LOD_V main_buffer_freq 1
SET_V main_buffer_freq 0
LOD_V main_buffer_freq 2
SET_V main_buffer_freq 1
LOD_V main_buffer_freq 3
SET_V main_buffer_freq 2
LOD_V main_buffer_freq 4
SET_V main_buffer_freq 3
LOD_V main_buffer_freq 5
SET_V main_buffer_freq 4
LOD_V main_buffer_freq 6
SET_V main_buffer_freq 5
LOD main_freq_smoothed
SET_V main_buffer_freq 6
LOD_V main_buffer_freq 0
SET main_freq_atrasada
EQU 0.0
LIN
JIZ __Lif6else
LOD main_freq_atrasada
F_DIV 60.0
NOP
F_QUO
SET main_lambda_val
JMP __Lif6end
@__Lif6else LOD 0.0
SET main_lambda_val
@__Lif6end LOD 1000000.0
F_MLT main_x_atrasado
F2I
OUT 3
LOD main_dfreq
F_ADD 10.0
P_LOD 1000000.0
SF_MLT
F2I
OUT 4
LOD 0.0
SET main_y
LOD 6
GRE main_cnt
JIZ __Lif7else
@__Lwh1 LOD main_alfa
F_GRE 1.0
JIZ __Lwh1end
LOD_V main_buffer_entrada_farrow 0
F_MLT 0.1666666667
F_NEG
P_LOD_V main_buffer_entrada_farrow 1
F_MLT 0.5
SF_ADD
P_LOD_V main_buffer_entrada_farrow 2
F_MLT 0.5
F_NEG
SF_ADD
P_LOD_V main_buffer_entrada_farrow 3
F_MLT 0.1666666667
SF_ADD
SET main_H0
LOD_V main_buffer_entrada_farrow 0
F_MLT 0.5
P_LOD_V main_buffer_entrada_farrow 1
SF_SU2
P_LOD_V main_buffer_entrada_farrow 2
F_MLT 0.5
SF_ADD
SET main_H1
LOD_V main_buffer_entrada_farrow 0
F_MLT 0.5
F_NEG
P_LOD_V main_buffer_entrada_farrow 2
F_MLT 0.5
SF_ADD
SET main_H2
LOD_V main_buffer_entrada_farrow 0
F_MLT 0.1666666667
P_LOD_V main_buffer_entrada_farrow 1
F_MLT 0.6666666667
SF_ADD
P_LOD_V main_buffer_entrada_farrow 2
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
LOD 1000000.0
F_MLT main_y
F2I
OUT 0
LOD main_alfa
F_ADD main_lambda_val
SET main_alfa
JMP __Lwh1
@__Lwh1end LOD main_alfa
F_SU1 1.0
SET main_alfa
JMP __Lif7end
@__Lif7else LOD main_cnt
ADD 1
SET main_cnt
@__Lif7end @__Lif5else LOD 348160
LES main_cont_global
JIZ __Lif8else
LOD main_cont_global
ADD 1
SET main_cont_global
@__Lif8else @__Lif2else LOD 2000
LES main_cont_kalman
JIZ __Lif9else
LOD main_cont_kalman
ADD 1
SET main_cont_kalman
@__Lif9else @fim JMP fim
