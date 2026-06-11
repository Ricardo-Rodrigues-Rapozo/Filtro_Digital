import numpy as np
from scipy.signal import lfilter
from sinaisIEC60255_118 import signal_frequency, frequency_ramp, modulation
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from DSPEPS import Kalman_filter, downsample, estima_f_zc, BSplineInterp, FlatTopFilterBase, PolyphaseFilterBank, kf_trend_poly
from auxiliares import TVE, wrap_to_pi
import matplotlib.pyplot as plt

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

f1 = 61
Rf = 1
fa = 54.75

x, Xr, fr, ROCOFr = signal_frequency(f1, (Nc + 300)*Nppc, f0, Fs, Fr, hmax, hmag, SNR)
# x, Xr, fr, ROCOFr = frequency_ramp(Rf, (Nc + 300)*Nppc, f0, fa, Fs, Fr, hmax, hmag, SNR)

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

discard_samples = 2*int(np.ceil(total_delay / Nppc) * Nppc)
f_zc_m = f_zc_m[discard_samples:]
f_zc = f_zc[discard_samples:]
x = x[discard_samples:]
fr = fr[discard_samples:]
ROCOFr = ROCOFr[discard_samples:]
Xr = Xr[:, discard_samples:]

# Kalman filter to estimate the tendency of the frequency
q = 1e-3;   # ajuste fino
r = 1;      # se a senoide for forte, aumente

out = kf_trend_poly(f_zc_m, Ts, 1, q, r)
freq = out["b"].squeeze() #
freq_kalman, rocof_kalman = Kalman_filter(f_zc_m, Ts, 1, q, r)

N_kalman = min(len(freq), len(freq_kalman))
sample_kalman = np.arange(N_kalman)
freq_ref_plot = freq[:N_kalman]
freq_low_plot = freq_kalman[:N_kalman]
diff_kalman_mhz = 1000.0 * (freq_low_plot - freq_ref_plot)
max_diff_mhz = np.max(np.abs(diff_kalman_mhz)) if N_kalman > 0 else 0.0

fig_kalman, ax_kalman = plt.subplots(2, 1, sharex=True, figsize=(12, 7))

ax_kalman[0].plot(sample_kalman, freq_ref_plot, label="Kalman matricial", linewidth=2.0)
ax_kalman[0].plot(sample_kalman, freq_low_plot, label="Kalman baixo nivel", linestyle="--", linewidth=1.6)
ax_kalman[0].set_ylabel("Frequencia [Hz]")
ax_kalman[0].set_title("Comparacao das respostas do Kalman")
ax_kalman[0].grid(True, alpha=0.35)
ax_kalman[0].legend()

ax_kalman[1].plot(sample_kalman, diff_kalman_mhz, color="crimson", linewidth=1.4)
ax_kalman[1].axhline(0.0, color="black", linewidth=0.8, alpha=0.7)
ax_kalman[1].set_xlabel("Amostra")
ax_kalman[1].set_ylabel("Diferenca [mHz]")
ax_kalman[1].set_title(f"Baixo nivel - matricial | max = {max_diff_mhz:.6g} mHz")
ax_kalman[1].grid(True, alpha=0.35)

fig_kalman.tight_layout()
plt.show()

delay = np.zeros(total_delay+1)
delay[-1] = 1.0

x = lfilter(delay, [1.0], x)

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

