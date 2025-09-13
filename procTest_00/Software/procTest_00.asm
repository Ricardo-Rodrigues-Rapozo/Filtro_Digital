NOP
#PRNAME procTest_00
#NUBITS 23
#NDSTAC 5
#SDEPTH 5
#NUIOIN 1
#NUIOOU 2
#NBMANT 16
#NBEXPO 6
#PIPELN 3
#NUGAIN 128
#array h 11
#array x 11
@main LOD 0
P_LOD 0.01363158
STI h
LOD 1
P_LOD 0.02947376
STI h
LOD 2
P_LOD 0.07149450
STI h
LOD 3
P_LOD 0.12460785
STI h
LOD 4
P_LOD 0.16825941
STI h
LOD 5
P_LOD 0.18506581
STI h
LOD 6
P_LOD 0.16825941
STI h
LOD 7
P_LOD 0.12460785
STI h
LOD 8
P_LOD 0.07149450
STI h
LOD 9
P_LOD 0.02947376
STI h
LOD 10
P_LOD 0.01363158
STI h
LOD 11
SET tam_buff_input
LOD 11
SET tam_buff_coeffs
LOD 0
SET buff_circ_cont
LOD 0
SET coeffs_cont
LOD 0
SET pos
@L1 LOD 1
JIZ L1end
LOD buff_circ_cont
P_INN 0
I2F
F_MLT 0.001
STI x
I2F_M 0
SET y
LOD buff_circ_cont
SET pos
@L2 LOD tam_buff_coeffs
LES coeffs_cont
JIZ L2end
LOD coeffs_cont
LDI h
P_LOD pos
LDI x
SF_MLT
F_ADD y
SET y
LOD coeffs_cont
ADD 1
SET coeffs_cont
NEG_M 1
ADD pos
SET pos
LOD 0
LES pos
JIZ L3else
LOD pos
ADD tam_buff_input
SET pos
@L3else JMP L2
@L2end I2F_M 1000
F_MLT y
F2I
OUT 0
LOD 0
SET coeffs_cont
LOD buff_circ_cont
ADD 1
SET buff_circ_cont
LOD tam_buff_input
EQU buff_circ_cont
JIZ L4else
LOD 0
SET buff_circ_cont
@L4else JMP L1
@L1end @fim JMP fim
