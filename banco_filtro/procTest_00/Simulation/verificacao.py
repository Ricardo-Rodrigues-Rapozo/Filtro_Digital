import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# ===================================================
#            Basic Parameters of the signal 
# ===================================================

f0 = 60
Nppc = 256
Fs = f0 * Nppc
Ts = 1/Fs
Ganho_saida_sapho = 1000000    ## ganho usado inicialmente 1000000
Ganho_saida_interpolador = 10000
#Nc = 60
#t = np.arange(Nc * Nppc) * Ts
#x = np.cos(2*np.pi* f0 * t) + 0.5*np.cos(2*np.pi* 3*f0 * t) + 0.5*np.cos(2*np.pi*5*f0 * t)
#


# ===================================================
#               Leitura dados de arquivo txt
# ===================================================

x = np.loadtxt('59Hz.txt')
Nc = len(x) // Nppc
t = np.arange(len(x)) * Ts

np.savetxt('input_0.txt', x, fmt='%d')

x = x/ Ganho_saida_interpolador 

print(Nc)
print(f"Tamanho de x: {len(x)}")
print(f"Tamanho esperado: {Nc*Nppc}")


v1r = np.loadtxt('output_1.txt') / Ganho_saida_sapho
v1i = np.loadtxt('output_2.txt') / Ganho_saida_sapho   

v3r = np.loadtxt('output_3.txt') / Ganho_saida_sapho
v3i = np.loadtxt('output_4.txt') / Ganho_saida_sapho

v5r = np.loadtxt('output_5.txt') / Ganho_saida_sapho
v5i = np.loadtxt('output_6.txt') / Ganho_saida_sapho


# ========================================================
#                   Base Filter flat top 
#=========================================================
M = 256

c5 = [1.0005967, 1.9991048, 1.9097925, 1.4448987, 0.66403725, 0.1304229]

