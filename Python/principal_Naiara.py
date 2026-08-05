import numpy as np
from pathlib import Path
from scipy.signal import lfilter
from sinaisIEC60255_118 import signal_frequency, frequency_ramp, modulation
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from DSPEPS import Kalman_filter, downsample, estima_f_zc, BSplineInterp, FlatTopFilterBase, PolyphaseFilterBank, kf_trend_poly
from auxiliares import TVE, wrap_to_pi
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]
DADOS_DIR = BASE_DIR / "Aurora" / "dados_simulacao"
SAIDA_DIR = DADOS_DIR / "analise_saidas"
# ===================================================
# Basic Parameters for Signal Generation
# ===================================================

f0 = 60
Nppc = 256 # para melhorar os resultados de harmonicos mais altos colocar 512
Fs = f0 * Nppc
Ts = 1/Fs
Nc = 600
t = np.arange((Nc + 100) * Nppc)*Ts

# ===================================================
# Basic Parameters for IEC60255_118 Tests
# ===================================================

hmax = 50
hmag = 0.05

Fr = 60
SNR = 6000000

f1 = 57
Rf = 1
fa = 54.75
fm     = 0.1             # Hz  -> repetir o ensaio com fm = 5.0
kx, ka = 0.1, 0.0       # AM (Tabela 4, 1a linha)
#kx, ka = 0.0, 0.1        # PM (Tabela 4, 2a linha)

x, Xr, fr, ROCOFr = signal_frequency(f1, (Nc + 300)*Nppc, f0, Fs, Fr, hmax, hmag, SNR)
#x, Xr, fr, ROCOFr = frequency_ramp(Rf, (Nc + 300)*Nppc, f0, fa, Fs, Fr, hmax, hmag, SNR)
#x, Xr, fr, ROCOFr = modulation(fm, kx, ka, (Nc + 300)*Nppc, f0, Fs, Fr, hmag=hmag, hmax=hmax, SNR=SNR)

x_int = (x * 32768.0).astype(np.int32)    
saida_sapho = Path(__file__).resolve().parents[1] / "Aurora" / "dados_simulacao" / "sinal_teste.txt"
np.savetxt(saida_sapho, x_int, fmt='%d')
saida_teste = Path(__file__).resolve().parents[1] / "Python"/"Testes"/"Off_nominal"/"offnominal_57hz.txt"
np.savetxt(saida_teste, x_int, fmt='%d')

# Plotting the input signal, reference frequency, and reference ROCOF
# -------------------------------------------------------------------
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=("Input Signal", "Reference Frequency", "Reference ROCOF")
)