fig.add_trace(go.Scatter(y=f_zc, name="F ZC", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=fr2, name="Reference", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=f_zc_m, name="F ZC Smoothed", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(y=fr, name="Reference", mode='lines'), row=2, col=1)


fig.update_yaxes(title_text="f (Hz)", row=1, col=1)
fig.update_yaxes(title_text="f (Hz)", row=2, col=1)
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

fig = go.Figure()
fig.add_trace(go.Scatter(y=x, name="Input Signal", mode='lines+markers', marker_symbol='x', marker_size=8,))
fig.add_trace(go.Scatter(y=xi, name="Interpolated Signal", mode='lines+markers', marker_symbol='x', marker_size=8,))

fig.update_xaxes(title_text="Samples")
fig.update_yaxes(title_text="Amp")

fig.update_layout(
    autosize=True,
    title_text="BSpline Interpolation",
    title_font=dict(size=24, family='Arial', color='black'),  
    title_x=0.5,  
    template='gridon'
)
fig.show()

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

X  = X[1:hmax+1,:]
AFT = 2*np.abs(X)
PFT = np.unwrap(np.angle(X))

# Downsampling the frequency, fr and Xr to match the decimation factor of the polyphase filter bank
# ---------------------------------------------------------------------------------------------
freq = downsample(freq,M)
Xr = downsample(Xr,M)
fr = downsample(fr,M)

# Compensating the delay introduced by the polyphase filter bank, which is equal to half the length of the filter divided by the decimation factor
# --------------------------------------------------------------------------------------------------------------------------------------
freq = np.concatenate((np.zeros(fbDelay), freq))
fr = np.concatenate((np.zeros(fbDelay), fr))
Xr = np.hstack((np.zeros((hmax, fbDelay)), Xr))

# Adjusting the length of the signals to match the number of samples of X
# --------------------------------------------------------------------------------------------------------------------------------------
freq = freq[:-fbDelay]
fr = fr[:-fbDelay]
Xr = Xr[:,:-fbDelay]

# ===================================================
# Phase Correction
# ===================================================
delta_f = freq - f0
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
# Performance Analysis
# ===================================================
Aref = np.abs(Xr)
Pref = np.unwrap(np.angle(Xr))

hh = 0

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Estimation", "Phase Estimation"))

fig.add_trace(go.Scatter(y=AFT[hh,:], name="Estimated", mode='lines+markers'), row=1, col=1)
fig.add_trace(go.Scatter(y=Aref[hh,:], name="Reference", mode='lines+markers'), row=1, col=1)
fig.add_trace(go.Scatter(y=PFT[hh,:]*180/np.pi, name="Estimated", mode='lines+markers'), row=2, col=1)
fig.add_trace(go.Scatter(y=PFTc[hh,:]*180/np.pi, name="Corrected", mode='lines+markers'), row=2, col=1)
fig.add_trace(go.Scatter(y=Pref[hh,:]*180/np.pi, name="Reference", mode='lines+markers'), row=2, col=1)
fig.add_trace(go.Scatter(y=correcH[hh,:]*180/np.pi, name="Correction", mode='lines+markers'), row=2, col=1)

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
AFT   = AFT[:,10*fbDelay:]  
Aref  = Aref[:,10*fbDelay:] 
PFTc  = PFTc[:,10*fbDelay:] 
Pref  = Pref[:,10*fbDelay:] 
Xc    = Xc[:,10*fbDelay:] 
Xr    = Xr[:,10*fbDelay:] 
    
ErroAFT = 100*np.abs(AFT - Aref)/Aref            # Magnitude Error (%)
ErroPFT = (wrap_to_pi(PFTc - Pref))*180/np.pi    # Phase Error (°)

TVEFT = TVE(Xc,Xr)                       # TVE (%)                       

ErroAFT = ErroAFT[:,:Nc]
ErroPFT = ErroPFT[:,:Nc]
TVEFT = TVEFT[:,:Nc] 

fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Error", "Phase Error", "Total Vector Error"))

fig.add_trace(go.Scatter(y=ErroAFT[hh,:], name="Magnitude Error (%)", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=ErroPFT[hh,:], name="Phase Error (°)", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(y=TVEFT[hh,:],   name="TVE (%)", mode='lines'), row=3, col=1)
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

ErroPFTmin = np.min(ErroPFT, axis=1)
ErroPFTmax = np.max(ErroPFT, axis=1)
ErroPFTavg = np.mean(ErroPFT, axis=1)

TVEFTmin = np.min(TVEFT, axis=1)
TVEFTmax = np.max(TVEFT, axis=1)
TVEFTavg = np.mean(TVEFT, axis=1)

indh = np.arange(hmax)+1

TVElim = 1 # Limit IEC/IEEE 60255-118-1 for TVE (%)
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Error", "Phase Error", "Total Vector Error (TVE)"))

fig.add_trace(go.Scatter(x=indh,y=ErroAFTavg, name="Average", mode='lines+markers', marker_symbol='circle', line=dict(color='royalblue')), row=1, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([ErroAFTavg, ErroAFTmax[::-1]]), fill='toself', fillcolor='rgba(65,105,225,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximum'), row=1, col=1)
fig.add_trace(go.Scatter(x=indh, y=ErroPFTavg, name="Average", mode='lines+markers', marker_symbol='circle', line=dict(color='seagreen')), row=2, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([ErroPFTavg, ErroPFTmax[::-1]]), fill='toself', fillcolor='rgba(60,179,113,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximum'), row=2, col=1)
fig.add_trace(go.Scatter(x=indh, y=TVEFTavg,   name="Average", mode='lines+markers', marker_symbol='circle', line=dict(color='crimson')), row=3, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([TVEFTavg, TVEFTmax[::-1]]), fill='toself', fillcolor='rgba(220,20,60,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximum'), row=3, col=1)
fig.add_trace(go.Scatter(x=indh, y=TVElim*np.ones(len(TVEFTavg)),   name="Limit IEC/IEEE 60255-118-1", mode='lines',line=dict(color='black', dash='dot')), row=3, col=1)

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
