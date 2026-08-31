import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import mplcursors
from DSPEPS import BSplineInterp, FlatTopFilterBase, PolyphaseFilterBank, downsample, estima_f_zc, kf_trend_poly
from sinaisIEC60255_118 import modulation, signal_frequency, frequency_ramp
from scipy.signal import lfilter
from auxiliares import TVE, wrap_to_pi

# ==========================================================
# Esquema de cores (usado em todas as figuras)
# ==========================================================
COR_PY   = "#2a78d6"  # azul     - cálculo/sinal Python
COR_SAPHO  = "#eb6834"  # laranja  - cálculo/sinal do SAPHO (arquivos carregados do embarcado)
COR_REF  = "#008300"  # verde    - referência / sinal ideal
COR_DIFF = "#4a3aa7"  # violeta  - diferença / erro
COR_LIM  = "#d03b3b"  # vermelho - limite normativo

hmax = 50

# Leitura dos Arquivos de Saída do SAPHO
# ======================================================================================
BASE_DIR = Path(__file__).resolve().parents[1]
DADOS_DIR = BASE_DIR / "Aurora" / "dados_simulacao"
SAIDA_DIR = DADOS_DIR / "analise_saidas"

f_zc_sapho = np.loadtxt(Path(__file__).resolve().parents[1] / "Aurora" / "dados_simulacao" / "saida_interp1.txt", dtype=float) / 1000000.0
f_zc_sapho = f_zc_sapho[1:]  # Remove the first sample, which is zero

# O SAPHO despeja o DESVIO (fout 2 = dfreq), nao a frequencia absoluta: os 60 Hz sao
# somados aqui. Materializar 65 Hz em float32 custava meio ULP de vies (3.87e-6 Hz),
# que a integral da correcao de fase transformava em ~1% de TVE em h=50.
_freq_sapho_raw = np.loadtxt(Path(__file__).resolve().parents[1] / "Aurora" / "dados_simulacao" / "saida_interp2.txt", dtype=float) / 1000000.0 + 60.0
freq_sapho = _freq_sapho_raw[1:]  # Remove the first sample, which is zero

freq_desc_sapho = np.loadtxt(Path(__file__).resolve().parents[1] / "Aurora" / "dados_simulacao" / "saida_interp4.txt", dtype=float) / 1000000.0 + 50
freq_desc_sapho = freq_desc_sapho[1:]  # Remove the first sample, which is zero

x_atras_sapho = np.loadtxt(Path(__file__).resolve().parents[1] / "Aurora" / "dados_simulacao" / "saida_interp3.txt", dtype=float) / 1000000.0
x_atras_sapho = x_atras_sapho[1:]  # Remove the first sample, which is zero

x_int_sapho = np.loadtxt(Path(__file__).resolve().parents[1] / "Aurora" / "dados_simulacao" / "saida_interp0.txt", dtype=float) / 1000000.0
x_int_sapho = x_int_sapho[1:]  # Remove the first sample, which is zero

ARQ_SAPHO_BANCO = DADOS_DIR / "saida_banco0.txt"
out_banco = np.atleast_1d(np.loadtxt(ARQ_SAPHO_BANCO, dtype=float))

fasores_por_frame = hmax + 1
escalares_por_frame = 2 * fasores_por_frame
amostras_por_frame = 1 + escalares_por_frame

out_banco = out_banco[1:]  # remove o elemento de cabeçalho antes de calcular os frames
N_frames = len(out_banco) // amostras_por_frame
out_banco = out_banco[:N_frames * amostras_por_frame]

frames_banco = out_banco.reshape(N_frames, amostras_por_frame)

freq_banco_sapho = frames_banco[:, 0] / 1_000_000.0 + 50
fasores_banco = frames_banco[:, 1:]

real = fasores_banco[:, 0::2] / 1_000_000.0
imag = fasores_banco[:, 1::2] / 1_000_000.0

fasor_completo = (real + 1j * imag).T
X_sapho = fasor_completo[1:hmax+1, :]


# Setando parâmetros do sinal
# =======================================================================================
Nppc = 256
f0 = 60.0
Fs = f0 * Nppc
Ts = 1/Fs
Frep = 60.0

f1 = 65
hmag = 0.05
SNR = 1000000000000000000

Rf = 1
fa = 35

