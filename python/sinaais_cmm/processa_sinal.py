# =========================
# Imports
# =========================
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import freqz, lfilter, firls, upfirdn, firwin
import mplcursors
import filtros_polifasicos_ref_Manso.sinaisIEC60255_118 as sinaisIEC60255_118

# =========================
# Parâmetros do sinal
# =========================
f0   = 60            # Hz
Nppc = 60            # pontos por ciclo
Fs   = f0 * Nppc     # frequência de amostragem (Hz)
Nc   = 100           # número de ciclos
Q    = 1000          # fator de escala para salvar inteiro
M = Fs//f0  # número de amostras por ciclo
print(f"Usado M = {M}")
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
    dir_base = Path(r"C:\Users\Ricardo\Documents\Dissertação\procTest_00\Simulation")
    dir_base2 = Path(r"C:\Users\Ricardo\Documents\Dissertação\python")
    arq1 = dir_base / "input_0.txt"
    arq2 = dir_base / "output_0.txt"
    arq3 = dir_base2 / "y_python.txt"

    # Parâmetros
    fs = Fs  # Hz
    # Leitura (coluna 0)
    x1 = ler_coluna(arq1, col=0) ## entrada 
    y1 = ler_coluna(arq2, col=0) ## saída Cmm
    y_python = ler_coluna(arq3, col=0) ## saída Python

    # Ajuste de tamanhos
    N = min(x1.size, y1.size)
    tam = N
    x1 = x1[:tam]
    y1 = y1[:tam]
    y = y_python[:tam]
    y1 =  (y1)
    print(f"Fs = {fs} Hz \n numero de amostras = {tam} \n número de ciclos = {(tam*60)/(fs):.2f}")

#===================================================
# Filtro FIR (ordem 10) - LOWPASS
#===================================================

    order = 99 ## antes era 10
    numtaps = order + 1
    fc = 80.0  # Hz (ajuste conforme desejado)
    h = firwin(numtaps=numtaps, cutoff=fc, fs=Fs, window='hamming', pass_zero='lowpass')
    print(h)
    # resposta ao impulso (opcional)
    w, H = freqz(h, worN=2048, fs=Fs)
    k = lfilter(h, 1.0, x1)  # filtra o sinal de entrada para comparação
    k = k[:tam]
    plt.figure()
    plt.plot(w, 20*np.log10(np.maximum(np.abs(H), 1e-12)))
    plt.grid(True); plt.xlabel('Frequência (Hz)'); plt.ylabel('Magnitude (dB)')
    plt.title('FIR Lowpass (ordem 10)')
    plt.show(block=True)

    # Eixo de tempo coerente com fs e tam
    #t = np.arange(tam) / fs

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