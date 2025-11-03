import numpy as np
from scipy.signal import freqz, lfilter, firls, upfirdn
import matplotlib.pyplot as plt
import mplcursors
import sinaisIEC60255_118
from pathlib import Path

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


def downsample(signal, factor):
    downsampled = signal[::factor]
    return downsampled

# #===================================================
# # Parametros
# #===================================================
# f0 = 60
# Nppc = 128
# Fs = f0*Nppc
# Nc = 100
# t = np.arange(Nc*Nppc)/Fs

# #===================================================
# # Sinal de Teste
# #===================================================
# f1 = 60

# hmax = 50
# hmag = 0.1

# Fr = 60
# SNR = 1000000

# x,Xr,f1r,ROCOFr = sinaisIEC60255_118.signal_frequency(f1, (Nc+1)*Nppc, f0, Fs, Fr, hmax, hmag, SNR)
# Xr = Xr[:,:Nc*Nppc]
# f1r = f1r[:Nc*Nppc]
# ROCOFr = ROCOFr[:Nc*Nppc]

# plt.figure()
# plt.plot(t,x[:Nc*Nppc])
# plt.grid()
# plt.xlabel('Time (s)')
# plt.ylabel('Magnitude')
# plt.title('Sinal de Teste')
# mplcursors.cursor(hover=True)
# plt.show(block = False)



from scipy.signal import freqz, lfilter, firls, upfirdn, firwin

##------------------------------------------------------------------------------------------------------
## ---------------------------------- ler_coluna -------------------------------------------------------
##------------------------------------------------------------------------------------------------------
def ler_coluna(arquivo: str | Path, col: int = 0) -> np.ndarray:
    """Lê uma coluna específica de um arquivo .txt (índice começa em 0)."""
    try:
        x = np.loadtxt(arquivo, usecols=col, dtype=float, ndmin=1)
    except Exception as e:
        raise ValueError(f"Erro ao ler coluna {col} de {arquivo}: {e}")
    if x.size == 0:
        raise ValueError(f"Sem dados numéricos em {arquivo} (coluna {col})")
    return x

dir_base = Path(r"C:\Users\Ricardo\Documents\Dissertação\procTest_00\Simulation")
dir_base2 = Path(r"C:\Users\Ricardo\Documents\Dissertação\python")
arq1 = dir_base / "input_0.txt"
x1 = ler_coluna(arq1, col=0) ## entrada multiplicada por 1000
#===================================================
# Protótipo do Filtro
#===================================================

# Filtro DFT
h = np.array([
    0.01363158,
    0.02947376,
    0.07149450,
    0.12460785,
    0.16825941,
    0.18506581,
    0.16825941,
    0.12460785,
    0.07149450,
    0.02947376
])
omega,H = freqz(h,1,4096)
f = omega/(2*np.pi)
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

M = 5
#x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70]
x = x1
H = [h[i::M] for i in range(M)]

E = np.zeros((M,len(h)//M))

for kk in range(M):
    E[kk,:] = h[kk::M]
print(E)
# #===================================================
# # Resposta em Frequência do Banco de Filtros
# #===================================================

# plt.figure()
# plt.title('Resposta em Magnitude do Filtro')
# for kk in range(1,M):
#     EH = np.convolve(E[kk],M*idftmtx[kk,:])
#     omega,H = freqz(EH,1,4096)
#     f = omega*Fs/(2*np.pi)
#     H_mag = abs(H)
#     plt.plot(f,H_mag)
#     plt.show(block=False)
# plt.grid()
# plt.xlabel('Frequência (Hz)')
# plt.ylabel('Magnitude')
# mplcursors.cursor(hover=True)
# plt.show(block=False)

#===================================================
# Aplicação dos Filtros
#===================================================




## Neste codigo o xx é equivalente ao Exx que são as amostras que vao ser usadas no filtro. Isso não equivale ao meu codigo no meu entender
## Ele não faz o rodizio como esperado, e sim pega uma amostra deslocada de M apenas



Eout = np.zeros((M,len(x)//M))
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
    v[:,nn] = np.conj(M*np.fft.ifft(Eout[:,nn]))#idftmtx.dot(Eout[:,nn])#
    
# #===================================================
# # Plot dos Resultados
# #===================================================

# Xref = np.zeros((hmax,Nc*Nppc//M), dtype=complex)
# for hh in range(hmax):
#     Xref[hh,:] = downsample(Xr[hh,:Nc*Nppc], M) 
print(v.shape)
plt.figure()
plt.suptitle('Magnitudes dos Fasores')
for hh in range(1200):
    #plt.subplot(4,2,hh+1)
    plt.plot(abs(v[:,hh])*2/np.sqrt(2), label = 'Estimado %d' %hh)
    #plt.plot(abs(Xref[hh-1,:]), label = 'Referência %d' %hh)
    # plt.xlabel('Tempo (s)')
    # plt.ylabel('Magnitude')
    # plt.legend()
    # plt.grid()
#mplcursors.cursor(hover=True)
plt.show()


plt.figure()
plt.suptitle('Fase Fasores')
for hh in range(1200):
    plt.plot(np.unwrap(np.angle(v[:,hh])), label = 'Estimado %d' %hh)
    #plt.plot(np.angle(Xref[hh-1,:]), label = 'Referência %d' %hh)
    # plt.ylim(-np.pi-1, np.pi+1)
    # plt.xlabel('Tempo (s)')
    # plt.ylabel('Fases (rad)')
    # plt.legend()
    # plt.grid()
#mplcursors.cursor(hover=True)
plt.show()


# #===================================================
# # Cálculo dos Erros
# #===================================================

# erro_mag = np.zeros((hmax,Nc*Nppc//M))
# erro_fas = np.zeros((hmax,Nc*Nppc//M))
# TVEh = np.zeros((hmax,Nc*Nppc//M))
# for hh in range(1,hmax):

#     mag = abs(v[hh,:])*2/np.sqrt(2)
#     fas = np.unwrap(np.angle(v[hh,:]))
    
#     erro_mag[hh-1,:] = mag - abs(Xref[hh-1,:])
#     erro_fas[hh-1,:] = (180/np.pi)*(fas - np.angle(Xref[hh-1,:]))

#     re,im = pol2cart(mag, fas)
#     fasor = re + 1j*im
    
#     TVEh[hh-1,:] = TVE(fasor,Xref[hh-1,:])
    

# erro_mag = erro_mag[:,M//2:]
# erro_fas = erro_fas[:,M//2:]
# TVEh = TVEh[:,M//2:]


# plt.figure()
# plt.suptitle('Erro Magnitudes')
# plt.stem(range(1,hmax+1),erro_mag.max(axis=1))
# mplcursors.cursor(hover=True)
# plt.show(block = False)

# plt.figure()
# plt.suptitle('Erro Fases')
# plt.stem(range(1,hmax+1),erro_fas.max(axis=1))
# mplcursors.cursor(hover=True)
# plt.show(block = False)

# plt.figure()
# plt.suptitle('TVE')
# plt.stem(range(1,hmax+1),TVEh.max(axis=1))
# mplcursors.cursor(hover=True)
# plt.show(block = True)