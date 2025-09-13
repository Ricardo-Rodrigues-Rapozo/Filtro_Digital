import numpy as np
from scipy.signal import freqz, lfilter, firls, upfirdn
import matplotlib.pyplot as plt
import mplcursors
import sinaisIEC60255_118

def TVE(X, Xr):

    X_re = np.real(X)
    X_im = np.imag(X)

    Xr_re = np.real(Xr)
    Xr_im = np.imag(Xr)

    TVE = 100*np.sqrt(((X_re - Xr_re)**2 + (X_im - Xr_im)**2)/(Xr_re**2 + Xr_im**2))

    return TVE


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def upsample_with_zeros(signal, factor):
    upsampled = np.zeros(len(signal) * factor)
    upsampled[::factor] = signal
    return upsampled


#===================================================
# Parametros
#===================================================
f0 = 60
Nppc = 128
Fs = f0*Nppc
Nc = 100
t = np.arange(Nc*Nppc)/Fs

#===================================================
# Sinal de Teste
#===================================================
f1 = 60

hmax = 50
hmag = 0.1

Fr = 60
SNR = 45

x,Xr,f1r,ROCOFr = sinaisIEC60255_118.signal_frequency(f1, (Nc+1)*Nppc, f0, Fs, Fr, hmax, hmag, SNR)
Xr = Xr[:,:Nc*Nppc]
f1r = f1r[:Nc*Nppc]
ROCOFr = ROCOFr[:Nc*Nppc]

plt.figure()
plt.plot(t,x[:Nc*Nppc])
plt.grid()
plt.xlabel('Time (s)')
plt.ylabel('Magnitude')
plt.title('Sinal de Teste')
mplcursors.cursor(hover=True)
plt.show(block = False)

#===================================================
# Protótipo do Filtro
#===================================================

# Filtro DFT
N = int(1*Nppc)
h = (1/N)*np.ones(N)

# N = 201
# h = firls(N,[0, 20/(Fs/2), 30/(Fs/2), 1], [1, 1, 0, 0])

omega,H = freqz(h,1,4096)
f = omega*Fs/(2*np.pi)
H_mag = abs(H)

plt.figure()
plt.title('Resposta em Magnitude do Filtro')
plt.plot(f,H_mag)
plt.grid()
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
mplcursors.cursor(hover=True)
plt.show(block=False)

#===================================================
# Decomposição Polifásica
#===================================================

M = Fs//f0

# H = [h[i::M] for i in range(M)]

E = np.zeros((M,len(h)))

for kk in range(M):
    E[kk,:] = upsample_with_zeros(h[kk::M], M)

idftmtx = np.linalg.inv(np.fft.fft(np.eye(M)))

#===================================================
# Resposta em Frequência do Banco de Filtros
#===================================================

plt.figure()
plt.title('Resposta em Magnitude do Filtro')
for kk in range(1,M):
    EH = np.convolve(E[kk],M*idftmtx[kk,:])
    omega,H = freqz(EH,1,4096)
    f = omega*Fs/(2*np.pi)
    H_mag = abs(H)
    plt.plot(f,H_mag)
    plt.show(block=False)
plt.grid()
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
mplcursors.cursor(hover=True)
plt.show(block=False)

#===================================================
# Aplicação dos Filtros
#===================================================

Eout = np.zeros((M,Nc*Nppc))
for mm in range(M):    
    xx = x[mm:Nc*Nppc+mm]
    
    Eout[mm,:] = lfilter(E[mm],1,xx)

#===================================================
# Aplicação da IDFT
#===================================================

v = np.zeros((M,Nc*Nppc), dtype=complex)

for nn in range(Nc*Nppc):
    v[:,nn] = np.conj(M*np.fft.ifft(Eout[:,nn]))#idftmtx.dot(Eout[:,nn])#

plt.figure()
plt.suptitle('Magnitudes dos Fasores')
for hh in range(1,7):
    plt.subplot(4,2,hh+1)
    plt.plot(abs(v[hh,:])*2/np.sqrt(2), label = 'Estimado %d' %hh)
    plt.plot(abs(Xr[hh-1,:]), label = 'Referência %d' %hh)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.grid()
mplcursors.cursor(hover=True)
plt.show(block = False)


plt.figure()
plt.suptitle('Fase Fasores')
for hh in range(1,7):
    plt.subplot(4,2,hh+1)
    plt.plot(np.unwrap(np.angle(v[hh,:])) - 2*np.pi*hh*(1/Nppc)*np.arange(len(v[hh,:])), label = 'Estimado %d' %hh)
    plt.plot(np.angle(Xr[hh-1,:]), label = 'Referência %d' %hh)
    # plt.ylim(-np.pi-1, np.pi+1)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Fases (rad)')
    plt.legend()
    plt.grid()
mplcursors.cursor(hover=True)
plt.show(block = False)


#===================================================
# Cálculo dos Erros
#===================================================

erro_mag = np.zeros((hmax,len(t)))
erro_fas = np.zeros((hmax,len(t)))
TVEh = np.zeros((hmax,len(t)))
for hh in range(1,hmax):

    mag = abs(v[hh,:])*2/np.sqrt(2)
    fas = np.unwrap(np.angle(v[hh,:])) - 2*np.pi*hh*(1/M)*np.arange(len(v[hh,:]))
    
    erro_mag[hh-1,:] = mag - abs(Xr[hh-1,:])
    erro_fas[hh-1,:] = (180/np.pi)*(fas - np.angle(Xr[hh-1,:]))

    re,im = pol2cart(mag, fas)
    fasor = re + 1j*im
    
    TVEh[hh-1,:] = TVE(fasor,Xr[hh-1,:])

erro_mag = erro_mag[:,Nppc*M//2:]
erro_fas = erro_fas[:,Nppc*M//2:]
TVEh = TVEh[:,Nppc*M//2:]

plt.figure()
plt.suptitle('Erro Magnitudes')
plt.stem(range(1,hmax+1),erro_mag.max(axis=1))
mplcursors.cursor(hover=True)
plt.show(block = False)

plt.figure()
plt.suptitle('Erro Fases')
plt.stem(range(1,hmax+1),erro_fas.max(axis=1))
mplcursors.cursor(hover=True)
plt.show(block = False)

plt.figure()
plt.suptitle('TVE')
plt.stem(range(1,hmax+1),TVEh.max(axis=1))
mplcursors.cursor(hover=True)
plt.show(block = True)