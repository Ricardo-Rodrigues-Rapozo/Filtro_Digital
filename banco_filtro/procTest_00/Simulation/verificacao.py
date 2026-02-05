import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

#Nppc = 128

# ===================================================
# Basic Parameters
# ===================================================

f0 = 60
Nppc = 256
Fs = f0 * Nppc
Ts = 1/Fs
Nc = 10  # Numero de ciclos da senoide fundamental
t = np.arange(Nc*Nppc)*Ts

x = np.cos(2*np.pi* f0 * t) + 0.5*np.cos(2*np.pi* 3*f0 * t) + 0.5*np.cos(2*np.pi*5*f0 * t)


np.savetxt('input_0.txt', x*(2**14), fmt='%d')

# ===================================================
# Leitura dados SAPHO
# ===================================================

# x = np.loadtxt('input_0.txt')/32768.0

plt.figure()
plt.plot(x)     
plt.title('Input Signal')
plt.show(block=False)

v1r = np.loadtxt('output_1.txt')/1000000
v1i = np.loadtxt('output_2.txt')/1000000   

v3r = np.loadtxt('output_3.txt')/1000000
v3i = np.loadtxt('output_4.txt')/1000000

v5r = np.loadtxt('output_5.txt')/1000000
v5i = np.loadtxt('output_6.txt')/1000000

# v7r = np.loadtxt('output_7.txt')/10000000 
# v7i = np.loadtxt('output_8.txt')/10000000 

# ===================================================
# Base Filter   MEDIA MOVEL 
# ===================================================
# N = 4*Nppc
# h = (1/N)*np.ones(N)

# M = 128

# Nf = int(np.ceil(len(h)/M))
# Ehh = np.zeros((M, Nf))

# for kk in range(M):
#     hh = np.array(h[kk::M])          # transforma em numpy array
#     hh_padded = np.pad(hh, (0, Nf - len(hh)), 'constant')  # completa com zeros à direita
#     Ehh[kk, :] = hh_padded



# ========================================================
# Base Filter
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
# SAVA salva Ehh em formato coluna
# ===================================================
Ehh = Ehh.astype(np.float64)
Ehh_col = Ehh.reshape(-1, order="C")     # row-major
np.savetxt("Ehh_flat.txt", Ehh_col, fmt="%.18e", newline="\n")

# ===================================================
# Polyphase Implementation
# ===================================================
buffer= np.zeros(M)
E = np.zeros((M, Nf))
E0 = np.zeros(M)
v = np.zeros((M,len(x)//M), dtype=complex)
jj = 0

for nn in range(len(x)):
    for kk in range(M-1):
        buffer[M-1-kk] = buffer[M-2-kk] 
    buffer[0] = x[nn]
    
    if((nn % M) == 0):
        for mm in range(M):
            for kk in range(Nf -1, 0, -1):
                E[mm,kk] = E[mm,kk-1]        
            E[mm,0] = buffer[mm]
            E0[mm] =  np.dot(Ehh[mm,:],E[mm,:])
        
        vv = M*np.fft.ifft(E0)
        v[:,jj] = vv
        jj += 1

plt.figure()
plt.subplot(4,2,1)
plt.plot(v1r, label='SAPHO Real', marker='o', linestyle='-')
plt.plot(v[1,:].real, label='Polyphase Real', marker='o', linestyle='--')
plt.title('Output 1 Real')
plt.legend()
plt.subplot(4,2,2)
plt.plot(v1i, label='SAPHO Imag', marker='o', linestyle='-')       
plt.plot(v[1,:].imag, label='Polyphase Imag', marker='o', linestyle='--')
plt.title('Output 1 Imag')
plt.legend()

plt.subplot(4,2,3)
plt.plot(v3r, label='SAPHO Real', marker='o', linestyle='-')
plt.plot(v[3,:].real, label='Polyphase Real', marker='o', linestyle='--')
plt.title('Output 3 Real')
plt.legend()
plt.subplot(4,2,4)
plt.plot(v3i, label='SAPHO Imag', marker='o', linestyle='-')       
plt.plot(v[3,:].imag, label='Polyphase Imag', marker='o', linestyle='--')
plt.title('Output 3 Imag')
plt.legend()

plt.subplot(4,2,5)
plt.plot(v5r, label='SAPHO Real', marker='o', linestyle='-')
plt.plot(v[5,:].real, label='Polyphase Real', marker='o', linestyle='--')
plt.title('Output 5 Real')
plt.legend()
plt.subplot(4,2,6)
plt.plot(v5i, label='SAPHO Imag', marker='o', linestyle='-')       
plt.plot(v[5,:].imag, label='Polyphase Imag', marker='o', linestyle='--')
plt.title('Output 5 Imag')
plt.legend()


# plt.subplot(4,2,7)
# plt.plot(v7r, label='SAPHO Real', marker='o', linestyle='-')
# plt.plot(v[7,:].real, '--', label='Polyphase Real', marker='o', linestyle='-')
# plt.title('Output 7 Real')
# plt.legend()
# plt.subplot(4,2,8)
# plt.plot(v7i, label='SAPHO Imag', marker='o', linestyle='-')       
# plt.plot(v[7,:].imag, '--', label='Polyphase Imag', marker='o', linestyle='-')
# plt.title('Output 7 Imag')
# plt.legend()
# mplcursors.cursor(hover=True)

plt.show(block=False)


v1abs = np.sqrt(v1r**2 + v1i**2)
v_poly1abs = np.sqrt(v[1,:].real**2 + v[1,:].imag**2)

v3abs = np.sqrt(v3r**2 + v3i**2)
v_poly3abs = np.sqrt(v[3,:].real**2 + v[3,:].imag**2)

v5abs = np.sqrt(v5r**2 + v5i**2)
v_poly5abs = np.sqrt(v[5,:].real**2 + v[5,:].imag**2)

# v7abs = np.sqrt(v7r**2 + v7i**2)
# v_poly7abs = np.sqrt(v[7,:].real**2 + v[7,:].imag**2)

plt.figure()
plt.subplot(2,2,1)  
plt.plot(v1abs, label='SAPHO Abs', marker='o', linestyle='-')
plt.plot(v_poly1abs, label='Polyphase Abs', marker='o', linestyle='--')
plt.title('Output 1 Abs')
plt.legend()
plt.subplot(2,2,2)  
plt.plot(v3abs, label='SAPHO Abs', marker='o', linestyle='-')
plt.plot(v_poly3abs, label='Polyphase Abs', marker='o', linestyle='--')
plt.title('Output 3 Abs')
plt.legend()
plt.subplot(2,2,3)  
plt.plot(v5abs, label='SAPHO Abs', marker='o', linestyle='-')
plt.plot(v_poly5abs, label='Polyphase Abs', marker='o', linestyle='--')
plt.title('Output 5 Abs')
plt.legend()
plt.subplot(2,2,4)  
# plt.plot(v7abs, label='SAPHO Abs', marker='o', linestyle='-')
# plt.plot(v_poly7abs, '--', label='Polyphase Abs', marker='o',   linestyle='-')
# plt.title('Output 7 Abs')
# plt.legend()
# mplcursors.cursor(hover=True)
plt.show()




