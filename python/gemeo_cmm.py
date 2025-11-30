import numpy as np
from sinaisIEC60255_118 import signal_frequency
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def downsample(signal, factor):
    signal = np.asarray(signal)
    downsampled = signal[..., ::factor]  # preserva todas as dimensões anteriores
    return downsampled

# ===================================================
# Basic Parameters
# ===================================================

f0 = 60
Nppc = 256
Fs = f0 * Nppc
Ts = 1/Fs
Nc = 600
t = np.arange(Nc*Nppc)*Ts

# ===================================================
# Test Signal
# ===================================================

f1 = 57
hmax = 50
hmag = 0.15

Fr = 60
SNR = 600000000000

x, Xr, fr, ROCOFr = signal_frequency(f1, Nc*Nppc, f0, Fs, Fr, hmax, hmag, SNR)

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

# x = np.arange(100)

# N = 10
# h = (1/N)*np.ones(N)
# M = 5

# ===================================================
# Base Filter
# ===================================================
N = 2*Nppc
h = (1/N)*np.ones(N)

M = Fs//f0

Nf = int(np.ceil(len(h)/M))
Ehh = np.zeros((M, Nf))

for kk in range(M):
    hh = np.array(h[kk::M])          # transforma em numpy array
    hh_padded = np.pad(hh, (0, Nf - len(hh)), 'constant')  # completa com zeros à direita
    Ehh[kk, :] = hh_padded

# ===================================================
# Polyphase Implementation
# ===================================================
buffer= np.zeros(M)
E = np.zeros((M,len(h)//M))
E0 = np.zeros(M)
v = np.zeros((M,len(x)//M), dtype=complex)
jj = 0

for nn in range(len(x)):
    for kk in range(M-1):
        buffer[M-1-kk] = buffer[M-2-kk] 
    buffer[0] = x[nn]
    
    if((nn % M) == 0):
        for mm in range(M):
            for kk in range((len(h)//M) -1, 0, -1):
                E[mm,kk] = E[mm,kk-1]        
            E[mm,0] = buffer[mm]
            E0[mm] =  np.dot(Ehh[mm,:],E[mm,:])
        
        vv = M*np.fft.ifft(E0)
        v[:,jj] = vv
        jj += 1

Xr = downsample(Xr, M)
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Fundamental", "5th Haromonic", "13th Harmonic"))

fig.add_trace(go.Scatter(y=np.abs(Xr[0,:]), name="Ref Fundamental", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=2*np.abs(v[1,:]), name="Est Fundamental", mode='lines'), row=1, col=1)

fig.add_trace(go.Scatter(y=np.abs(Xr[1,:]), name="Ref 5th Harmonic", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(y=2*np.abs(v[2,:]), name="Est 5th Harmonic", mode='lines'), row=2, col=1)

fig.add_trace(go.Scatter(y=np.abs(Xr[2,:]), name="Ref 13th Harmonic", mode='lines'), row=3, col=1)
fig.add_trace(go.Scatter(y=2*np.abs(v[3,:]), name="Ref 13th Harmonic", mode='lines'), row=3, col=1)

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