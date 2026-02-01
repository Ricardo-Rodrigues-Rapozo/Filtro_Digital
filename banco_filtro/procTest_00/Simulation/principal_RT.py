import numpy as np
from sinaisIEC60255_118 import signal_frequency
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import firls, lfilter
from auxiliares import TVE

# ========================================================
# Basic Parameters
# ========================================================

f0 = 60
Nppc = 256
Fs = f0 * Nppc
Ts = 1/Fs
Nc = 100
t = np.arange((Nc + 100) * Nppc)*Ts

# ========================================================
# Initialization and variables declaration
# ========================================================

# Frequency Estimation
# --------------------------------------------------------
    
N = 2 * Nppc      # filter order
Fpass = 70         
Fstop = 120       
Wpass = 1
Wstop = 1

num_pre_ZC = firls(N+1, [0, Fpass, Fstop, Fs / 2], [1, 1, 0, 0], weight=[Wpass, Wstop], fs=Fs)

x_buff_ZC = np.zeros(len(num_pre_ZC))
buff_pt_ZC = 0

va = 0.0
Tsc = 1 / 60.0  
T1 = 0.0
cnt = 0
f_zc = f0

# B-Spline Interpolation
#---------------------------------------------------------

MBSP = 5
s = np.sqrt(3) - 2

num_pre_BSP = -6*(s**np.arange(MBSP+1, 0, -1))  
den_pre_BSP = np.array([1, -s])

x_buff_BSP = np.zeros(len(num_pre_BSP))
y_buff_BSP = np.zeros(len(den_pre_BSP)-1)

x_buff_pt_BSP = 0
y_buff_pt_BSP = 0

buffer_farrow = np.zeros(4)
alfa = 0.0

# Base Filter
#---------------------------------------------------------

c5 = [1.0005967, 1.9991048, 1.9097925, 1.4448987, 0.66403725, 0.1304229]