N = 8 * (Fs//f0)

n1 = np.arange(-(N - 1) / 2, 1 + (N - 1) / 2, 1)

wM = np.zeros(N)

for m in range(len(c5)):
    wM = wM + c5[m] * np.cos(m * (2 * np.pi / N) * n1)

wM = wM / np.sum(wM)   ## Normaliza

h = wM

Nf = int(np.ceil(len(h)/M))  # aqui esta arredondando para cima 5 ao inves de 4
Ehh = np.zeros((M, Nf))

for kk in range(M):
    hh = np.array(h[kk::M])          # transforma em numpy array
    hh_padded = np.pad(hh, (0, Nf - len(hh)), 'constant')  # completa com zeros à direita
    Ehh[kk, :] = hh_padded



# ===================================================
#             Salva Ehh em formato coluna
# ===================================================
Ehh = Ehh.astype(np.float64)
Ehh_col = Ehh.reshape(-1, order="C")     # row-major
np.savetxt("Ehh_flat.txt", Ehh_col, fmt="%.18e", newline="\n")

# ===================================================
#                   Polyphase Implementation
# ===================================================
buffer= np.zeros(M)
E = np.zeros((M, Nf))
E0 = np.zeros(M)
v = np.zeros((M, (len(x)//M) + 1), dtype=complex)
jj = 0

for nn in range(len(x)):
    for kk in range(M-1):
        buffer[M-1-kk] = buffer[M-2-kk] 
    buffer[0] = x[nn]
    
    #if((nn % M) == 0):
    if (nn % M) == 0:
        for mm in range(M):
            for kk in range(Nf -1, 0, -1):
                E[mm,kk] = E[mm,kk-1]        
            E[mm,0] = buffer[mm]
            E0[mm] =  np.dot(Ehh[mm,:],E[mm,:])
        
        vv = M*np.fft.ifft(E0)
        v[:,jj] = vv
        jj += 1


# ============================================================== #
#            Resposta em frequencia do filtro flat top           #
# ============================================================== #

H = np.fft.rfft(h, 16384)   # uso mais pontos para ficar suave
fh = np.fft.rfftfreq(16384, d=1/Fs)

plt.figure()
plt.plot(fh, np.abs(H))
plt.title("FFT do filtro")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()
# ============================================================== #
#            Resposta em frequencia do sinal                     #
# ============================================================== #
X = np.fft.rfft(x)
f = np.fft.rfftfreq(len(x), d=1/Fs)

plt.figure()
plt.plot(f, np.abs(X))
plt.title("FFT do sinal")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()


# ============================================================== #
#            Sinal                                               #
# ============================================================== #

plt.figure()
plt.plot(t,x)     
plt.title('Input Signal')
plt.show(block=False)

# ============================================================== #
#        Comparison Between SAPHO and Polyphase Outputs          #
# ============================================================== #
# This section compares the real and imaginary components of the
# harmonic estimates obtained from SAPHO with those produced by
# the implemented polyphase filter bank.
#
# Harmonics analyzed:
#   - Fundamental (1st)
#   - 3rd harmonic
#   - 5th harmonic
#
# The goal is to visually validate the equivalence between both
# implementations in terms of magnitude and phase behavior.
# ============================================================== #

plt.figure()

# ============================================================== #
#                      Fundamental                               #
# ============================================================== #

plt.subplot(4,2,1)
plt.plot(v1r, label='SAPHO Real', marker='o', linestyle='-')
plt.plot(v[1,:].real, label='Polyphase Real', marker='o', linestyle='--')
plt.title('Fundamental - Real Component')
plt.legend()

plt.subplot(4,2,2)
plt.plot(v1i, label='SAPHO Imag', marker='o', linestyle='-')       
plt.plot(v[1,:].imag, label='Polyphase Imag', marker='o', linestyle='--')
plt.title('Fundamental - Imaginary Component')
plt.legend()


# ============================================================== #
#                            3rd Harmonic                        #
# ============================================================== #

plt.subplot(4,2,3)
plt.plot(v3r, label='SAPHO Real', marker='o', linestyle='-')
plt.plot(v[3,:].real, label='Polyphase Real', marker='o', linestyle='--')
plt.title('3rd Harmonic - Real Component')
plt.legend()

plt.subplot(4,2,4)
plt.plot(v3i, label='SAPHO Imag', marker='o', linestyle='-')       
plt.plot(v[3,:].imag, label='Polyphase Imag', marker='o', linestyle='--')
plt.title('3rd Harmonic - Imaginary Component')
plt.legend()

# ============================================================== #
#                         5th Harmonic                           #
# ============================================================== #


plt.subplot(4,2,5)
plt.plot(v5r, label='SAPHO Real', marker='o', linestyle='-')
plt.plot(v[5,:].real, label='Polyphase Real', marker='o', linestyle='--')
plt.title('5th Harmonic - Real Component')
plt.legend()

plt.subplot(4,2,6)
plt.plot(v5i, label='SAPHO Imag', marker='o', linestyle='-')       
plt.plot(v[5,:].imag, label='Polyphase Imag', marker='o', linestyle='--')
plt.title('5th Harmonic - Imaginary Component')
plt.legend()

plt.show(block=False)


# ============================================================== #
#        Magnitude Comparison (Vector Norm)                       #
# ============================================================== #
# The magnitude of each harmonic is computed using the Euclidean
# norm:
#
#        |V| = sqrt(Real² + Imag²)
#
# This allows a direct comparison of harmonic amplitudes between
# SAPHO and the polyphase structure.
# ============================================================== #

v1abs = np.sqrt(v1r**2 + v1i**2)
v_poly1abs = np.sqrt(v[1,:].real**2 + v[1,:].imag**2)

v3abs = np.sqrt(v3r**2 + v3i**2)
v_poly3abs = np.sqrt(v[3,:].real**2 + v[3,:].imag**2)

v5abs = np.sqrt(v5r**2 + v5i**2)
v_poly5abs = np.sqrt(v[5,:].real**2 + v[5,:].imag**2)

plt.figure()

# ============================================================== #
#                      Fundamental                               #
# ============================================================== #

plt.subplot(2,2,1)  
plt.plot(v1abs, label='SAPHO Abs', marker='o', linestyle='-')
plt.plot(v_poly1abs, label='Polyphase Abs', marker='o', linestyle='--')
plt.title('Fundamental Magnitude')
plt.legend()

# ============================================================== #
#                            3rd Harmonic                        #
# ============================================================== #

plt.subplot(2,2,2)  
plt.plot(v3abs, label='SAPHO Abs', marker='o', linestyle='-')
plt.plot(v_poly3abs, label='Polyphase Abs', marker='o', linestyle='--')
plt.title('3rd Harmonic Magnitude')
plt.legend()

# ============================================================== #
#                         5th Harmonic                           #
# ============================================================== #

plt.subplot(2,2,3)  
plt.plot(v5abs, label='SAPHO Abs', marker='o', linestyle='-')
plt.plot(v_poly5abs, label='Polyphase Abs', marker='o', linestyle='--')
plt.title('5th Harmonic Magnitude')
plt.legend()

plt.show()


