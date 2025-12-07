import numpy as np
from filtros_polifasicos_ref_Manso.sinaisIEC60255_118 import signal_frequency
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import string

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

x = list(range(1, 31))

# ===================================================
# Base Filter
# ===================================================
N = 2*Nppc
h = np.ones(30)
M = 5
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
    for mm in range(M):
        for kk in range((len(h)//M) -1, 0, -1):
            E[mm,kk] = E[mm,kk-1]        
        E[mm,0] = buffer[mm]
