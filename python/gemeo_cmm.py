
# Filtro polifásico para decimação
# int M, n, k, L, m,r;
# float Mk;
# float Q;
# int tam_buff_input, tam_buff_coeffs, buff_circ_cont, coeffs_cont, head, pos;
# float h[10]; //coeficientes
# float y;
# float x[10]; // Buffer das amostras de entrada
# float xm[10]; // Buffer das amostras decimadas 
#float hm[10]; // coeficientes por fase 
#float ym[10][10]; // linhas são as fases(m) e as colunas são os taps(k) sendo que k <= L -1  
from pathlib import Path

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import freqz, lfilter, firls, upfirdn, firwin


def ler_coluna(arquivo: str | Path, col: int = 0) -> np.ndarray:
    """Lê uma coluna específica de um arquivo .txt (índice começa em 0)."""
    try:
        x = np.loadtxt(arquivo, usecols=col, dtype=float, ndmin=1)
    except Exception as e:
        raise ValueError(f"Erro ao ler coluna {col} de {arquivo}: {e}")
    if x.size == 0:
        raise ValueError(f"Sem dados numéricos em {arquivo} (coluna {col})")
    return x

def downsampling(a,b):
    if(a % b == 0):
        return b
    return 0



# --------------------------------- Coeficientes --------------------------------------
h = np.array([
    0.01363158,
    0.02947376,
    0.07149450,
    0.12460785,
    0.16825941,
    0.18506581,
    0.16825941,
    0.12460785,
    0.07149450,
    0.02947376,
    0.01363158
])
#---------------------------- PARAMETROS -------------------------------------------------------------
dir_base = Path(r"C:\Users\Ricardo\Documents\Dissertação\procTest_00\Simulation")
dir_base2 = Path(r"C:\Users\Ricardo\Documents\Dissertação\python")
arq1 = dir_base / "input_0.txt"
x1 = ler_coluna(arq1, col=0) ## entrada multiplicada por 1000


Q = 0.001 #; // Fator de decimação 
L = 10# ; // Tamanho do filtro 
M = 10# ; // Número de fases do filtro polifásico
Mk = 1/M #; // usado para iterar os taps do filtro polifásico
k = 0 #; // Percorre os taps da fase m
tam_buff_input = L #;  // Tamanho do buffer circular das amostras de entrada
tam_buff_coeffs = L #; // Tamanho do vetor de coefs do filtro
x = np.array(np.zeros(tam_buff_input)) #; // Buffer circular das amostras de entrada

# -------------------------- Contadores para os loops ------------------------------------------------
buff_circ_cont = 0 #; // Contador do buffer circular
coeffs_cont = 0 #; // Contador para o numero de coeffs
pos = 0 #; // Posição no Buffer circular
n = 0 #; // Índice de saída do filtro 
m = 0 #; // Índice que percorre qual fase esta sendo utilizada (0<= m <= M -1)
tam = len(x1) #; // Tamanho do sinal de entrada
real_time = 0 #; // Contador do tempo real (número de amostras processadas)
y = np.array(np.zeros(tam)) #; // Saída do filtro
y_prev = 0 #; // Saída anterior do filtro
for real_time in range(tam):
    # Buffer circular das amostras de entrada
    x[buff_circ_cont]    =  x1[real_time] * Q
    #y[real_time]   =   0
    pos   =   buff_circ_cont

    while(coeffs_cont < tam_buff_coeffs):
        y[real_time]    =    y_prev + h[coeffs_cont] * x[pos]
        y_prev  =   y[real_time]
        # Atualiza os contadores
        coeffs_cont    =    coeffs_cont + 1
        pos  =  pos - 1
        if(pos<0):
        
            pos   =   pos + tam_buff_input
        
    real_time   =   real_time + 1
    coeffs_cont    =    0
    buff_circ_cont   =   buff_circ_cont + 1
    if (buff_circ_cont   ==   tam_buff_input):
        buff_circ_cont    =    0

plt.plot(y ,'b')
plt.plot(x1 * Q,'r--')
plt.show()
