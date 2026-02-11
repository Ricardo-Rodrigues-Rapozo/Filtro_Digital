import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import mplcursors

def downsample(signal, factor):
    signal = np.asarray(signal)
    downsampled = signal[..., ::factor]  # preserva todas as dimensões anteriores
    return downsampled

BASE_DIR = Path(__file__).parent

# Parâmetros 
######################################################################
f0 = 60
Nppc = 256
Fs = Nppc*60
Ts = 1/Fs
M = Fs//f0

fbDelay = (8*Nppc)//(2*M) #(len(h))//(2*M)

# Leitura do arquivo de saída do SAPHO e montagem da matriz de fasores
######################################################################
out = np.loadtxt(BASE_DIR / "output_1.txt")

real = out[0::2]/1000000
imag = out[1::2]/1000000

fasores = real + 1j*imag

N = len(fasores)//50
fasores = fasores[0:50*N]

fasor_h = fasores.reshape(50, N, order='F')
fasor_h = fasor_h[1:50,:]

AFT = 2*np.abs(fasor_h)
PFT = np.rad2deg(np.angle(fasor_h))

# Leitura dos fasores de referência
#######################################################################
# X_real = np.loadtxt(BASE_DIR / "X_real_59Hz.txt")
# X_imag = np.loadtxt(BASE_DIR / "X_imag_59Hz.txt")

# X_real = downsample(X_real,M)
# X_real = X_real[:,0:fasor_h.shape[1]]

# X_imag = downsample(X_imag,M)
# X_imag = X_imag[:,0:fasor_h.shape[1]]

# np.savetxt(BASE_DIR / "X_real.txt", X_real)
# np.savetxt(BASE_DIR / "X_imag.txt", X_imag)

X_real = np.loadtxt(BASE_DIR / "X_real.txt")
X_imag = np.loadtxt(BASE_DIR / "X_imag.txt")

X_ref = X_real + 1j*X_imag

X_ref = np.hstack((np.zeros((50, fbDelay)), X_ref)) # Reference delay to compensate FilterBank delay
X_ref = X_ref[:,0:fasor_h.shape[1]]



magref = np.abs(X_ref)
angref = np.unwrap(np.angle(X_ref))

# Correção da Fase
#######################################################################

freq = 59*np.ones(fasor_h.shape[1])
freq   = np.concatenate((np.zeros(fbDelay), freq))
freq   = freq[0:fasor_h.shape[1]]
delta_f = freq - 60
correc = np.zeros(len(delta_f))



# Trapezoidal Integration (without error accumulation)
for nn in range(1, len(delta_f)):
    if(nn >= fbDelay+1):
        correc[nn] = correc[nn-1] + np.pi*(delta_f[nn] + delta_f[nn-1])*(M*Ts)

# Multiplies the correction by each harmonic (h = 1:50)
h = np.arange(1, 50).reshape(-1, 1)   # shape (50, 1)
correcH = h*correc

PFTc = np.unwrap((PFT) + np.unwrap(correcH)) 
Xc = AFT*np.exp(1j*PFTc)

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