fig.add_trace(go.Scatter(x=t, y=x, name="Signal", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=fr, name="Frequency", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(x=t, y=ROCOFr, name="ROCOF", mode='lines'), row=3, col=1)

fig.update_yaxes(title_text="Amp", row=1, col=1)
fig.update_yaxes(title_text="f (Hz)", row=2, col=1)
fig.update_yaxes(title_text="ROCOF (Hz/s)", row=3, col=1)
fig.update_xaxes(title_text="Time (s)", row=3, col=1)

# 👇 aplica a TODOS os eixos
fig.update_xaxes(title_font=dict(size=24), tickfont=dict(size=24))
fig.update_yaxes(title_font=dict(size=24), tickfont=dict(size=24))

fig.update_layout(
    legend=dict(font=dict(size=24)),
    font=dict(size=24)   # fonte global
)
fig.update_annotations(font_size=26)
fig.update_traces(line=dict(width=4))

fig.show()

# ===================================================
# Frequency Estimation
# ===================================================

f_zc_m, zc_m_delay, f_zc, zc_delay, total_delay = estima_f_zc(x, 1/Fs, Nppc, plot_level=0)

#discard_samples = 2*int(np.ceil(total_delay / Nppc) * Nppc)
discard_kalman = 3 * Nppc
f_zc_m = f_zc_m[discard_kalman:]
f_zc = f_zc[discard_kalman:]
x = x[discard_kalman:]
fr = fr[discard_kalman:]
ROCOFr = ROCOFr[discard_kalman:]
Xr = Xr[:, discard_kalman:]

# Kalman filter to estimate the tendency of the frequency
q = 1e-3;   # ajuste fino
r = 1;      # se a senoide for forte, aumente

out = kf_trend_poly(f_zc_m, Ts, 1, q, r)
freq = out["b"].squeeze() #
freq_kalman, rocof_kalman = Kalman_filter(f_zc_m, Ts, 1, q, r)
freq_sapho = np.loadtxt(Path(__file__).resolve().parents[1] / "Aurora" / "dados_simulacao" / "saida_interp2.txt", dtype=float) / 1000000.0
freq_sapho = freq_sapho[(freq_sapho > 40.0) & (freq_sapho < 80.0)]
N_kalman = min(len(freq), len(freq_kalman), len(freq_sapho))
sample_kalman = np.arange(N_kalman)
freq_ref_plot = freq[:N_kalman]
freq_low_plot = freq_kalman[:N_kalman]
freq_sapho_plot = freq_sapho[:N_kalman]
diff_kalman_mhz = 1000.0 * (freq_low_plot - freq_ref_plot)
diff_sapho_mhz = 1000.0 * (freq_sapho_plot - freq_ref_plot)
max_diff_mhz = np.max(np.abs(diff_kalman_mhz)) if N_kalman > 0 else 0.0
max_diff_sapho_mhz = np.max(np.abs(diff_sapho_mhz)) if N_kalman > 0 else 0.0

fig_kalman, ax_kalman = plt.subplots(2, 1, sharex=True, figsize=(12, 7))

ax_kalman[0].plot(sample_kalman, freq_ref_plot, label="Kalman matricial", linewidth=2.0)
ax_kalman[0].plot(sample_kalman, freq_low_plot, label="Kalman baixo nivel", linestyle="--", linewidth=1.6)
ax_kalman[0].plot(sample_kalman, freq_sapho_plot, label="Kalman SAPHO", linestyle=":", linewidth=1.8)
ax_kalman[0].set_ylabel("Frequencia [Hz]")
ax_kalman[0].set_title("Comparacao das respostas do Kalman")
ax_kalman[0].grid(True, alpha=0.35)
ax_kalman[0].legend()

ax_kalman[1].plot(sample_kalman, diff_kalman_mhz, color="crimson", linewidth=1.4)
ax_kalman[1].plot(sample_kalman, diff_sapho_mhz, color="royalblue", linestyle=":", linewidth=1.4)
ax_kalman[1].axhline(0.0, color="black", linewidth=0.8, alpha=0.7)
ax_kalman[1].set_xlabel("Amostra")
ax_kalman[1].set_ylabel("Diferenca [mHz]")
ax_kalman[1].set_title(f"Baixo nivel max = {max_diff_mhz:.6g} mHz | SAPHO max = {max_diff_sapho_mhz:.6g} mHz")
ax_kalman[1].grid(True, alpha=0.35)
ax_kalman[1].legend(["Baixo nivel - matricial", "SAPHO - matricial"])

fig_kalman.tight_layout()
plt.show()

delay = np.zeros(total_delay+1)
delay[-1] = 1.0

x = lfilter(delay, [1.0], x)
freq = freq_kalman
# para alinhar o tempo de f_zc, fr, Xr e ROCOFr com o tempo de x, considerando o delay introduzido pelo filtro de média móvel
# ---------------------------------------------------------------------------------------------------------------------------
fr2 = np.concatenate((np.zeros(zc_delay), fr)) 
fr = np.concatenate((np.zeros(total_delay), fr)) 
Xr = np.hstack((np.zeros((hmax, total_delay)), Xr)) 
ROCOFr  = np.concatenate((np.zeros(total_delay), ROCOFr)) 

# Plotting the input signal, reference frequency, and reference ROCOF
# -------------------------------------------------------------------
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    subplot_titles=("Freq ZC", "Freq ZC Smoothed")
)

f_zc_sapho_raw = np.loadtxt(DADOS_DIR / "saida_interp1.txt", dtype=float) / 1_000_000.0
if len(f_zc_sapho_raw) > 1 and f_zc_sapho_raw[0] == 0.0:
    f_zc_sapho_raw = f_zc_sapho_raw[1:]
f_zc_sapho_raw = f_zc_sapho_raw[discard_kalman:]
f_zc_sapho = np.where((f_zc_sapho_raw >= 40.0) & (f_zc_sapho_raw <= 80.0), f_zc_sapho_raw, np.nan)