fm = 5
kx = 0.0
ka = 0.1

# Geração do Sinal de Referência para Comparação
#=========================================================================================

#x, Xr, fr, ROCOFr = signal_frequency(f1, 1600*Nppc, f0, Fs, Frep, hmax, hmag, SNR)
#x, Xr, fr, ROCOFr = frequency_ramp(Rf, 1820*Nppc, f0, fa, Fs, Frep, hmax, hmag, SNR)
x, Xr, fr, ROCOFr = modulation(fm, kx, ka, 1600*Nppc, f0, Fs, Frep, hmax, hmag, SNR)


# Salva o sinal gerado em arquivo de texto para uso no SAPHO
# =======================================================================================================

x_int = (x * 32768.0).astype(np.int32)    
saida_sapho = Path(__file__).resolve().parents[1] / "Aurora" / "dados_simulacao" / "sinal_teste.txt"
np.savetxt(saida_sapho, x_int, fmt='%d')
# saida_teste = Path(__file__).resolve().parents[1] / "Python"/"Testes"/"rampa"/"offnominal_65hz.txt"
# np.savetxt(saida_teste, x_int, fmt='%d')

# Plot dos Sinais para Comparação
# --------------------------------------
sns.set_theme(style="whitegrid", palette="tab10")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), sharex=True)

ax1.plot(x, marker="o", linewidth=0.8, markersize=3, color=COR_REF, label="Referencia Gerada")
ax1.set_xlabel("Amostra")
ax1.set_ylabel("Valor")
ax1.set_title("MU_ch4")
ax1.legend()

ax2.plot(fr, marker="o", linewidth=0.8, markersize=3, color=COR_REF, label="fr")
ax2.set_xlabel("Amostra")
ax2.set_ylabel("Frequência [Hz]")
ax2.set_title("Frequência de Referência")
ax2.legend()

plt.tight_layout()
# mplcursors.cursor([ax1, ax2], hover=True)
plt.show(block=False)


# Estimação da Frequência do Sinal de Entrada
#==========================================================================================

f_zc_m, zc_m_delay, f_zc, zc_delay, total_delay = estima_f_zc(x, 1/Fs, Nppc, plot_level=0)

tam = min(len(f_zc), len(fr), len(f_zc_sapho))
f_zc = f_zc[:tam]
fr = fr[:tam]
f_zc_sapho = f_zc_sapho[:tam]

plt.figure(figsize=(14, 4))
plt.plot(f_zc, marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="f_zc")
plt.plot(f_zc_sapho, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="f_zc_sapho")
plt.xlabel("Amostra")
plt.ylabel("Frequência [Hz]")
plt.title("Frequência Estimada (Kalman) vs Frequência de Referência")
plt.legend()
plt.tight_layout()
# mplcursors.cursor(hover=True)
plt.show(block=False)

discard_samples = 4*Nppc

x = x[discard_samples:]
f_zc = f_zc[discard_samples:]
fr = fr[discard_samples:]
ROCOFr = ROCOFr[discard_samples:]
Xr = Xr[:, discard_samples:]

# Kalman filter to estimate the tendency of the frequency
q = 1e-1;   # ajuste fino
r = 20;      # se a senoide for forte, aumente

f_ini = fa
out = kf_trend_poly(f_zc, f_ini, Ts, 1, q, r)
freq = out["b"].squeeze() #

tam = min(len(freq), len(fr), len(freq_sapho))
freq = freq[:tam]
fr = fr[:tam]
freq_sapho = freq_sapho[:tam]

plt.figure(figsize=(14, 4))
plt.plot(freq, marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="freq (Kalman)")
plt.plot(freq_sapho, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="freq_sapho")
plt.plot(fr, marker="o", linewidth=0.8, markersize=3, color=COR_REF, label="fr")
plt.xlabel("Amostra")
plt.ylabel("Frequência [Hz]")
plt.title("Frequência Estimada (Kalman) vs Frequência de Referência")
plt.legend()
plt.tight_layout()
# mplcursors.cursor(hover=True)
plt.show(block=False)

# Atraso do Sinal de Entrada para compensar o atraso da estimação da frequência
#------------------------------------------------------------------------------
delay = np.zeros(total_delay+1)
delay[-1] = 1.0

