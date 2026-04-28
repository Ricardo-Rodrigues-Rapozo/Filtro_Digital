import numpy as np
from scipy.signal import freqz, lfilter, firls, upfirdn
import matplotlib.pyplot as plt
import mplcursors
from pathlib import Path

def downsample(signal, factor):
    downsampled = signal[::factor]
    return downsampled



import matplotlib.pyplot as plt
import mplcursors
import numpy as np
from pathlib import Path
import auxiliares
from plotly.subplots import make_subplots
import plotly.graph_objects as go

SCRIPT_DIR = Path(__file__).resolve().parent
SIMULATION_DIR = SCRIPT_DIR.parent
INPUT_DIR = SIMULATION_DIR / "data" / "input"
OUTPUT_DIR = SIMULATION_DIR / "data" / "output"
REFERENCE_DIR = SIMULATION_DIR / "data" / "reference"

f0 = 60
Nppc = 256
Fs = f0 * Nppc
Ts = 1 / Fs
Ganho_saida_sapho = 1000000
Ganho_saida_interpolador = 10000

x = np.loadtxt(INPUT_DIR / "saida_59hz_interpolador.txt")
x = np.loadtxt(OUTPUT_DIR / "xteste.txt") * Ganho_saida_sapho #* (2**14)   ## Entrada interpolador Python


x = x // 10 ## POR CONTA DAS 
Nc = len(x) // Nppc
t = np.arange(len(x)) * Ts

np.savetxt(OUTPUT_DIR / "input_0.txt", x, fmt="%d")

x = x  / Ganho_saida_interpolador
#x = x/max(np.abs(x)) # Normalização do sinal de entrada para evitar saturação

print(Nc)
print(f"Tamanho de x: {len(x)}")
print(f"Tamanho esperado: {Nc * Nppc}")

# v1r = np.loadtxt(OUTPUT_DIR / "output_1.txt") / Ganho_saida_sapho
# v1i = np.loadtxt(OUTPUT_DIR / "output_2.txt") / Ganho_saida_sapho
# v3r = np.loadtxt(OUTPUT_DIR / "output_3.txt") / Ganho_saida_sapho
# v3i = np.loadtxt(OUTPUT_DIR / "output_4.txt") / Ganho_saida_sapho
# v5r = np.loadtxt(OUTPUT_DIR / "output_5.txt") / Ganho_saida_sapho
# v5i = np.loadtxt(OUTPUT_DIR / "output_6.txt") / Ganho_saida_sapho

M = 256

c5 = [1.0005967, 1.9991048, 1.9097925, 1.4448987, 0.66403725, 0.1304229]