fig.add_trace(go.Scatter(y=f_zc, name="F ZC", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=f_zc_sapho, name="F ZC SAPHO", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=f_zc_sapho_raw, name="F ZC SAPHO bruto", mode='lines', visible='legendonly'), row=1, col=1)
fig.add_trace(go.Scatter(y=fr2, name="Reference", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=f_zc_m, name="F ZC Smoothed", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(y=fr, name="Reference", mode='lines'), row=2, col=1)


fig.update_yaxes(title_text="f (Hz)", row=1, col=1)
fig.update_yaxes(title_text="f (Hz)", row=2, col=1)
fig.update_yaxes(range=[50, 65], row=1, col=1)
fig.update_xaxes(title_text="Samples", row=2, col=1)

# 👇 aplica a TODOS os eixos
fig.update_xaxes(title_font=dict(size=24), tickfont=dict(size=24))
fig.update_yaxes(title_font=dict(size=24), tickfont=dict(size=24))

fig.update_layout(
    legend=dict(font=dict(size=24)),
    font=dict(size=24)   # fonte global
)
fig.update_annotations(font_size=26)
fig.update_traces(line=dict(width=4))

fig.show()

# Discarding the initial samples to align the time axes of all signals
# --------------------------------------------------------------------
discard_samples = 2*int(np.ceil(total_delay / Nppc) * Nppc)
print("Discarding the first", discard_samples)

freq = freq[discard_samples:discard_samples+(Nc+200)*Nppc]
x = x[discard_samples:discard_samples+(Nc+200)*Nppc]

fr = fr[discard_samples:discard_samples+(Nc+200)*Nppc]
Xr = Xr[:, discard_samples:discard_samples+(Nc+200)*Nppc]
ROCOFr = ROCOFr[discard_samples:discard_samples+(Nc+200)*Nppc]

# Plotting the reference frequency and the zero-crossing frequency estimation
# ---------------------------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(y=fr, name="Reference", mode='lines'))
fig.add_trace(go.Scatter(y=freq, name="Zero Crossing", mode='lines'))

fig.update_yaxes(title_text="Frequency (Hz)")
fig.update_xaxes(title_text="Time (s)")

fig.update_layout(
    xaxis_title_font=dict(size=24),
    yaxis_title_font=dict(size=24),
    xaxis_tickfont=dict(size=24),
    yaxis_tickfont=dict(size=24),
    legend=dict(font=dict(size=24))
)
fig.update_traces(line=dict(width=4))
fig.show()

# ===================================================
# BSpline Interpolation
# ===================================================
MBSP = 5

xi = BSplineInterp(x, f0, freq, MBSP, Fs, plot_level=0)

saida_interpolada_sapho = np.loadtxt(
    Path(__file__).resolve().parents[1] / "Aurora" / "dados_simulacao" / "saida_interp0.txt",
    dtype=float
) / 1000000.0

if len(saida_interpolada_sapho) > 1 and saida_interpolada_sapho[0] == 0.0:
    saida_interpolada_sapho = saida_interpolada_sapho[1:]
if len(saida_interpolada_sapho) > 1:
    saida_interpolada_sapho = saida_interpolada_sapho[:-1]

N_interp = min(len(x), len(xi), len(saida_interpolada_sapho))
sample_interp = np.arange(N_interp)
ref_interp = x[:N_interp]
xi_plot = xi[:N_interp]
sapho_plot = saida_interpolada_sapho[:N_interp]

erro_python_interp = xi_plot - ref_interp
erro_sapho_interp = sapho_plot - ref_interp

fig_bspline, ax_bspline = plt.subplots(2, 1, sharex=True, figsize=(12, 8))

ax_bspline[0].plot(sample_interp, ref_interp, label="Referencia", linewidth=2.0)
ax_bspline[0].plot(sample_interp, xi_plot, label="Interpolado Python", linestyle="--", linewidth=1.6)
ax_bspline[0].plot(sample_interp, sapho_plot, label="Interpolado SAPHO", linestyle=":", linewidth=1.8)
ax_bspline[0].set_ylabel("Amplitude")
ax_bspline[0].set_title("BSpline Interpolation")
ax_bspline[0].legend()
ax_bspline[0].grid(True, alpha=0.35)

ax_bspline[1].plot(sample_interp, erro_python_interp, label="Python - referencia", linewidth=1.4)
ax_bspline[1].plot(sample_interp, erro_sapho_interp, label="SAPHO - referencia", linestyle=":", linewidth=1.4)
ax_bspline[1].axhline(0.0, color="black", linewidth=0.8, alpha=0.7)
ax_bspline[1].set_xlabel("Samples")
ax_bspline[1].set_ylabel("Diferenca")
ax_bspline[1].legend()
ax_bspline[1].grid(True, alpha=0.35)

fig_bspline.tight_layout()
plt.show()


# ===================================================
# Polyphase FilterBank
# ===================================================
M = Fs//f0

h = FlatTopFilterBase(8*Nppc + 1) # Base Filter Definition - FlatTop 
fbDelay = (len(h))//(2*M)

# Cut the signals to the length of the polyphase filter bank output, which is equal to the number of samples that can be processed by the filter bank given its delay and decimation factor
# ------------------------------------------------------------------------------------------------------------------------------------------------------
xi = xi[:(Nc + fbDelay)*Nppc]
Xr = Xr[:,:(Nc + fbDelay)*Nppc]
freq = freq[:(Nc + fbDelay)*Nppc]
fr = fr[:(Nc + fbDelay)*Nppc]

X = PolyphaseFilterBank(h, M, xi)

ARQ_SAPHO_BANCO = DADOS_DIR / "saida_banco0.txt"
out_banco = np.atleast_1d(np.loadtxt(ARQ_SAPHO_BANCO, dtype=float))

#if len(out_banco) > 0 and out_banco[0] == 0.0:
 #   out_banco = out_banco[1:]

fasores_por_frame = hmax + 1
escalares_por_frame = 2 * fasores_por_frame
amostras_por_frame = 1 + escalares_por_frame

N_frames = len(out_banco) // amostras_por_frame
out_banco = out_banco[:N_frames * amostras_por_frame]

frames_banco = out_banco.reshape(N_frames, amostras_por_frame)

freq_sapho = frames_banco[1:, 0] / 1_000_000.0
fasores_banco = frames_banco[:, 1:]

real = fasores_banco[:, 0::2] / 1_000_000.0
imag = fasores_banco[:, 1::2] / 1_000_000.0

fasor_completo = (real + 1j * imag).T
X_sapho = fasor_completo[1:hmax+1, :]

X  = X[1:hmax+1,:]  ## Python 

# Downsampling the frequency, fr and Xr to match the decimation factor of the polyphase filter bank
# ---------------------------------------------------------------------------------------------
freq = downsample(freq,M)
Xr = downsample(Xr,M)
fr = downsample(fr,M)
freq_sapho_banco = np.loadtxt(DADOS_DIR / "saida_interp4.txt", dtype=float) / 1_000_000.0
freq_sapho_banco_valida = np.flatnonzero((freq_sapho_banco > 40.0) & (freq_sapho_banco < 80.0))
if len(freq_sapho_banco_valida) > 0:
    freq_sapho_banco = freq_sapho_banco[freq_sapho_banco_valida[0]:]
freq_sapho_banco = freq_sapho_banco[:(Nc + fbDelay)*Nppc]
freq_sapho_banco = downsample(freq_sapho_banco,M)  ## sapho 

# Compensating the delay introduced by the polyphase filter bank, which is equal to half the length of the filter divided by the decimation factor
# --------------------------------------------------------------------------------------------------------------------------------------
freq = np.concatenate((np.zeros(fbDelay), freq))
fr = np.concatenate((np.zeros(fbDelay), fr))
Xr = np.hstack((np.zeros((hmax, fbDelay)), Xr))
freq_sapho = np.concatenate((np.zeros(fbDelay), freq_sapho))  ## sapho
freq_sapho_interpolada = np.concatenate((np.zeros(fbDelay), freq_sapho_banco))  ## sapho
# Adjusting the length of the signals to match the number of samples of X
# --------------------------------------------------------------------------------------------------------------------------------------
freq = freq[:-fbDelay]
fr = fr[:-fbDelay]
Xr = Xr[:,:-fbDelay]
freq_sapho = freq_sapho[:-fbDelay]  ## sapho
freq_sapho_interpolada = freq_sapho_interpolada[:-fbDelay]  ## sapho


N_fasor = min(X.shape[1], X_sapho.shape[1], Xr.shape[1], len(freq), len(freq_sapho))
X = X[:, :N_fasor]
X_sapho = X_sapho[:, :N_fasor]
Xr = Xr[:, :N_fasor]
freq = freq[:N_fasor]
freq_sapho = freq_sapho[:N_fasor]
fr = fr[:N_fasor]
freq_sapho_interpolada = freq_sapho_interpolada[:N_fasor]  ## sapho

np.savetxt('freq_sapho_int4.txt',1_000_000 * freq_sapho_interpolada, fmt='%.6e')
np.savetxt('freq_sapho_decimada.txt', 1_000_000 * freq_sapho, fmt='%.6e')
np.savetxt('freq_python_decimada.txt', freq, fmt='%.6e')


AFT = 2*np.abs(X)   ##python
PFT = np.unwrap(np.angle(X))
AFT_sapho = 2*np.abs(X_sapho)  ## SAPHO
PFT_sapho = np.unwrap(np.angle(X_sapho))

# ===================================================
# Phase Correction python 
# ===================================================
delta_f = freq - f0 ## so incluir aqui a frequencia aqui que foi decimada no proc.cmm
correc = np.zeros(len(delta_f))

# Trapezoidal Integration (without error accumulation)
for nn in range(1, len(delta_f)):
    if(nn >= fbDelay+1):
        correc[nn] = correc[nn-1] + np.pi*(delta_f[nn] + delta_f[nn-1])*(M*Ts) 

correc = correc  - 1.4*np.pi/180 # para alinhar a fase do primeiro harmonico com a fase do referencial, considerando o atraso introduzido pelo filtro de média móvel e pelo filtro de interpolação
# Multiplies the correction by each harmonic (h = 1:50)
h = np.arange(1, 51).reshape(-1, 1)   # shape (50, 1)
correcH = h*correc

PFTc = np.unwrap((PFT) + np.unwrap(correcH)) 
Xc = AFT*np.exp(1j*PFTc)



# ===================================================
# Phase Correction sapho 
# ===================================================
delta_f_sapho_banco = freq_sapho - f0
correc_sapho_banco = np.zeros(len(delta_f_sapho_banco))

# Trapezoidal Integration (without error accumulation)
for nn in range(1, len(delta_f_sapho_banco)):
    if(nn >= fbDelay+1):
        correc_sapho_banco[nn] = correc_sapho_banco[nn-1] + np.pi*(delta_f_sapho_banco[nn] + delta_f_sapho_banco[nn-1])*(M*Ts) 

correc_sapho_banco = correc_sapho_banco  - 1.4*np.pi/180 # para alinhar a fase do primeiro harmonico com a fase do referencial, considerando o atraso introduzido pelo filtro de média móvel e pelo filtro de interpolação
# Multiplies the correction by each harmonic (h = 1:50)
h = np.arange(1, 51).reshape(-1, 1)   # shape (50, 1)
correcH_sapho = h*correc_sapho_banco

PFTc_sapho = np.unwrap((PFT_sapho) + np.unwrap(correcH_sapho)) 
Xc_sapho = AFT_sapho*np.exp(1j*PFTc_sapho)

# ===================================================
# Bank Output Comparison
# ===================================================
hh = 0
sample_fasor = np.arange(N_fasor)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Magnitude", "Imaginary"))

fig.add_trace(go.Scatter(x=sample_fasor, y=np.abs(X[hh, :]), name="Python", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(x=sample_fasor, y=np.abs(X_sapho[hh, :]), name="SAPHO", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(x=sample_fasor, y=np.imag(X[hh, :]), name="Python", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(x=sample_fasor, y=np.imag(X_sapho[hh, :]), name="SAPHO", mode='lines'), row=2, col=1)

fig.update_yaxes(title_text="Magnitude", row=1, col=1)
fig.update_yaxes(title_text="Imag", row=2, col=1)
fig.update_xaxes(title_text="Samples", row=2, col=1)

fig.update_layout(
    title_text=f"Banco Python x SAPHO - Harmonico {hh+1}",
    title_font=dict(size=22, family='Arial', color='black'),
    title_x=0.5,
    template='gridon'
)
# fig.show()

# ===================================================
# Performance Analysis
# ===================================================
Aref = np.abs(Xr)
Pref = np.unwrap(np.angle(Xr))

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Estimation", "Phase Estimation"))

fig.add_trace(go.Scatter(y=AFT[hh,:], name="Estimated Python", mode='lines+markers'), row=1, col=1)
fig.add_trace(go.Scatter(y=AFT_sapho[hh,:], name="Estimated SAPHO", mode='lines+markers'), row=1, col=1)
fig.add_trace(go.Scatter(y=Aref[hh,:], name="Reference", mode='lines+markers'), row=1, col=1)
fig.add_trace(go.Scatter(y=PFT[hh,:]*180/np.pi, name="Estimated Python", mode='lines+markers'), row=2, col=1)
fig.add_trace(go.Scatter(y=PFTc[hh,:]*180/np.pi, name="Corrected Python", mode='lines+markers'), row=2, col=1)
fig.add_trace(go.Scatter(y=PFTc_sapho[hh,:]*180/np.pi, name="Corrected SAPHO", mode='lines+markers'), row=2, col=1)
fig.add_trace(go.Scatter(y=Pref[hh,:]*180/np.pi, name="Reference", mode='lines+markers'), row=2, col=1)
fig.add_trace(go.Scatter(y=correcH[hh,:]*180/np.pi, name="Correction Python", mode='lines+markers'), row=2, col=1)
fig.add_trace(go.Scatter(y=correcH_sapho[hh,:]*180/np.pi, name="Correction SAPHO", mode='lines+markers'), row=2, col=1)

fig.update_yaxes(title_text="Amp", row=1, col=1)
fig.update_yaxes(title_text="Phase (°)", row=2, col=1)
fig.update_xaxes(title_text="Samples", row=2, col=1)

fig.update_layout(
    title_text=f"Magnitude and Phase Estimation for Harmonic - {hh+1}",
    title_font=dict(size=24, family='Arial', color='black'),  
    title_x=0.5,  
    template='gridon'
)
fig.show()


# Error Calculation
# ---------------------------------------------------
AFT   = AFT[:,2*fbDelay:]  
AFT_sapho = AFT_sapho[:,2*fbDelay:]
Aref  = Aref[:,2*fbDelay:] 
PFTc  = PFTc[:,2*fbDelay:] 
PFTc_sapho = PFTc_sapho[:,2*fbDelay:]
Pref  = Pref[:,2*fbDelay:] 
Xc    = Xc[:,2*fbDelay:] 
Xc_sapho = Xc_sapho[:,2*fbDelay:]
Xr    = Xr[:,2*fbDelay:] 

N_erro = min(
    Nc,
    AFT.shape[1],
    AFT_sapho.shape[1],
    Aref.shape[1],
    PFTc.shape[1],
    PFTc_sapho.shape[1],
    Pref.shape[1],
    Xc.shape[1],
    Xc_sapho.shape[1],
    Xr.shape[1],
)

AFT = AFT[:, :N_erro]
AFT_sapho = AFT_sapho[:, :N_erro]
Aref = Aref[:, :N_erro]
PFTc = PFTc[:, :N_erro]
PFTc_sapho = PFTc_sapho[:, :N_erro]
Pref = Pref[:, :N_erro]
Xc = Xc[:, :N_erro]
Xc_sapho = Xc_sapho[:, :N_erro]
Xr = Xr[:, :N_erro]
    
Aref_safe = np.where(np.abs(Aref) > 1e-12, Aref, np.nan)
ErroAFT = 100*np.abs(AFT - Aref)/Aref_safe            # Magnitude Error (%)
ErroAFT_sapho = 100*np.abs(AFT_sapho - Aref)/Aref_safe
ErroPFT = (wrap_to_pi(PFTc - Pref))*180/np.pi    # Phase Error (°)

ErroPFT_sapho = (wrap_to_pi(PFTc_sapho - Pref))*180/np.pi

valid_tve_ref = np.abs(Xr) > 1e-12
valid_tve_python = np.abs(Xc) > 1e-12

TVEFT = np.full(Xr.shape, np.nan, dtype=float)
TVEFT_sapho = np.full(Xr.shape, np.nan, dtype=float)
TVEFT_sapho_python = np.full(Xc.shape, np.nan, dtype=float)

TVEFT[valid_tve_ref] = TVE(Xc[valid_tve_ref], Xr[valid_tve_ref])
TVEFT_sapho[valid_tve_ref] = TVE(Xc_sapho[valid_tve_ref], Xr[valid_tve_ref])
TVEFT_sapho_python[valid_tve_python] = TVE(Xc_sapho[valid_tve_python], Xc[valid_tve_python])

ErroAFT = ErroAFT[:,:Nc]
ErroAFT_sapho = ErroAFT_sapho[:,:Nc]
ErroPFT = ErroPFT[:,:Nc]
ErroPFT_sapho = ErroPFT_sapho[:,:Nc]
TVEFT = TVEFT[:,:Nc] 
TVEFT_sapho = TVEFT_sapho[:,:Nc]
TVEFT_sapho_python = TVEFT_sapho_python[:,:Nc]

fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Error", "Phase Error", "Total Vector Error"))

fig.add_trace(go.Scatter(y=ErroAFT[hh,:], name="Magnitude Error Python (%)", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=ErroAFT_sapho[hh,:], name="Magnitude Error SAPHO (%)", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=ErroPFT[hh,:], name="Phase Error (°)", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(y=ErroPFT_sapho[hh,:], name="Phase Error SAPHO (deg)", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(y=TVEFT[hh,:], name="TVE Python x referencia (%)", mode='lines'), row=3, col=1)
fig.add_trace(go.Scatter(y=TVEFT_sapho[hh,:], name="TVE SAPHO x referencia (%)", mode='lines'), row=3, col=1)
fig.add_trace(go.Scatter(y=np.ones(len(TVEFT[hh,:])),   name="Limit IEC/IEEE 60255-118-1", mode='lines',line=dict(color='red', dash='dash')), row=3, col=1)

fig.update_xaxes(title_text="Samples", row=3, col=1)

fig.update_layout(
    title_text=f"Errors for Harmonic - {hh+1}",
    title_font=dict(size=24, family='Arial', color='black'),  
    title_x=0.5,  
    template='gridon'
)
fig.show()


# Min, Max and Average Errors
# ---------------------------------------------------
ErroAFTmin = np.min(ErroAFT, axis=1)
ErroAFTmax = np.max(ErroAFT, axis=1)
ErroAFTavg = np.mean(ErroAFT, axis=1)
ErroAFT_saphomin = np.min(ErroAFT_sapho, axis=1)
ErroAFT_saphomax = np.max(ErroAFT_sapho, axis=1)
ErroAFT_saphoavg = np.mean(ErroAFT_sapho, axis=1)

ErroPFTmin = np.min(ErroPFT, axis=1)
ErroPFTmax = np.max(ErroPFT, axis=1)
ErroPFTavg = np.mean(ErroPFT, axis=1)
ErroPFT_saphomin = np.min(ErroPFT_sapho, axis=1)
ErroPFT_saphomax = np.max(ErroPFT_sapho, axis=1)
ErroPFT_saphoavg = np.mean(ErroPFT_sapho, axis=1)

TVEFTmin = np.min(TVEFT, axis=1)
TVEFTmax = np.max(TVEFT, axis=1)
TVEFTavg = np.mean(TVEFT, axis=1)
TVEFT_saphomin = np.min(TVEFT_sapho, axis=1)
TVEFT_saphomax = np.max(TVEFT_sapho, axis=1)
TVEFT_saphoavg = np.mean(TVEFT_sapho, axis=1)
TVEFT_sapho_pythonavg = np.mean(TVEFT_sapho_python, axis=1)

indh = np.arange(hmax)+1

TVElim = 1 # Limit IEC/IEEE 60255-118-1 for TVE (%)
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Error", "Phase Error", "Total Vector Error (TVE)"))

fig.add_trace(go.Scatter(x=indh, y=ErroAFTavg, name="Media Python", legendgroup="media_python", showlegend=True, mode='lines+markers', marker_symbol='circle', line=dict(color='royalblue')), row=1, col=1)
fig.add_trace(go.Scatter(x=indh, y=ErroAFT_saphoavg, name="Media SAPHO", legendgroup="media_sapho", showlegend=True, mode='lines+markers', marker_symbol='diamond', line=dict(color='darkorange')), row=1, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([ErroAFTavg, ErroAFTmax[::-1]]), fill='toself', fillcolor='rgba(65,105,225,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximo Python', legendgroup="maximo_python", showlegend=True), row=1, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([ErroAFT_saphoavg, ErroAFT_saphomax[::-1]]), fill='toself', fillcolor='rgba(255,140,0,0.18)', line=dict(color='rgba(255,255,255,0)'), name='Maximo SAPHO', legendgroup="maximo_sapho", showlegend=True), row=1, col=1)
fig.add_trace(go.Scatter(x=indh, y=ErroPFTavg, name="Media Python", legendgroup="media_python", showlegend=False, mode='lines+markers', marker_symbol='circle', line=dict(color='royalblue')), row=2, col=1)
fig.add_trace(go.Scatter(x=indh, y=ErroPFT_saphoavg, name="Media SAPHO", legendgroup="media_sapho", showlegend=False, mode='lines+markers', marker_symbol='diamond', line=dict(color='darkorange')), row=2, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([ErroPFTavg, ErroPFTmax[::-1]]), fill='toself', fillcolor='rgba(65,105,225,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximo Python', legendgroup="maximo_python", showlegend=False), row=2, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([ErroPFT_saphoavg, ErroPFT_saphomax[::-1]]), fill='toself', fillcolor='rgba(255,140,0,0.18)', line=dict(color='rgba(255,255,255,0)'), name='Maximo SAPHO', legendgroup="maximo_sapho", showlegend=False), row=2, col=1)
fig.add_trace(go.Scatter(x=indh, y=TVEFTavg, name="Media Python", legendgroup="media_python", showlegend=False, mode='lines+markers', marker_symbol='circle', line=dict(color='royalblue')), row=3, col=1)
fig.add_trace(go.Scatter(x=indh, y=TVEFT_saphoavg, name="Media SAPHO", legendgroup="media_sapho", showlegend=False, mode='lines+markers', marker_symbol='diamond', line=dict(color='darkorange')), row=3, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([TVEFTavg, TVEFTmax[::-1]]), fill='toself', fillcolor='rgba(65,105,225,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximo Python', legendgroup="maximo_python", showlegend=False), row=3, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([TVEFT_saphoavg, TVEFT_saphomax[::-1]]), fill='toself', fillcolor='rgba(255,140,0,0.18)', line=dict(color='rgba(255,255,255,0)'), name='Maximo SAPHO', legendgroup="maximo_sapho", showlegend=False), row=3, col=1)
fig.add_trace(go.Scatter(x=indh, y=TVElim*np.ones(len(TVEFTavg)), name="Limite IEC/IEEE 60255-118-1", mode='lines', line=dict(color='black', dash='dot')), row=3, col=1)

