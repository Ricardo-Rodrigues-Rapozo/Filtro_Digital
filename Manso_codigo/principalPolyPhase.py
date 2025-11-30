import numpy as np
from sinaisIEC60255_118 import signal_frequency, frequency_ramp
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from DSPEPS import downsample, estima_f_zc, BSplineInterp, FlatTopFilterBase, PolyphaseFilterBank 
from auxiliares import TVE

# ===================================================
# Basic Parameters
# ===================================================

f0 = 60
Nppc = 256
Fs = f0 * Nppc
Ts = 1/Fs
Nc = 600
t = np.arange((Nc + 100) * Nppc)*Ts

# ===================================================
# Test Signal
# ===================================================

f1 = 55
hmax = 50
hmag = 0.1

Rf = 1
fa = 54.75

Fr = 60
SNR = 600000000000

# x, Xr, fr, ROCOFr = signal_frequency(f1, (Nc + 100) * Nppc, f0, Fs, Fr, hmax, hmag, SNR)
x, Xr, fr, ROCOFr = frequency_ramp(Rf, (Nc + 100) * Nppc, f0, fa, Fs, Fr, hmax, hmag, SNR)

fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Input Signal", "Reference Frequency", "Reference ROCOF"))

fig.add_trace(go.Scatter(x = t, y=x, name="Signal", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(x = t, y=fr, name="Frequency", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(x = t, y=ROCOFr, name="ROCOF", mode='lines'), row=3, col=1)
fig.update_yaxes(title_text="Amp", row=1, col=1)
fig.update_yaxes(title_text="f (Hz)", row=2, col=1)
fig.update_yaxes(title_text="ROCOF (Hz/s)", row=3, col=1)
fig.update_xaxes(title_text="Time (s)", row=3, col=1)

fig.update_layout(
    title_text="Test Signal",
    title_font=dict(size=24, family='Arial', color='black'), 
    title_x=0.5,  
    template='gridon'
)

fig.show()

# ===================================================
# Frequency Estimation
# ===================================================

f_zc, f_zc_m = estima_f_zc(x, 1/Fs, Nppc)

# Discard for eliminate the transient of frequency estimation
Ncd = 16
start = Ncd * Nppc    

f_zc   = f_zc[start:]
f_zc_m = f_zc_m[start:]
x      = x[start:]
Xr     = Xr[:,start:]   
fr     = fr[start:]
ROCOFr = ROCOFr[start:]

fig = go.Figure()
fig.add_trace(go.Scatter(x = t, y=fr, name="Reference", mode='lines'))
fig.add_trace(go.Scatter(x = t, y=f_zc, name="Zero Crossing", mode='lines'))
fig.add_trace(go.Scatter(x = t, y=f_zc_m, name="Zero Crossing Smooth", mode='lines'))

fig.update_yaxes(title_text="Frequency (Hz)")
fig.update_xaxes(title_text="Time (s)")

fig.update_layout(
    autosize=True,
    title_text="Frequency Estimation",
    title_font=dict(size=24, family='Arial', color='black'),  
    title_x=0.5,  
    template='gridon'
)
fig.show()

# ===================================================
# BSpline Interpolation
# ===================================================
MBSP = 5
freq = f_zc_m

xi = BSplineInterp(x, f0, freq, MBSP, Fs)

# Vector Dimension Adjustment
# ---------------------------------------------------
NcdFT = 13 # Number of cycles needed to discar the FT Filterbank transient

xi = xi[0:(Nc+NcdFT)*Nppc]
freq   = freq[0:(Nc+NcdFT)*Nppc]
Xr     = Xr[:,0:(Nc+NcdFT)*Nppc]   
fr     = fr[0:(Nc+NcdFT)*Nppc]
ROCOFr = ROCOFr[0:(Nc+NcdFT)*Nppc]

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
# FlatTop FilterBank
# ===================================================
h = FlatTopFilterBase(13*Nppc+1) 
M = Fs//f0

X = PolyphaseFilterBank(h, M, xi)

X  = X[1:hmax+1,:]
AFT = 2*np.abs(X)
PFT = np.unwrap(np.angle(X))

Xr = np.hstack((np.zeros((hmax, len(h)//2)), Xr)) # Reference delay to compensate FilterBank delay
Xr = Xr[:,0:(Nc+NcdFT)*Nppc] 

# ===================================================
# Phase Correction
# ===================================================
delta_f = freq - f0
delta_f = np.concatenate((np.zeros(len(h)//2), delta_f)) # Frequency delay to compensate FilterBank delay
delta_f = delta_f[0:(Nc+NcdFT)*Nppc]
correc = np.zeros(len(delta_f))

# Trapezoidal Integration (without error accumulation)
for nn in range(1, len(delta_f)):
    if(nn >= ((13*Nppc+1)//2)+1):
        correc[nn] = correc[nn-1] + np.pi*(delta_f[nn] + delta_f[nn-1])*Ts

correc = downsample(correc, M)
# Multiplies the correction by each harmonic (h = 1:50)
h = np.arange(1, 51).reshape(-1, 1)   # shape (50, 1)
correcH = h*correc

PFTc = (PFT) + (correcH)
Xc = AFT*np.exp(1j*PFTc)

# ===================================================
# Performance Analysis
# ===================================================
Xr = downsample(Xr,M)
Aref = np.abs(Xr)
Pref = np.unwrap(np.angle(Xr))

hh = 1

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Estimation", "Phase Estimation"))

fig.add_trace(go.Scatter(y=AFT[hh,:], name="Estimated", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=Aref[hh,:], name="Reference", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=PFTc[hh,:]*180/np.pi, name="Estimated", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(y=Pref[hh,:]*180/np.pi, name="Reference", mode='lines'), row=2, col=1)

fig.update_yaxes(title_text="Amp", row=1, col=1)
fig.update_yaxes(title_text="Phase (°)", row=2, col=1)
fig.update_xaxes(title_text="Samples", row=2, col=1)

fig.update_layout(
    title_text=f"Magnitude and Phase Estimation for Harmonic - {hh}",
    title_font=dict(size=24, family='Arial', color='black'),  
    title_x=0.5,  
    template='gridon'
)
fig.show()

# Error Calculation
# ---------------------------------------------------
AFT   = AFT[:,NcdFT:]  
Aref  = Aref[:,NcdFT:] 
PFTc  = PFTc[:,NcdFT:] 
Pref  = Pref[:,NcdFT:] 
Xc    = Xc[:,NcdFT:] 
Xr    = Xr[:,NcdFT:] 

ErroAFT = 100*np.abs(AFT - Aref)/Aref      # Magnitude Error (%)
ErroPFT = np.abs(PFTc - Pref)*180/np.pi   # Phase Error (°)
TVEFT = TVE(Xc,Xr)                         # TVE (%)                       

fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Error", "Phase Error", "Total Vector Error"))

fig.add_trace(go.Scatter(y=ErroAFT[hh,:], name="Magnitude Error (%)", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=ErroPFT[hh,:], name="Phase Error (°)", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(y=TVEFT[hh,:],   name="TVE (%)", mode='lines'), row=3, col=1)
fig.add_trace(go.Scatter(y=np.ones(len(TVEFT[hh,:])),   name="Limit IEC/IEEE 60255-118-1", mode='lines',line=dict(color='red', dash='dash')), row=3, col=1)

fig.update_xaxes(title_text="Samples", row=3, col=1)

fig.update_layout(
    title_text=f"Errors for Harmonic - {hh}",
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

fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Error", "Phase Error", "Total Vector Error (TVE)"))

fig.add_trace(go.Scatter(x=indh,y=ErroAFTavg, name="Average", mode='lines+markers', marker_symbol='circle', line=dict(color='royalblue')), row=1, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([ErroAFTavg, ErroAFTmax[::-1]]), fill='toself', fillcolor='rgba(65,105,225,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximum'), row=1, col=1)
fig.add_trace(go.Scatter(x=indh, y=ErroPFTavg, name="Average", mode='lines+markers', marker_symbol='circle', line=dict(color='seagreen')), row=2, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([ErroPFTavg, ErroPFTmax[::-1]]), fill='toself', fillcolor='rgba(60,179,113,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximum'), row=2, col=1)
fig.add_trace(go.Scatter(x=indh, y=TVEFTavg,   name="Average", mode='lines+markers', marker_symbol='circle', line=dict(color='crimson')), row=3, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([TVEFTavg, TVEFTmax[::-1]]), fill='toself', fillcolor='rgba(220,20,60,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximum'), row=3, col=1)
fig.add_trace(go.Scatter(x=indh, y=np.ones(len(TVEFTavg)),   name="Limit IEC/IEEE 60255-118-1", mode='lines',line=dict(color='black', dash='dot')), row=3, col=1)

fig.update_yaxes(title_text="Error (%)", row=1, col=1)
fig.update_yaxes(title_text="Error (°)", row=2, col=1)
fig.update_yaxes(title_text="TVE (%)", row=3, col=1)
fig.update_xaxes(title_text="Harmonic", row=3, col=1)

fig.update_layout(
    title_text=f"Errors for Harmonic - {hh}",
    title_font=dict(size=24, family='Arial', color='black'),  
    title_x=0.5,  
    template='gridon'
)
fig.show()