x = lfilter(delay, [1.0], x)

# para alinhar o tempo de f_zc, fr, Xr e ROCOFr com o tempo de x, considerando o delay introduzido pelo filtro de média móvel
# ---------------------------------------------------------------------------------------------------------------------------
fr = np.concatenate((np.zeros(total_delay), fr)) 
Xr = np.hstack((np.zeros((hmax, total_delay)), Xr)) 
ROCOFr  = np.concatenate((np.zeros(total_delay), ROCOFr)) 

# Discarding the initial samples to align the time axes of all signals
# --------------------------------------------------------------------
discard_samples = 1200*Nppc

freq = freq[discard_samples:]
x = x[discard_samples:]

fr = fr[discard_samples:]
Xr = Xr[:, discard_samples:]
ROCOFr = ROCOFr[discard_samples:]

fr = fr[:len(freq)]

tam = min(len(freq), len(freq_desc_sapho), len(fr))
freq = freq[:tam]
freq_desc_sapho = freq_desc_sapho[:tam]
fr = fr[:tam]


# Plot da Frequência Estimada por Zero-Crossing
# --------------------------------------
fig_fzc, (ax_fzc, ax_fzc_err) = plt.subplots(2, 1, figsize=(14, 7), sharex=True)

ax_fzc.plot(freq, marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="f_zc CH4")
ax_fzc.plot(freq_desc_sapho, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="f_zc_sapho")
ax_fzc.plot(fr, marker="o", linewidth=0.8, markersize=3, color=COR_REF, label="fr")
ax_fzc.set_xlabel("Ciclo")
ax_fzc.set_ylabel("Frequência [Hz]")
ax_fzc.set_title("Frequência Estimada")
ax_fzc.legend()

ax_fzc_err.plot(freq - fr, marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="freq - fr")
ax_fzc_err.plot(freq_desc_sapho - fr, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="freq_sapho - fr")
ax_fzc_err.set_xlabel("Ciclo")
ax_fzc_err.set_ylabel("Erro [Hz]")
ax_fzc_err.set_title("Erro de Estimação de Frequência")
ax_fzc_err.legend()

plt.tight_layout()
# mplcursors.cursor([ax_fzc, ax_fzc_err], hover=True)
plt.show(block=False)


# BSpline Interpolation
# ===================================================
MBSP = 5

tam = min(len(x), len(freq))
x = x[:tam]


xi = BSplineInterp(x, f0, freq, MBSP, Fs, plot_level=0)

# Plot BSpline vs Sinal Interpolado
# --------------------------------------
fig_xi, ax_xi = plt.subplots(2, 1, figsize=(14, 4))

ax_xi[0].plot(x, marker="o", linewidth=0.8, markersize=3, color=COR_REF, label="x (Referencia)")
ax_xi[0].plot(x_atras_sapho, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="x_atras_sapho (SAPHO)")
ax_xi[0].set_xlabel("Amostra")
ax_xi[0].set_ylabel("Valor")
ax_xi[0].set_title("Sinal Atrasado")
ax_xi[0].legend()

ax_xi[1].plot(xi, marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="xi (BSpline)")
ax_xi[1].plot(x_int_sapho, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="xint_ch4 (SAPHO)")
ax_xi[1].set_xlabel("Amostra")
ax_xi[1].set_ylabel("Valor")
ax_xi[1].set_title("BSpline Interpolation - xi vs xint_ch4")
ax_xi[1].legend()

plt.tight_layout()
# mplcursors.cursor([ax_xi], hover=True)
plt.show(block=False)

