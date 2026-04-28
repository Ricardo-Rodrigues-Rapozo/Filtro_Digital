import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import mplcursors
import auxiliares
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def downsample(signal, factor):
    signal = np.asarray(signal)
    downsampled = signal[..., ::factor]  # preserva todas as dimensões anteriores
    return downsampled

BASE_DIR = Path(__file__).parent
SIMULATION_DIR = BASE_DIR.parent
OUTPUT_DIR = SIMULATION_DIR / "data" / "output"

# Parâmetros 
######################################################################
f0 = 60
Nppc = 512
Fs = Nppc*60
Ts = 1/Fs
M = Fs//f0
hmax = 50
fbDelay = (8*Nppc)//(2*M) #(len(h))//(2*M)
f1 = 60

# Leitura do arquivo de saída do SAPHO e montagem da matriz de fasores
######################################################################
out = np.loadtxt(OUTPUT_DIR / "saida_fm_0.2.txt")

real = out[0::2]/1_000_000.0
imag = out[1::2]/1_000_000.0

fasores = real + 1j*imag

# Detecta o número de componente por frame (50 ou 51)
Nh = None
for cand in (50, 51):
    if len(fasores) % cand == 0:
        Nh = cand
        break
if Nh is None:
    raise ValueError(f"len(fasores)={len(fasores)} not multiple of 50 or 51. Check SAPHO saving loop.")

N = len(fasores)//Nh
fasores = fasores[0:Nh*N]

fasor_h = fasores.reshape(Nh, N, order='F')
fasor_h = fasor_h[1:50, fbDelay+1:len(fasor_h)]

AFT = 2*np.abs(fasor_h)
PFT = np.unwrap(np.angle(fasor_h))

# Leitura do arquivo de saída do SAPHO e montagem day matriz de referência
######################################################################

X_real = np.loadtxt(OUTPUT_DIR / "X_fm_0.2_real.txt")
X_imag = np.loadtxt(OUTPUT_DIR / "X_fm_0.2_imag.txt")

X_ref = X_real + 1j*X_imag
X_ref = X_ref[:,0:fasor_h.shape[1]]

magref = np.abs(X_ref)
angref = np.unwrap(np.angle(X_ref))

# Correção da Fase
#######################################################################

freq = f1*np.ones(fasor_h.shape[1])
#freq = np.loadtxt(OUTPUT_DIR / "f_rampa_referencia.txt")
#freq = downsample(freq,M)  # Reduz a taxa de amostragem pela metade
delta_f = freq - 60
correc = np.zeros(len(delta_f))


# Integração Trapezoidal
for nn in range(1, len(delta_f)):
    if(nn >= 1):
        correc[nn] = correc[nn-1] + np.pi*(delta_f[nn] + delta_f[nn-1])*(M*Ts)

h = np.arange(1, 50).reshape(-1, 1)   # shape (50, 1)
correcH = h*correc

PFTc = np.unwrap((PFT) + np.unwrap(correcH))
Xc = AFT*np.exp(1j*PFTc)

plt.figure()
plt.subplot(2,2,1)
plt.plot(AFT[45,:], marker='o', linestyle='-')
plt.plot(magref[45,:], marker='o', linestyle='-')
plt.title('Fundamental Magnitude')

plt.subplot(2,2,2)
plt.plot(AFT[46,:], marker='o', linestyle='-')
plt.plot(magref[46,:], marker='o', linestyle='-')
plt.title('3rd Harmonic Magnitude')

plt.subplot(47,2,3)
plt.plot(AFT[4,:], marker='o', linestyle='-')
plt.plot(magref[4,:], marker='o', linestyle='-')
plt.title('5th Harmonic Magnitude')

plt.subplot(2,2,4)
plt.plot(AFT[38,:], marker='o', linestyle='-')
plt.plot(magref[38,:], marker='o', linestyle='-')
plt.title('7th Harmonic Magnitude')

plt.show(block=False)

plt.figure()
plt.subplot(2,2,1)
# plt.plot(np.rad2deg(PFT[0,:]), marker='o', linestyle='-')
plt.plot(np.rad2deg(PFTc[0,:]), marker='o', linestyle='-')
plt.plot(np.rad2deg(angref[0,:]), marker='o', linestyle='-')
plt.title('Fundamental Phase')

plt.subplot(2,2,2)
# plt.plot(np.rad2deg(PFT[2,:]), marker='o', linestyle='-')
plt.plot(np.rad2deg(PFTc[2,:]), marker='o', linestyle='-')
plt.plot(np.rad2deg(angref[2,:]), marker='o', linestyle='-')
plt.title('3rd Harmonic Phase')

plt.subplot(2,2,3)
# plt.plot(np.rad2deg(PFT[4,:]), marker='o', linestyle='-')
plt.plot(np.rad2deg(PFTc[4,:]), marker='o', linestyle='-')
plt.plot(np.rad2deg(angref[4,:]), marker='o', linestyle='-')
plt.title('5th Harmonic Phase')

plt.subplot(2,2,4)
# plt.plot(np.rad2deg(PFT[6,:]), marker='o', linestyle='-')
plt.plot(np.rad2deg(PFTc[6,:]), marker='o', linestyle='-')
plt.plot(np.rad2deg(angref[6,:]), marker='o', linestyle='-')
plt.title('7th Harmonic Phase')

cursor = mplcursors.cursor(hover=True)
plt.show()

a = 1

Xc = Xc[0::2]
X_ref = X_ref[0::2]
AFT = AFT[0::2]
PFTc = PFTc[0::2]
magref = magref[0::2]
angref = angref[0::2]

ErroAFT = 100*np.abs(AFT - magref)/AFT      # Magnitude Error (%)
ErroPFT = np.abs(PFTc - angref)*180/np.pi   # Phase Error (°)
TVEFT = auxiliares.TVE(Xc,X_ref)     # TVE (%)
TVEFT   = TVEFT[:,10:]
ErroAFT   = ErroAFT[:,10:]
ErroPFT   = ErroPFT[:,10:]

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
indh = np.arange(0,50,2)+1

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
    title_text=f"Errors for Harmonic",
    title_font=dict(size=24, family='Arial', color='black'),
    title_x=0.5,
    template='gridon'
)
fig.show()

TVEFTmin = np.min(TVEFT, axis=1)
TVEFTmax = np.max(TVEFT, axis=1)
TVEFTavg = np.mean(TVEFT, axis=1)
indh = np.arange(0,50,2)+1

fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=("Magnitude Error", "Phase Error", "Total Vector Error (TVE)"))


fig.add_trace(go.Scatter(x=indh, y=TVEFTmax,   name="Average", mode='lines+markers', marker_symbol='circle', line=dict(color='crimson')), row=1, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([TVEFTavg, TVEFTmax[::-1]]), fill='toself', fillcolor='rgba(220,20,60,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximum'), row=1, col=1)
fig.add_trace(go.Scatter(x=indh, y=np.ones(len(TVEFTmax)),   name="Limit IEC/IEEE 60255-118-1", mode='lines',line=dict(color='black', dash='dot')), row=1, col=1)


fig.update_yaxes(title_text="TVE (%)", row=1, col=1)
fig.update_xaxes(title_text="Harmonic", row=1, col=1)

fig.update_layout(
    title_text=f"Errors for Harmonic",
    title_font=dict(size=24, family='Arial', color='black'),
    title_x=0.5,
    template='gridon'
)
fig.show()