N = 13*(Fs//f0)+1
n = np.arange(-(N - 1) / 2, 1 + (N - 1) / 2, 1)

wM = np.zeros(N)
for m in range(len(c5)):
    wM = wM + c5[m] * np.cos(m * (2 * np.pi / N) * n)

wM = wM / np.sum(wM)


# Polyphase Filter
#---------------------------------------------------------
h = wM

M = Fs//f0

Nf = int(np.ceil(len(h)/M))
E = np.zeros((M, Nf))

for kk in range(M):
    hh = np.array(h[kk::M])          # transforma em numpy array
    hh_padded = np.pad(hh, (0, Nf - len(hh)), 'constant')  # completa com zeros à direita
    E[kk, :] = hh_padded

# ========================================================
# Test Signal
# ========================================================

f1 = 65
hmax = 50
hmag = 0

Fr = 60
SNR = 60

x, Xr, fr, ROCOFr = signal_frequency(f1, (Nc + 100) * Nppc, f0, Fs, Fr, hmax, hmag, SNR)

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


# ========================================================
# Main loop for real time processing
# ========================================================

# For test purpose only
# --------------------------------------------------------
f_zc_test = np.zeros(len(x))
x_filt_zc = np.zeros(len(x))

x_filt_BSP = np.zeros(len(x))
x_int_BSP = []

for nn in range(len(x)):
    
    xx = x[nn]
    
    # ========================================================
    # Frequency Estimation
    # ========================================================
    
    # Filter to eliminate harmonics
    #---------------------------------------------------------
        
    x_buff_ZC[buff_pt_ZC] = xx
    v = 0
    for kk in range(len(num_pre_ZC)):
        v += num_pre_ZC[kk]*x_buff_ZC[buff_pt_ZC]
        buff_pt_ZC -= 1
        if buff_pt_ZC < 0: 
            buff_pt_ZC = len(num_pre_ZC) - 1
    
    buff_pt_ZC += 1
    if buff_pt_ZC > (len(num_pre_ZC) - 1):
        buff_pt_ZC = 0
        
    x_filt_zc[nn] = v # For test purpose only
    
    # Zero Crossing Detection
    #---------------------------------------------------------
    if va >= 0:
        sig = va * v
    else:
        sig = 1

    Tsc += Ts
    cnt += 1

    if sig < 0:  
        Nb = v / (v - va)
        T2 = Nb * Ts
        Tsc = Tsc + T1 - T2
        f_zc = 1/Tsc
        T1 = T2
        Tsc = 0
        cnt = 0

    va = v
    
    f_zc_test[nn] = f_zc # For test purpose only
    
    # ========================================================
    # B-Spline Interpolation
    # ========================================================
    
    # Pre-Filter
    #---------------------------------------------------------
    x_buff_BSP[x_buff_pt_BSP] = xx
    
    xpre = 0
    for kk in range(len(num_pre_BSP)):
        
        xpre += num_pre_BSP[kk]*x_buff_BSP[x_buff_pt_BSP]
        
        x_buff_pt_BSP -= 1
        if x_buff_pt_BSP < 0: 
            x_buff_pt_BSP = len(num_pre_BSP) - 1
    
    for jj in range(len(den_pre_BSP)-1):
        
        xpre -= den_pre_BSP[jj+1]*y_buff_BSP[y_buff_pt_BSP]
        
        y_buff_pt_BSP -= 1
        if y_buff_pt_BSP < 0: 
            y_buff_pt_BSP = len(den_pre_BSP) - 2
            
    x_buff_pt_BSP += 1
    if x_buff_pt_BSP > (len(num_pre_BSP) - 1):
        x_buff_pt_BSP = 0
        
    y_buff_pt_BSP += 1
    if y_buff_pt_BSP > (len(den_pre_BSP) - 2):
        y_buff_pt_BSP = 0
    
    y_buff_BSP[y_buff_pt_BSP] = xpre 
    
    x_filt_BSP[nn] = xpre # For test purpose only
    
    # Farrow Structure
    #---------------------------------------------------------
    
    buffer_farrow[0] = buffer_farrow[1]
    buffer_farrow[1] = buffer_farrow[2]
    buffer_farrow[2] = buffer_farrow[3]
    buffer_farrow[3] = xpre
    
    if(f_zc != 0):
        lamb = f0/f_zc
    else:
        lamb = 0
        
    if nn >= (MBSP+2):
        while alfa < 1.0:
            H0 = (-1/6)*buffer_farrow[0] + 0.5*buffer_farrow[1] - 0.5*buffer_farrow[2] + (1/6)*buffer_farrow[3]
            H1 = 0.5*buffer_farrow[0] - buffer_farrow[1] + 0.5*buffer_farrow[2]
            H2 = -0.5*buffer_farrow[0] + 0.5*buffer_farrow[2]
            H3 = (1/6)*buffer_farrow[0] + (2/3)*buffer_farrow[1] + (1/6)*buffer_farrow[2]

            xi = (alfa**3)*H0 + (alfa**2)*H1 + alfa*H2 + H3
            x_int_BSP.append(xi)
            
            alfa += lamb
        alfa -= 1.0
        
        

# ========================================================
# Plots
# ========================================================


fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Input Signal", "Filtered Signal"))

fig.add_trace(go.Scatter(x = t, y=x, name="Signal", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(x = t, y=x_filt_zc, name="Signal", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(x = t, y=f_zc_test, name="Frequency", mode='lines'), row=3, col=1)
fig.update_yaxes(title_text="Amp", row=1, col=1)
fig.update_yaxes(title_text="Amp", row=2, col=1)
fig.update_yaxes(title_text="Freq (Hz)", row=3, col=1)
fig.update_xaxes(title_text="Time (s)", row=2, col=1)

fig.update_layout(
    title_text="Frequency Estimation",
    title_font=dict(size=24, family='Arial', color='black'), 
    title_x=0.5,  
    template='gridon'
)

fig.show()


fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Input Signal", "Filtered Signal", "Interpolated Signal"))

fig.add_trace(go.Scatter(y=x, name="Signal", mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(y=x_filt_BSP, name="Filtered Signal", mode='lines'), row=2, col=1)
fig.add_trace(go.Scatter(y=x_int_BSP, name="Interpolated Signal", mode='lines'), row=3, col=1)
fig.update_yaxes(title_text="Amp", row=1, col=1)
fig.update_yaxes(title_text="Amp", row=2, col=1)
fig.update_yaxes(title_text="Amp", row=3, col=1)
fig.update_xaxes(title_text="Time (s)", row=2, col=1)

fig.update_layout(
    title_text="B-Spline Interpolation",
    title_font=dict(size=24, family='Arial', color='black'), 
    title_x=0.5,  
    template='gridon'
)

fig.show()







# fig = go.Figure()
# fig.add_trace(go.Scatter(y=lfilter(num_pre_BSP, den_pre_BSP, x), name="Reference", mode='lines'))
# fig.add_trace(go.Scatter(y=x_filt_BSP, name="Prefiltro ", mode='lines'))

# fig.update_yaxes(title_text="Amplitude")
# fig.update_xaxes(title_text="Time (s)")

# fig.update_layout(
#     autosize=True,
#     title_text="Prefiltro Bspline",
#     title_font=dict(size=24, family='Arial', color='black'),  
#     title_x=0.5,  
#     template='gridon'
# )
# fig.show()