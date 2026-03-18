import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SIMULATION_DIR = SCRIPT_DIR.parent
SRC_DIR = SIMULATION_DIR / "src"
INPUT_DIR = SIMULATION_DIR / "data" / "input"
OUTPUT_DIR = SIMULATION_DIR / "data" / "output"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from DSPEPS import BSplineInterp, FlatTopFilterBase, PolyphaseFilterBank

f0 = 60
Nppc = 256
Fs = Nppc * f0

x = np.loadtxt(INPUT_DIR / "interpolador_entrada_59.txt") / (2**14) ## Entrada interpolador Python 
xiS = np.loadtxt(OUTPUT_DIR / "saida_59hz_interpolador_sapho.txt") / 10000 ## Saida interpolador SAPHO
out = np.loadtxt(OUTPUT_DIR / "saida_banco_59hz.txt") ## Saida Banco polifasico SAPHO (real e imaginaria intercalados)
sinal_60 = np.loadtxt(INPUT_DIR / "input_0.txt")  ## Entrada interpolador Python para 60Hz

### input_0 foi gerado no gerainput do python

plt.plot(sinal_60, "+-", label="Entrada Interp Sapho")
cursor = mplcursors.cursor(hover=True)
plt.show(block=True)
xiS = xiS[253:509]

real = out[0::2] / 1000000
imag = out[1::2] / 1000000

fasores = real + 1j * imag

N = len(fasores) // 50
fasores = fasores[0:50 * N]

fasor_h = fasores.reshape(50, N, order="F")
fasor_h = fasor_h[1:50, :]

AFT = 2 * np.abs(fasor_h)
PFT = np.rad2deg(np.angle(fasor_h))

MBSP = 5
freq = 59 * np.ones(len(x))

xi = BSplineInterp(x, f0, freq, MBSP, Fs)

# plt.plot(xi[253:509], "+-", label="Entrada Interp Sapho")
# cursor = mplcursors.cursor(hover=True)
# plt.show(block=True)
xi = xi[253:509]
sinal_60 = sinal_60[253:509] / np.max(np.abs(sinal_60[253:509]))
xi = xi / np.max(np.abs(xi[253:509]))
xiS = xiS / np.max(np.abs(xiS[253:509]))


freq_eixo = np.arange(0, len(xi)) * (Fs / Nppc)


plt.figure()


plt.title("Interpolacao")
plt.legend()
plt.show(block=False)

Nfft = Nppc
xi_fft = xi[:Nfft]
xiS_fft = xiS[:Nfft]
sinal_60_fft = sinal_60[:Nfft]

FFT_xi = np.fft.fft(xi_fft)
FFT_xiS = np.fft.fft(xiS_fft)
FFT_sinal_60 = np.fft.fft(sinal_60_fft)

mag_xi = 2 * np.abs(FFT_xi) / Nfft
mag_xiS = 2 * np.abs(FFT_xiS) / Nfft
mag_60 = 2 * np.abs(FFT_sinal_60) / Nfft

mag_xi = mag_xi / np.max(mag_xi)
mag_xiS = mag_xiS / np.max(mag_xiS)
mag_60 = mag_60 / np.max(mag_60)

plt.figure()
plt.stem(freq_eixo[0:Nfft//2], mag_xi[0:Nfft//2], label="Interpolacao Python", linefmt = 'r')
plt.stem(freq_eixo[0:Nfft//2], mag_xiS[0:Nfft//2], label="Interpolacao SAPHO", linefmt = 'b')
plt.stem(freq_eixo[0:Nfft//2], mag_60[0:Nfft//2], label="Entrada 60Hz_signal_frequency", linefmt = 'k')

plt.title("FFT dos sinais interpolados")
plt.xlabel("Frequencia [Hz]")
plt.ylabel("Magnitude normalizada")
plt.legend()
plt.grid(True)
plt.show()

# h = FlatTopFilterBase(8 * Nppc)
# M = Fs // f0
# X = PolyphaseFilterBank(h, M, xi)

# plt.figure()
# plt.subplot(211)
# plt.plot(np.abs(X[1, :]), "+-", label="Amp Python")
# plt.plot(AFT[0, :], "+-", label="Amp SAPHO")
# mplcursors.cursor(hover=True)
# plt.legend()

# plt.subplot(212)
# plt.plot(np.angle(X[1, :]), "+-", label="Fase Python")
# plt.plot(PFT[0, :], "+-", label="Fase SAPHO")
# plt.title("Saida Banco")
# plt.legend()
# mplcursors.cursor(hover=True)
# plt.show()