fig.update_yaxes(title_text="Error (%)", row=1, col=1)
fig.update_yaxes(title_text="Error (°)", row=2, col=1)
fig.update_yaxes(title_text="TVE (%)", row=3, col=1)
fig.update_xaxes(title_text="Harmonic", row=3, col=1)

fig.update_layout(
    title_text=f"Errors for Harmonics up to {hmax}",
    title_font=dict(size=20, family='Arial', color='black'),  
    title_x=0.5,  
    title_y = 0.95,
    template='gridon'
)

fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.09,
    xanchor="right",
    x=1
))

fig.show()


# ===================================================
# TVE
# ===================================================
TVEFT_plot = np.where(np.isfinite(TVEFT), TVEFT, np.nan)
TVEFT_sapho_plot = np.where(np.isfinite(TVEFT_sapho), TVEFT_sapho, np.nan)

fig = go.Figure()
fig.add_trace(go.Scatter(y=TVEFT_plot[hh, :], name="Python", mode='lines'))
fig.add_trace(go.Scatter(y=TVEFT_sapho_plot[hh, :], name="SAPHO", mode='lines'))
fig.update_yaxes(title_text="TVE (%)")
fig.update_xaxes(title_text="Samples")
fig.update_layout(
    title_text=f"TVE - Harmonico {hh+1}",
    title_font=dict(size=24, family='Arial', color='black'),
    title_x=0.5,
    template='gridon'
)
# fig.show()

TVEFTavg = np.full(hmax, np.nan, dtype=float)
TVEFT_saphoavg = np.full(hmax, np.nan, dtype=float)

for ii in range(hmax):
    tve_python_valid = TVEFT_plot[ii, np.isfinite(TVEFT_plot[ii, :])]
    tve_sapho_valid = TVEFT_sapho_plot[ii, np.isfinite(TVEFT_sapho_plot[ii, :])]

    if len(tve_python_valid) > 0:
        TVEFTavg[ii] = np.mean(tve_python_valid)

    if len(tve_sapho_valid) > 0:
        TVEFT_saphoavg[ii] = np.mean(tve_sapho_valid)

fig = go.Figure()
fig.add_trace(go.Scatter(x=indh, y=TVEFTavg, name="Python", mode='lines+markers'))
fig.add_trace(go.Scatter(x=indh, y=TVEFT_saphoavg, name="SAPHO", mode='lines+markers'))
fig.update_yaxes(title_text="TVE medio (%)")
fig.update_xaxes(title_text="Harmonic")
fig.update_layout(
    title_text=f"TVE medio por harmonico ate {hmax}",
    title_font=dict(size=20, family='Arial', color='black'),
    title_x=0.5,
    template='gridon'
)
# fig.show()
