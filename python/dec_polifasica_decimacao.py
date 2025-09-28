import numpy as np
from scipy.signal import freqz, lfilter, firls, upfirdn
import matplotlib.pyplot as plt
import mplcursors
import sinaisIEC60255_118
from scipy.signal import firwin

def TVE(X, Xr):
 
    X_re = np.real(X)
    X_im = np.imag(X)

    Xr_re = np.real(Xr)
    Xr_im = np.imag(Xr)

    TVE = 100*np.sqrt(((X_re - Xr_re)**2 + (X_im - Xr_im)**2)/(Xr_re**2 + Xr_im**2))

    return TVE


def pol2cart(rho, phi):
    #Transforma coordenadas polares em cartesiana
    x = rho * np.cos(phi) 
    y = rho * np.sin(phi)
    return(x, y)

def upsample_with_zeros(signal, factor):
    upsampled = np.zeros(len(signal) * factor)
    upsampled[::factor] = signal # [start:stop:step] pegando elementos do inicio ao fim de factor em factor 
    return upsampled


def downsample(signal, factor):
    downsampled = signal[::factor]# [start:stop:step] pegando elementos do inicio ao fim de factor em factor 
    return downsampled

def downsample_1(x, M): 
    """
    Aplica a fórmula de decimação y[n] = x[n * M], 
    reduzindo a taxa de amostragem do sinal de entrada.

    Parâmetros:
    x : array-like
        Sinal original a ser decimado.
    M : int
        Fator de decimação. A cada M amostras, uma é mantida.

    Retorno:
    numpy.ndarray
    
    xx_hands : Sinal decimado, contendo uma amostra a cada M posições do sinal original.
    
    """
    xx_hands = []
    count = 0
    for mn in range(len(x)):
        if (mn % M == 0):
            xx_hands.append(x[mn])
            count+=1 ## para o C 

    return np.array(xx_hands)


def FIR(signal, h):  
    y = np.zeros_like(signal)  # Saída com mesmo tamanho da entrada
    for n in range(len(signal)):
            for k in range(len(h)):
                if(n - k > 0):
                    y[n] += h[k] * signal[n - k]
    return y

#===================================================
# Parametros
#===================================================
f0 = 60 
Nppc = 128 # numero de pontos por ciclo 
Fs = f0*Nppc
Nc = 100 # numero de ciclos 
t = np.arange(Nc*Nppc)/Fs

#===================================================
# Sinal de Teste
#===================================================
f1 = 60

hmax = 50
hmag = 0.1

Fr = 60
SNR = 1000

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
# Protótipo do Filtro Media Movel 
#===================================================
## Nessa parte os coeficientes h foram calculados, agora tem que aplicar no FIR 
# Filtro DFT
N = int(8*Nppc)
h = (1/N)*np.ones(N)

# h = firls(101,[0, 20/(Fs/2), 30/(Fs/2), 1], [1, 1, 0, 0])

freq,H = freqz(h,1,4096) ##  
f = freq*Fs/(2*np.pi) ## rad2deg 
H_mag = abs(H) ## H é magnitude adimensional e fase em radianos

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

M = Fs//f0 # M = Nppc pois Fs = f0*Nppc

for i in range(len(h)):
    if(i % M):
        H = h[i]
H = [h[i::M] for i in range(M)] #h[start:stop:step]

E = np.zeros((M,len(h)//M))

for kk in range(M): 
    
    E[kk,:] = h[kk::M]

#===================================================
# Aplicação dos Filtros
#===================================================

Eout = np.zeros((M,Nc*Nppc//M))  
Eout_fir = np.zeros((M,Nc*Nppc//M))

xx_hands = downsample_1(x,M)

for mm in range(M):
    xx = downsample(x[mm:Nc*Nppc+mm], M)
    Eout[mm,:] = lfilter(E[mm],1,xx_hands[0:100])#(coefs num, coefs den , signal)
    Eout_fir[mm,:] = FIR(xx_hands[0:100],E[mm])
n_teste = np.arange(len(xx))  # Índice das amostras

print("Tamanho do filtro polifasico",Eout_fir.shape, "\n M =",M,"\n Nppc =",Nppc,"\n Nc =",Nc)


plt.figure(figsize=(10, 4))
plt.plot(xx, 'r-', marker='o', label='downsample()')
plt.plot(xx_hands[0:100], 'g--', marker='s', label='downsample_1()')
plt.title('Comparação entre métodos de decimação')
plt.xlabel('Amostra (n)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print(xx_hands,"xx_hands")
print(xx,"xx")






        ### ADEQUAR AO FOR NOVO E ENTÃO USAR O 





plt.figure(figsize=(12, 6))

# Subplot 1: Sinal filtrado com lfilter
plt.subplot(2, 1, 1)
plt.plot(Eout[mm, :], 'b-', label='Filtrado (lfilter)')
plt.title(f'Comparação dos Filtros (Canal {mm})')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Subplot 2: Sinal filtrado com FIR personalizado
plt.subplot(2, 1, 2)
plt.plot(Eout_fir[mm, :], 'r-', label='Filtrado (FIR)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()


#===================================================
# Aplicação da IDFT
#===================================================

v = np.zeros((M,Nc*Nppc//M), dtype=complex)

for nn in range(Nc*Nppc//M):
    v[:,nn] = np.conj(M*np.fft.ifft(Eout[:,nn]))#idftmtx.dot(Eout[:,nn])#
    

#===================================================
# Plot dos Resultados
#===================================================

Xref = np.zeros((hmax,Nc*Nppc//M), dtype=complex)
for hh in range(hmax):
    Xref[hh,:] = downsample(Xr[hh,:Nc*Nppc], M) 

plt.figure()
plt.suptitle('Magnitudes dos Fasores')
for hh in range(1,8):
    plt.subplot(4,2,hh+1)
    plt.plot(abs(v[hh,:])*2/np.sqrt(2), label = 'Estimado %d' %hh)
    plt.plot(abs(Xref[hh-1,:]), label = 'Referência %d' %hh)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.grid()
mplcursors.cursor(hover=True)
plt.show(block = False)


plt.figure()
plt.suptitle('Fase Fasores')
for hh in range(1,8):
    plt.subplot(4,2,hh+1)
    plt.plot(np.unwrap(np.angle(v[hh,:])), label = 'Estimado %d' %hh)
    plt.plot(np.angle(Xref[hh-1,:]), label = 'Referência %d' %hh)
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

erro_mag = np.zeros((hmax,Nc*Nppc//M))
erro_fas = np.zeros((hmax,Nc*Nppc//M))
TVEh = np.zeros((hmax,Nc*Nppc//M))
for hh in range(1,hmax):

    mag = abs(v[hh,:])*2/np.sqrt(2)
    fas = np.unwrap(np.angle(v[hh,:]))
    
    erro_mag[hh-1,:] = mag - abs(Xref[hh-1,:])
    erro_fas[hh-1,:] = (180/np.pi)*(fas - np.angle(Xref[hh-1,:]))

    re,im = pol2cart(mag, fas)
    fasor = re + 1j*im
    
    TVEh[hh-1,:] = TVE(fasor,Xref[hh-1,:])
    

erro_mag = erro_mag[:,M//2:]
erro_fas = erro_fas[:,M//2:]
TVEh = TVEh[:,M//2:]


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