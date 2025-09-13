# =========================
# Imports
# =========================
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import freqz, lfilter, firls, upfirdn, firwin
import mplcursors
import sinaisIEC60255_118

from gerasinal import y, Nc, Nppc, Q, Fs


# =========================
# Função utilitária
# =========================
def ler_coluna(arquivo: str | Path, col: int = 0) -> np.ndarray:
    """Lê uma coluna específica de um arquivo .txt (índice começa em 0)."""
    try:
        x = np.loadtxt(arquivo, usecols=col, dtype=float, ndmin=1)
    except Exception as e:
        raise ValueError(f"Erro ao ler coluna {col} de {arquivo}: {e}")
    if x.size == 0:
        raise ValueError(f"Sem dados numéricos em {arquivo} (coluna {col})")
    return x


# =========================
# Script principal
# =========================
if __name__ == "__main__":
    # Caminhos
    dir_base = Path(r"C:\Users\Ricardo\Documents\Codigos_C\primeiro\procTest_00\Simulation")
    arq1 = dir_base / "input_0.txt"
    arq2 = dir_base / "output_0.txt"

    # Parâmetros
    fs = Fs  # Hz
    # Leitura (coluna 0)
    x1 = ler_coluna(arq1, col=0)
    y1 = ler_coluna(arq2, col=0)

    # Ajuste de tamanhos
    N = min(x1.size, y1.size)
    tam = N
    x1 = x1[:tam]
    y1 = y1[:tam]
    y1 =  (y1)
    print(f"Fs = {fs} Hz \n numero de amostras = {tam} \n número de ciclos = {(tam*60)/(fs):.2f}")

    # Eixo de tempo coerente com fs e tam
    t = np.arange(tam) / fs

    # Figura 1: entrada vs saída (C)
    plt.figure()
    plt.plot( x1 / Q, label="Entrada Cmm")
    plt.plot( y1 / Q, "--", label="Saída Cmm")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude")
    plt.title("Comparação de dois sinais (coluna 0)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Figura 2: saída Python vs saída C (mesmo tam)
    plt.figure()
    plt.plot(y[:tam], label="Saída Python")
    plt.plot(y1 / Q, "--", label="Saída Cmm")
    plt.xlabel("Amostra")
    plt.ylabel("Amplitude")
    plt.title("Saída Python vs Saída Cmm")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