N = 8 * (Fs // f0)
n1 = np.arange(-(N - 1) / 2, 1 + (N - 1) / 2, 1)

wM = np.zeros(N)

for m in range(len(c5)):
    wM = wM + c5[m] * np.cos(m * (2 * np.pi / N) * n1)

wM = wM / np.sum(wM)
h = wM
h_filtro = h
Nf = int(np.ceil(len(h) / M))
Ehh = np.zeros((M, Nf))

#===================================================
# Decomposição Polifásica
#===================================================
M = Nppc
#x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70]
H = [h[i::M] for i in range(M)]

E = np.zeros((M,len(h)//M))

 # Ajusta o tamanho de x para ser múltiplo de M

for kk in range(M):
    E[kk,:] = h[kk::M]
print(E)

#===================================================
# Aplicação dos Filtros
#===================================================


Eout = np.zeros((M,len(x)//M))
Eout = np.zeros((M, len(downsample(x, M))))
for mm in range(M):    
    x_slice = x[0:len(x)-mm]
    zeros = np.zeros(mm)
    
    xxa = np.concatenate((zeros, x_slice)) 

    xx = downsample(xxa, M)

    Eout[mm,:] = lfilter(E[mm],1,xx)
    teste =  0# para debug
#===================================================
# Aplicação da IDFT
#===================================================

v = np.zeros((M,len(x)//M), dtype=complex)

for nn in range(len(x)//M):
    v[:,nn] = M*np.fft.ifft(Eout[:,nn])





Delay = 5
print("TAMANHO DE V :",v.shape)
v = v[:, Delay:]
print("TAMANHO DE V :",v.shape)
np.savetxt(OUTPUT_DIR / "ifft.csv", v, fmt="%.18e", delimiter=",")



AFT = 2*np.abs(v[1:50,:])
PFT = np.unwrap(np.angle(v[1:50,:]))
delta_f = (59 - 60) * np.ones(len(v[0]))
correc = np.zeros(len(delta_f))




# Integração Trapezoidal
for nn in range(1, len(delta_f)):
    if(nn >= 1):
        correc[nn] = correc[nn-1] + np.pi*(delta_f[nn] + delta_f[nn-1])*(M*Ts)



h = np.arange(1, 50).reshape(-1, 1)   # shape (50, 1)
correcH = h*correc

PFTc = np.unwrap((PFT) + np.unwrap(correcH))
Xc = AFT*np.exp(1j*PFTc)


np.savetxt(OUTPUT_DIR / "Xc.csv", Xc, fmt="%.18e", delimiter=",")
print(f"Matriz AFT salva em: {OUTPUT_DIR / 'AFT_59Hz.csv'}")






###======================================================================##
###               RESPOSTA EM MAGNITUDE E FASE DO FILTRO                 ##
###======================================================================##

Nfft = 16384
H = np.fft.fft(h_filtro, Nfft)              # resposta em frequencia
f = np.fft.fftfreq(Nfft, d=1/Fs)            # vetor de frequencia

# manter somente a parte positiva
idx = f >= 0
f_pos = f[idx]
H_pos = H[idx]

mag = np.abs(H_pos)
mag_db = 20*np.log10(np.maximum(mag, 1e-12))
fase = np.unwrap(np.angle(H_pos))

fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

axs[0].plot(f_pos, mag)
axs[0].set_title("Magnitude do filtro")
axs[0].set_ylabel("|H(f)|")
axs[0].grid(True)

axs[1].plot(f_pos, mag_db)
axs[1].set_title("Magnitude do filtro em dB")
axs[1].set_ylabel("Magnitude (dB)")
axs[1].grid(True)

axs[2].plot(f_pos, fase)
axs[2].set_title("Fase do filtro")
axs[2].set_xlabel("Frequencia (Hz)")
axs[2].set_ylabel("Fase (rad)")
axs[2].grid(True)

plt.tight_layout()
plt.show()


###======================================================================##
###======================================================================##
###======================================================================##


X_real = np.loadtxt(REFERENCE_DIR / 'X_ref_real_59.txt')
X_imag = np.loadtxt(REFERENCE_DIR / 'X_ref_imag_59.txt')

X_ref = X_real + 1j*X_imag
X_ref = X_ref[:,0:v.shape[1]]
print('TAMANHO X',len(X_ref[0]))
magref = np.abs(X_ref[:,:len(X_ref[0]) ])
angref = np.unwrap(np.angle(X_ref[:,:len(X_ref[0])]))



plt.plot(AFT[46,:], marker='o', linestyle='-',label = 'Fasores AFT')
plt.plot(magref[46,:], marker='o', linestyle='-',label = 'Fasores X_ref')
plt.title('47th Harmonic Magnitude')
plt.show()

plt.plot(np.rad2deg(PFTc[46,:]), marker='o', linestyle='-',label = 'Fasores PFTc')
plt.plot(np.rad2deg(angref[46,:]), marker='o', linestyle='-',label = 'Fasores X_ref')
plt.title('47th Harmonic Phase')
plt.legend()
plt.show()




np.savetxt(OUTPUT_DIR / "Xref.csv", X_ref, fmt="%.18e", delimiter=",")
np.savetxt(OUTPUT_DIR / "AFT.csv", AFT, fmt="%.18e", delimiter=",")
np.savetxt(OUTPUT_DIR / "magref.csv", magref, fmt="%.18e", delimiter=",")





plt.figure()
plt.subplot(2,2,1)
plt.plot(AFT[46,:], marker='o', linestyle='-')
plt.plot(magref[46,:], marker='o', linestyle='-')
plt.title('47th Harmonic Magnitude')

plt.subplot(2,2,2)
plt.plot(AFT[44,:], marker='o', linestyle='-',label = 'Fasores AFT')
plt.plot(magref[44,:], marker='o', linestyle='-',label = 'Fasores X_ref')
plt.title('45th Harmonic Magnitude')
plt.legend()

plt.subplot(2,2,3)
plt.plot(AFT[40,:], marker='o', linestyle='-',label = 'Fasores AFT')
plt.plot(magref[40,:], marker='o', linestyle='-',label = 'Fasores X_ref')
plt.title('41st Harmonic Magnitude')
plt.legend()

plt.subplot(2,2,4)
plt.plot(AFT[38,:], marker='o', linestyle='-',label = 'Fasores AFT')
plt.plot(magref[38,:], marker='o', linestyle='-',label = 'Fasores X_ref')
plt.title('39th Harmonic Magnitude')
plt.legend()

plt.show(block=False)

plt.figure()
plt.subplot(2,2,1)
plt.plot(np.rad2deg(PFTc[46,:]), marker='o', linestyle='-',label = 'Fasores PFTc')
plt.plot(np.rad2deg(angref[46,:]), marker='o', linestyle='-',label = 'Fasores X_ref')
plt.title('47th Harmonic Phase')
plt.legend()

plt.subplot(2,2,2)
plt.plot(np.rad2deg(PFTc[44,:]), marker='o', linestyle='-',label = 'Fasores PFTc')
plt.plot(np.rad2deg(angref[44,:]), marker='o', linestyle='-',label = 'Fasores X_ref')
plt.title('45th Harmonic Phase')
plt.legend()

plt.subplot(2,2,3)
plt.plot(np.rad2deg(PFTc[38,:]), marker='o', linestyle='-',label = 'Fasores PFTc')
plt.plot(np.rad2deg(angref[38,:]), marker='o', linestyle='-',label = 'Fasores X_ref')
plt.title('39th Harmonic Phase')
plt.legend()

plt.subplot(2,2,4)
plt.plot(np.rad2deg(PFTc[40,:]), marker='o', linestyle='-',label = 'Fasores PFTc')
plt.plot(np.rad2deg(angref[40,:]), marker='o', linestyle='-',label = 'Fasores X_ref')
plt.title('41st Harmonic Phase')
plt.legend()


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
ErroAFT = ErroAFT[:,10:]
ErroPFT = ErroPFT[:,10:]
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


fig.add_trace(go.Scatter(x=indh, y=TVEFTavg,   name="Average", mode='lines+markers', marker_symbol='circle', line=dict(color='crimson')), row=1, col=1)
fig.add_trace(go.Scatter(x=np.concatenate([indh, indh[::-1]]),y=np.concatenate([TVEFTavg, TVEFTmax[::-1]]), fill='toself', fillcolor='rgba(220,20,60,0.2)', line=dict(color='rgba(255,255,255,0)'), name='Maximum'), row=1, col=1)
fig.add_trace(go.Scatter(x=indh, y=np.ones(len(TVEFTavg)),   name="Limit IEC/IEEE 60255-118-1", mode='lines',line=dict(color='black', dash='dot')), row=1, col=1)


fig.update_yaxes(title_text="TVE (%)", row=1, col=1)
fig.update_xaxes(title_text="Harmonic", row=1, col=1)

fig.update_layout(
    title_text=f"Errors for Harmonic",
    title_font=dict(size=24, family='Arial', color='black'),
    title_x=0.5,
    template='gridon'
)
fig.show()



H = np.fft.rfft(h, 16384)
fh = np.fft.rfftfreq(16384, d=1 / Fs)

plt.figure()
plt.plot(fh, np.abs(H))
plt.title("FFT do filtro")
plt.xlabel("Frequencia (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()

X = np.fft.rfft(x)
f = np.fft.rfftfreq(len(x), d=1 / Fs)

plt.figure()
plt.plot(f, np.abs(X))
plt.title("FFT do sinal")
plt.xlabel("Frequencia (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()

plt.figure()
plt.plot(t, x)
plt.title("Input Signal")
plt.show(block=False)

plt.figure()




