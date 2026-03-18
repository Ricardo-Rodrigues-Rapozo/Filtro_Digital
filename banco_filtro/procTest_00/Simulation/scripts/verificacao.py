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

Nf = int(np.ceil(len(h) / M))
Ehh = np.zeros((M, Nf))

for kk in range(M):
    hh = np.array(h[kk::M])
    hh_padded = np.pad(hh, (0, Nf - len(hh)), "constant")
    Ehh[kk, :] = hh_padded

Ehh = Ehh.astype(np.float64)
Ehh_col = Ehh.reshape(-1, order="C")
np.savetxt(REFERENCE_DIR / "Ehh.txt", Ehh_col, fmt="%.18e", newline="\n")

buffer = np.zeros(M)
E = np.zeros((M, Nf))
E0 = np.zeros(M)
v = np.zeros((M, (len(x) // M) + 1), dtype=complex)
jj = 0

for nn in range(len(x)):
    for kk in range(M - 1):
        buffer[M - 1 - kk] = buffer[M - 2 - kk]
    buffer[0] = x[nn]

    if (nn % M) == 0:
        for mm in range(M):
            for kk in range(Nf - 1, 0, -1):
                E[mm, kk] = E[mm, kk - 1]
            E[mm, 0] = buffer[mm]
            E0[mm] = np.dot(Ehh[mm, :], E[mm, :])

        vv = M * np.fft.ifft(E0)
        v[:, jj] = vv
        jj += 1

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

# plt.plot(Xc[0:3,:], marker='o', linestyle='-',label = 'Fasores Xc')

np.savetxt(OUTPUT_DIR / "Xc.csv", Xc, fmt="%.18e", delimiter=",")
print(f"Matriz AFT salva em: {OUTPUT_DIR / 'AFT_59Hz.csv'}")


np.savetxt(OUTPUT_DIR / "output_python_polifasico_59Hz_real.txt", np.real(v[:50, :]), fmt="%.18e")
np.savetxt(OUTPUT_DIR / "output_python_polifasico_59Hz_imag.txt", np.imag(v[:50, :]), fmt="%.18e")



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



plt.plot(AFT[37,:], marker='o', linestyle='-')
plt.plot(magref[37,:], marker='o', linestyle='-')
plt.title('37th Harmonic Magnitude')
plt.show()




np.savetxt(OUTPUT_DIR / "Xref.csv", X_ref, fmt="%.18e", delimiter=",")
np.savetxt(OUTPUT_DIR / "AFT.csv", AFT, fmt="%.18e", delimiter=",")
np.savetxt(OUTPUT_DIR / "magref.csv", magref, fmt="%.18e", delimiter=",")


plt.figure()
plt.subplot(2,2,1)
plt.plot(AFT[0,:], marker='o', linestyle='-')
plt.plot(magref[0,:], marker='o', linestyle='-')
plt.title('Fundamental Magnitude')

plt.subplot(2,2,2)
plt.plot(AFT[2,:], marker='o', linestyle='-')
plt.plot(magref[2,:], marker='o', linestyle='-')
plt.title('3rd Harmonic Magnitude')

plt.subplot(2,2,3)
plt.plot(AFT[4,:], marker='o', linestyle='-')
plt.plot(magref[4,:], marker='o', linestyle='-')
plt.title('5th Harmonic Magnitude')

plt.subplot(2,2,4)
plt.plot(AFT[6,:], marker='o', linestyle='-')
plt.plot(magref[6,:], marker='o', linestyle='-')
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



# H = np.fft.rfft(h, 16384)
# fh = np.fft.rfftfreq(16384, d=1 / Fs)

# plt.figure()
# plt.plot(fh, np.abs(H))
# plt.title("FFT do filtro")
# plt.xlabel("Frequencia (Hz)")
# plt.ylabel("Magnitude")
# plt.grid()
# plt.show()

# X = np.fft.rfft(x)
# f = np.fft.rfftfreq(len(x), d=1 / Fs)

# plt.figure()
# plt.plot(f, np.abs(X))
# plt.title("FFT do sinal")
# plt.xlabel("Frequencia (Hz)")
# plt.ylabel("Magnitude")
# plt.grid()
# plt.show()

# plt.figure()
# plt.plot(t, x)
# plt.title("Input Signal")
# plt.show(block=False)

# plt.figure()
