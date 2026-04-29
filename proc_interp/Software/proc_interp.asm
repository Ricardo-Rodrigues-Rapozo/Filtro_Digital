NOP
#PRNAME proc_interp
#NUBITS 32
#NDSTAC 5
#SDEPTH 5
#NUIOIN 1
#NUIOOU 1
#NBMANT 23
#NBEXPO 8
#NUGAIN 128
@main #array main_num_pre_BSP 2 6
#array main_den_pre_BSP 2 2
#array main_buffer_entrada_prefiltro 2 6
#array main_buffer_saida_prefiltro 2 2
#array main_buffer_entrada_farrow 2 4
LOD 0.0
SET main_alfa
LOD 0
SET main_cnt
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
P_LOD 16384.0
SF_DIV
SET main_x
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
P_LOD main_x
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
LOD 59.0
SET main_freq_smoothed
LOD main_freq_smoothed
F_DIV 60.0
SET main_lambda_val
LOD 0.0
SET main_y
LOD 6
GRE main_cnt
JIZ L1else
@L2 LOD main_alfa
P_LOD 1.0
SF_LES
JIZ L2end
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
LOD main_alfa
F_MLT main_alfa
F_MLT main_alfa
F_MLT main_H0
P_LOD main_alfa
F_MLT main_alfa
F_MLT main_H1
SF_ADD
P_LOD main_alfa
F_MLT main_H2
SF_ADD
F_ADD main_H3
SET main_y
I2F_M 100000
F_MLT main_y
F2I
OUT 0
LOD main_alfa
F_ADD main_lambda_val
SET main_alfa
JMP L2
@L2end LOD main_alfa
F_SU1 1.0
SET main_alfa
JMP L1end
@L1else LOD main_cnt
ADD 1
SET main_cnt
@L1end @fim JMP fim