# Polyphase FilterBank
# ===================================================
M = int(Fs // f0)

h = FlatTopFilterBase(8*Nppc + 1) # Base Filter Definition - FlatTop 
fbDelay = (len(h))//(2*M)


# Cut the signals to the length of the polyphase filter bank output, which is equal to the number of samples that can be processed by the filter bank given its delay and decimation factor
# ------------------------------------------------------------------------------------------------------------------------------------------------------
xi = xi[:(len(xi)//Nppc)*Nppc]
Xr = Xr[:,:(len(Xr[0])//Nppc)*Nppc]
freq = freq[:(len(freq)//Nppc)*Nppc]
freq_desc_sapho = freq_desc_sapho[:(len(freq_desc_sapho)//Nppc)*Nppc]
fr = fr[:(len(fr)//Nppc)*Nppc]

X = PolyphaseFilterBank(h, M, xi)

X  = X[1:hmax+1,:len(freq)]
X_sapho = X_sapho[:, :len(freq)]

# Downsampling the frequency, fr and Xr to match the decimation factor of the polyphase filter bank
# ---------------------------------------------------------------------------------------------
freq = downsample(freq,M)
freq_desc_sapho = downsample(freq_desc_sapho,M)
Xr = downsample(Xr,M)
fr = downsample(fr,M)

# Compensating the delay introduced by the polyphase filter bank, which is equal to half the length of the filter divided by the decimation factor
# --------------------------------------------------------------------------------------------------------------------------------------
freq = np.concatenate((np.zeros(fbDelay), freq))
freq_desc_sapho = np.concatenate((np.zeros(fbDelay), freq_desc_sapho))
freq_banco_sapho = np.concatenate((np.zeros(fbDelay), freq_banco_sapho))
fr = np.concatenate((np.zeros(fbDelay), fr))
Xr = np.hstack((np.zeros((hmax, fbDelay)), Xr))

# Adjusting the length of the signals to match the number of samples of X
# --------------------------------------------------------------------------------------------------------------------------------------

tam = min(X.shape[1], freq.shape[0], X_sapho.shape[1])

freq = freq[:tam]
freq_desc_sapho = freq_desc_sapho[:tam]
freq_banco_sapho = freq_banco_sapho[:tam]
fr = fr[:tam]
Xr = Xr[:,:tam]

X = X[:,:tam]
AFT = 2*np.abs(X)
PFT = np.unwrap(np.angle(X))

X_sapho = X_sapho[:,:tam]
AFT_sapho = 2*np.abs(X_sapho)
PFT_sapho = np.unwrap(np.angle(X_sapho))

# ===================================================
# Phase Correction - Python
# ===================================================
delta_f = freq - f0
correc = np.zeros(len(delta_f))

# Trapezoidal Integration (without error accumulation)
for nn in range(1, len(delta_f)):
    if(nn >= fbDelay+1):
        correc[nn] = correc[nn-1] + np.pi*(delta_f[nn] + delta_f[nn-1])*(M*Ts) 

correc = correc -2*np.pi/Nppc #1*np.pi/128 #

# Multiplies the correction by each harmonic (h = 1:50)
h = np.arange(1, hmax+1).reshape(-1, 1)   # shape (50, 1)
correcH = h*correc

PFTc = np.unwrap((PFT) + np.unwrap(correcH)) 
Xc = AFT*np.exp(1j*PFTc)

# ===================================================
# Phase Correction - SAPHO
# ===================================================
delta_f_sapho = freq_desc_sapho  - f0
correc_sapho = np.zeros(len(delta_f_sapho))

# Trapezoidal Integration (without error accumulation)
for nn in range(1, len(delta_f_sapho)):
    if(nn >= fbDelay+1):
        correc_sapho[nn] = correc_sapho[nn-1] + np.pi*(delta_f_sapho[nn] + delta_f_sapho[nn-1])*(M*Ts) 

correc_sapho = correc_sapho -2*np.pi/Nppc #1*np.pi/128 #

# Multiplies the correction by each harmonic (h = 1:50)
h = np.arange(1, hmax+1).reshape(-1, 1)   # shape (50, 1)
correcH_sapho = h*correc_sapho

PFTc_sapho = np.unwrap((PFT_sapho) + np.unwrap(correcH_sapho)) 
Xc_sapho = AFT_sapho*np.exp(1j*PFTc_sapho)


# ===================================================
# Phase Correction - SAPHO - Freq FIFO
# ===================================================
delta_f_sapho_fifo = freq_banco_sapho  - f0
correc_sapho_fifo = np.zeros(len(delta_f_sapho_fifo))

# Trapezoidal Integration (without error accumulation)
for nn in range(1, len(delta_f_sapho_fifo)):
    if(nn >= fbDelay+1):
        correc_sapho_fifo[nn] = correc_sapho_fifo[nn-1] + np.pi*(delta_f_sapho_fifo[nn] + delta_f_sapho_fifo[nn-1])*(M*Ts) 

correc_sapho_fifo = correc_sapho_fifo -2*np.pi/Nppc #1*np.pi/128 #

# Multiplies the correction by each harmonic (h = 1:50)
h = np.arange(1, hmax+1).reshape(-1, 1)   # shape (50, 1)
correcH_sapho_fifo = h*correc_sapho_fifo

PFTc_sapho_fifo = np.unwrap((PFT_sapho) + np.unwrap(correcH_sapho_fifo)) 
Xc_sapho_fifo = AFT_sapho*np.exp(1j*PFTc_sapho_fifo)

# ===================================================
# Performance Analysis
# ===================================================
Aref = np.abs(Xr)
Pref = np.unwrap(np.angle(Xr))


# Plot dos deltaf e dos correcs
# --------------------------------------
fig_df, (ax_df, ax_correc) = plt.subplots(2, 1, figsize=(14, 7), sharex=True)

ax_df.plot(delta_f,       marker="o", linewidth=0.8, markersize=3, color=COR_PY,    label="delta_f")
ax_df.plot(delta_f_sapho, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="delta_f_sapho")
ax_df.plot(delta_f_sapho_fifo, marker="o", linewidth=0.8, markersize=3, color=COR_DIFF, label="delta_f_sapho_fifo")
ax_df.set_ylabel("Δf [Hz]")
ax_df.set_title("Desvio de Frequência (Δf)")
ax_df.legend()

ax_correc.plot(correc,       marker="o", linewidth=0.8, markersize=3, color=COR_PY,    label="correc")
ax_correc.plot(correc_sapho, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="correc_sapho")
ax_correc.plot(correc_sapho_fifo, marker="o", linewidth=0.8, markersize=3, color=COR_DIFF, label="correc_sapho_fifo")
ax_correc.set_xlabel("Amostra")
ax_correc.set_ylabel("Correção [rad]")
ax_correc.set_title("Correção de Fase")
ax_correc.legend()

plt.tight_layout()
mplcursors.cursor([ax_df, ax_correc], hover=True)
plt.show(block=False)


hh = 1

# Plot Amplitude e Fase - harmônica hh
# --------------------------------------
fig_perf, (ax_amp, ax_pha, ax_pft, ax_diff) = plt.subplots(4, 1, figsize=(14, 13), sharex=True)

ax_amp.plot(Aref[hh-1, :],    marker="o", linewidth=0.8, markersize=3, color=COR_REF, label="Aref")
ax_amp.plot(AFT[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="AFT")
ax_amp.plot(AFT_sapho[hh-1, :], marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="AFT_sapho")
ax_amp.set_xlabel("Amostra")
ax_amp.set_ylabel("Amplitude")
ax_amp.set_title(f"Amplitude - Harmônica {hh}")
ax_amp.legend()

ax_pha.plot(wrap_to_pi(Pref[hh-1, :])*180/np.pi,    marker="o", linewidth=0.8, markersize=3, color=COR_REF, label="Pref")
ax_pha.plot(wrap_to_pi(PFTc[hh-1, :])*180/np.pi,     marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="PFTc")
ax_pha.plot(wrap_to_pi(PFTc_sapho[hh-1, :])*180/np.pi, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="PFTc_sapho")
ax_pha.plot(wrap_to_pi(PFTc_sapho_fifo[hh-1, :])*180/np.pi, marker="o", linewidth=0.8, markersize=3, color=COR_DIFF, label="PFTc_sapho_fifo")
ax_pha.set_xlabel("Amostra")
ax_pha.set_ylabel("Fase [°]")
ax_pha.set_title(f"Fase - Harmônica {hh}")
ax_pha.legend()

ax_pft.plot(wrap_to_pi(PFT[hh-1, :])*180/np.pi,     marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="PFT")
ax_pft.plot(wrap_to_pi(PFT_sapho[hh-1, :])*180/np.pi, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="PFT_sapho")
ax_pft.set_xlabel("Amostra")
ax_pft.set_ylabel("Fase [°]")
ax_pft.set_title(f"Fase (sem correção) - Harmônica {hh}")
ax_pft.legend()

ax_diff.plot(correcH[hh-1, :]*180/np.pi, marker="o", linewidth=0.8, markersize=3, color=COR_DIFF, label="Correção Aplicada")
ax_diff.plot(correcH_sapho[hh-1, :]*180/np.pi, marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="Correção Aplicada SAPHO")
ax_diff.plot(correcH_sapho_fifo[hh-1, :]*180/np.pi, marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="Correção Aplicada SAPHO FIFO")
ax_diff.set_xlabel("Amostra")
ax_diff.set_ylabel("Correção [°]")
ax_diff.set_title(f"Correção de Fase Aplicada - Harmônica {hh}")
ax_diff.legend()

plt.tight_layout()
mplcursors.cursor([ax_amp, ax_pha, ax_pft, ax_diff], hover=True)
plt.show(block=False)

# Error Calculation
# ---------------------------------------------------
AFT   = AFT[:,2*fbDelay:] 
AFT_sapho   = AFT_sapho[:,2*fbDelay:]
AFT_sapho_fifo   = AFT_sapho
Aref  = Aref[:,2*fbDelay:] 
PFTc  = PFTc[:,2*fbDelay:] 
PFTc_sapho  = PFTc_sapho[:,2*fbDelay:]
PFTc_sapho_fifo  = PFTc_sapho_fifo[:,2*fbDelay:]
Pref  = Pref[:,2*fbDelay:] 

Xc    = Xc[:,2*fbDelay:] 
Xc_sapho    = Xc_sapho[:,2*fbDelay:]
Xc_sapho_fifo    = Xc_sapho_fifo[:,2*fbDelay:]
Xr    = Xr[:,2*fbDelay:] 
    
ErroAFT = 100*np.abs(AFT - Aref)/Aref            # Magnitude Error (%)
ErroAFT_sapho = 100*np.abs(AFT_sapho - Aref)/Aref            # Magnitude Error (%)
ErroAFT_sapho_fifo = 100*np.abs(AFT_sapho_fifo - Aref)/Aref            # Magnitude Error (%)

ErroPFT = (wrap_to_pi(PFTc - Pref))*180/np.pi    # Phase Error (°)
ErroPFT_sapho = (wrap_to_pi(PFTc_sapho - Pref))*180/np.pi    # Phase Error (°)
ErroPFT_sapho_fifo = (wrap_to_pi(PFTc_sapho_fifo - Pref))*180/np.pi    # Phase Error (°)

TVEFT = TVE(Xc,Xr)                       # TVE (%)                       
TVEFT_sapho = TVE(Xc_sapho,Xr)                       # TVE (%)
TVEFT_sapho_fifo = TVE(Xc_sapho_fifo,Xr)                       # TVE (%)

ErroAFT = ErroAFT[:,:1000]
ErroPFT = ErroPFT[:,:1000]
TVEFT = TVEFT[:,:1000] 
ErroAFT_sapho = ErroAFT_sapho[:,:1000]
ErroPFT_sapho = ErroPFT_sapho[:,:1000]
TVEFT_sapho = TVEFT_sapho[:,:1000] 
ErroAFT_sapho_fifo = ErroAFT_sapho_fifo[:,:1000]
ErroPFT_sapho_fifo = ErroPFT_sapho_fifo[:,:1000]
TVEFT_sapho_fifo = TVEFT_sapho_fifo[:,:1000]

fig_err, (ax_amag, ax_pha, ax_tve) = plt.subplots(3, 1, figsize=(14, 9), sharex=True)

ax_amag.plot(ErroAFT[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="Magnitude Error")
ax_amag.plot(ErroAFT_sapho[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="Magnitude Error SAPHO")
ax_amag.plot(ErroAFT_sapho_fifo[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_DIFF, label="Magnitude Error SAPHO FIFO")
ax_amag.set_ylabel("Erro (%)")
ax_amag.set_title(f"Magnitude Error - Harmônica {hh}")
ax_amag.legend()

ax_pha.plot(ErroPFT[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="Phase Error")
ax_pha.plot(ErroPFT_sapho[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="Phase Error SAPHO")
ax_pha.plot(ErroPFT_sapho_fifo[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_DIFF, label="Phase Error SAPHO FIFO")
ax_pha.set_ylabel("Erro (°)")
ax_pha.set_title(f"Phase Error - Harmônica {hh}")
ax_pha.legend()

ax_tve.plot(TVEFT[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_PY, label="TVE")
ax_tve.plot(TVEFT_sapho[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_SAPHO, label="TVE SAPHO")
ax_tve.plot(TVEFT_sapho_fifo[hh-1, :],     marker="o", linewidth=0.8, markersize=3, color=COR_DIFF, label="TVE SAPHO FIFO")
ax_tve.axhline(1.0, color=COR_LIM, linestyle="--", linewidth=1.0, label="Limit IEC/IEEE 60255-118-1")
ax_tve.set_xlabel("Amostra")
ax_tve.set_ylabel("TVE (%)")
ax_tve.set_title(f"Total Vector Error - Harmônica {hh}")
ax_tve.legend()

plt.tight_layout()
mplcursors.cursor([ax_amag, ax_pha, ax_tve], hover=True)
plt.show(block=False)


# Min, Max and Average Errors
# ---------------------------------------------------
ErroAFTmin = np.min(ErroAFT, axis=1)
ErroAFTmax = np.max(ErroAFT, axis=1)
ErroAFTavg = np.mean(ErroAFT, axis=1)
ErroAFTstd = np.std(ErroAFT, axis=1)

ErroAFT_sapho_min = np.min(ErroAFT_sapho, axis=1)
ErroAFT_sapho_max = np.max(ErroAFT_sapho, axis=1)
ErroAFT_sapho_avg = np.mean(ErroAFT_sapho, axis=1)
ErroAFT_sapho_std = np.std(ErroAFT_sapho, axis=1)

ErroAFT_sapho_fifo_min = np.min(ErroAFT_sapho_fifo, axis=1)
ErroAFT_sapho_fifo_max = np.max(ErroAFT_sapho_fifo, axis=1)
ErroAFT_sapho_fifo_avg = np.mean(ErroAFT_sapho_fifo, axis=1)
ErroAFT_sapho_fifo_std = np.std(ErroAFT_sapho_fifo, axis=1)

ErroPFTmin = np.min(ErroPFT, axis=1)
ErroPFTmax = np.max(ErroPFT, axis=1)
ErroPFTavg = np.mean(ErroPFT, axis=1)
ErroPFTstd = np.std(ErroPFT, axis=1)

ErroPFT_sapho_min = np.min(ErroPFT_sapho, axis=1)
ErroPFT_sapho_max = np.max(ErroPFT_sapho, axis=1)
ErroPFT_sapho_avg = np.mean(ErroPFT_sapho, axis=1)
ErroPFT_sapho_std = np.std(ErroPFT_sapho, axis=1)

ErroPFT_sapho_fifo_min = np.min(ErroPFT_sapho_fifo, axis=1)
ErroPFT_sapho_fifo_max = np.max(ErroPFT_sapho_fifo, axis=1)
ErroPFT_sapho_fifo_avg = np.mean(ErroPFT_sapho_fifo, axis=1)
ErroPFT_sapho_fifo_std = np.std(ErroPFT_sapho_fifo, axis=1)

TVEFTmin = np.min(TVEFT, axis=1)
TVEFTmax = np.max(TVEFT, axis=1)
TVEFTavg = np.mean(TVEFT, axis=1)
TVEFTstd = np.std(TVEFT, axis=1)

TVEFT_sapho_min = np.min(TVEFT_sapho, axis=1)
TVEFT_sapho_max = np.max(TVEFT_sapho, axis=1)
TVEFT_sapho_avg = np.mean(TVEFT_sapho, axis=1)
TVEFT_sapho_std = np.std(TVEFT_sapho, axis=1)

TVEFT_sapho_fifo_min = np.min(TVEFT_sapho_fifo, axis=1)
TVEFT_sapho_fifo_max = np.max(TVEFT_sapho_fifo, axis=1)
TVEFT_sapho_fifo_avg = np.mean(TVEFT_sapho_fifo, axis=1)
TVEFT_sapho_fifo_std = np.std(TVEFT_sapho_fifo, axis=1)

indh = np.arange(hmax)+1

TVElim = 1 # Limit IEC/IEEE 60255-118-1 for TVE (%)

def plot_error_stats(ax, x, avg, mx, std, ylabel, title,
                     avg_s=None, mx_s=None, std_s=None,
                     avg_f=None, mx_f=None, std_f=None):
    # Faixa min->max (fundo, bem clara)
    ax.fill_between(x, avg, mx, color=COR_PY, alpha=0.12, label="Maximum")
    # Faixa média +/- desvio padrao (com contorno para destacar)
    ax.fill_between(x, avg - std, avg + std, color=COR_DIFF, alpha=0.22,
                    edgecolor=COR_DIFF, linewidth=0.8, label="Average ± Std. Dev.")
    # Linha da media por cima de tudo
    ax.plot(x, avg, marker="o", linewidth=1.2, markersize=3.5,
            color=COR_PY, markerfacecolor="white", markeredgecolor=COR_PY,
            markeredgewidth=0.9, zorder=5, label="Average")

    # Grandezas SAPHO (opcional)
    if avg_s is not None:
        ax.fill_between(x, avg_s, mx_s, color=COR_SAPHO, alpha=0.12,
                        label="Maximum SAPHO")
        ax.fill_between(x, avg_s - std_s, avg_s + std_s, color=COR_SAPHO, alpha=0.18,
                        edgecolor=COR_SAPHO, linewidth=0.8,
                        label="Average ± Std. Dev. SAPHO")
        ax.plot(x, avg_s, marker="s", linewidth=1.2, markersize=3.5,
                color=COR_SAPHO, markerfacecolor="white", markeredgecolor=COR_SAPHO,
                markeredgewidth=0.9, zorder=6, label="Average SAPHO")

    # Grandezas SAPHO FIFO (opcional)
    if avg_f is not None:
        ax.fill_between(x, avg_f, mx_f, color=COR_REF, alpha=0.12,
                        label="Maximum SAPHO FIFO")
        ax.fill_between(x, avg_f - std_f, avg_f + std_f, color=COR_REF, alpha=0.18,
                        edgecolor=COR_REF, linewidth=0.8,
                        label="Average ± Std. Dev. SAPHO FIFO")
        ax.plot(x, avg_f, marker="^", linewidth=1.2, markersize=3.5,
                color=COR_REF, markerfacecolor="white", markeredgecolor=COR_REF,
                markeredgewidth=0.9, zorder=7, label="Average SAPHO FIFO")

    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight="bold")
    ax.grid(True, which="both", linestyle=":", linewidth=0.6, alpha=0.6)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.margins(x=0.01)
    ax.legend(loc="upper left", framealpha=0.9, ncol=3, fontsize=9)


fig_avg, (ax_amag2, ax_pha2, ax_tve2) = plt.subplots(3, 1, figsize=(14, 9), sharex=True)

plot_error_stats(ax_amag2, indh, ErroAFTavg, ErroAFTmax, ErroAFTstd, "Erro (%)", "Magnitude Error",
                 ErroAFT_sapho_avg, ErroAFT_sapho_max, ErroAFT_sapho_std,
                 ErroAFT_sapho_fifo_avg, ErroAFT_sapho_fifo_max, ErroAFT_sapho_fifo_std)

plot_error_stats(ax_pha2, indh, ErroPFTavg, ErroPFTmax, ErroPFTstd, "Erro (°)", "Phase Error",
                 ErroPFT_sapho_avg, ErroPFT_sapho_max, ErroPFT_sapho_std,
                 ErroPFT_sapho_fifo_avg, ErroPFT_sapho_fifo_max, ErroPFT_sapho_fifo_std)

plot_error_stats(ax_tve2, indh, TVEFTavg, TVEFTmax, TVEFTstd, "TVE (%)", f"Total Vector Error - Limite {TVElim}%",
                 TVEFT_sapho_avg, TVEFT_sapho_max, TVEFT_sapho_std,
                 TVEFT_sapho_fifo_avg, TVEFT_sapho_fifo_max, TVEFT_sapho_fifo_std)

ax_tve2.axhline(TVElim, color=COR_LIM, linestyle="--", linewidth=1.2, zorder=4, label="Limit IEC/IEEE 60255-118-1")
ax_tve2.set_xlabel("Harmônica")
ax_tve2.legend(loc="upper left", framealpha=0.9, ncol=4, fontsize=9)

fig_avg.suptitle(f"Errors for Harmonics up to {hmax}", fontsize=13, fontweight="bold")
plt.tight_layout()
mplcursors.cursor([ax_amag2, ax_pha2, ax_tve2], hover=True)
plt.show(block=True)