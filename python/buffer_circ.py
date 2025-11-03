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


def downsampling(a, b):
    if (a % b == 0):
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
    0.02947376
])

# ---------------------------- PARAMETROS -------------------------------------------------------------
dir_base = Path(r"C:\Users\Ricardo\Documents\Dissertação\procTest_00\Simulation")
dir_base2 = Path(r"C:\Users\Ricardo\Documents\Dissertação\python")
arq1 = dir_base / "input_0.txt"
x1 = ler_coluna(arq1, col=0)  # entrada multiplicada por 1000

Q = 0.001  # Fator de decimação 
M = 10     # Decimação e número de fases
tamanho_filtro = len(h)  # Tamanho do filtro
contador_posicao_buffer_circular = 0  # Cabeça do buffer circular
buffer_circular = np.zeros(4)  # Buffer circular
tamanho_buffer_circular = len(buffer_circular)  # Tamanho do buffer circular
count_real_time = 0  # Tempo real (índice de leitura do sinal de entrada)

while count_real_time < len(x1):
    # Buffer circular das amostras de entrada
    buffer_circular[contador_posicao_buffer_circular] = x1[count_real_time] * Q

    # Lógica do filtro aqui

    # Lógica de encerramento do buffer e contadores
    contador_posicao_buffer_circular = (contador_posicao_buffer_circular + 1) % tamanho_buffer_circular
    count_real_time += 1
