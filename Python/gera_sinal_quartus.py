from pathlib import Path

import numpy as np
from sinaisIEC60255_118 import signal_frequency, frequency_ramp, modulation

# ===================================================
# Basic Parameters for Signal Generation
# ===================================================

f0 = 60
Nppc = 256 # para melhorar os resultados de harmonicos mais altos colocar 512
Fs = f0 * Nppc
Ts = 1/Fs
Nc = 1
t = np.arange((Nc + 100) * Nppc)*Ts

# ===================================================
# Basic Parameters for IEC60255_118 Tests
# ===================================================

hmax = 50
hmag = 0

Fr = 60
SNR = 6000000

f1 = 60
Rf = 1
fa = 54.75

x, Xr, fr, ROCOFr = signal_frequency(f1, (Nc)*Nppc, f0, Fs, Fr, hmax, hmag, SNR)

Nbits = 16
qmin = -(2**(Nbits - 1))
qmax = 2**(Nbits - 1) - 1
mask = 2**Nbits - 1

escala = np.max(np.abs(x))
if escala == 0:
    x_int = np.zeros_like(x, dtype=np.int32)
else:
    x_int = np.rint((x / escala) * qmax).astype(np.int32)

x_int = np.clip(x_int, qmin, qmax)
x_bin = np.array([format(int(valor) & mask, f"0{Nbits}b") for valor in x_int])

saida = Path(r"C:\Users\Ricardo\Documents\Dissertacao\Quartus\sinal_entrada_quartus.txt")
np.savetxt(saida, x_bin, fmt="%s")
