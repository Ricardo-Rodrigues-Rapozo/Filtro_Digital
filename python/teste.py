import numpy as np

x = np.arange(100)

M = 5

h = 0.1*np.ones(20)

T = (len(h) // M)

Nf = int(np.ceil(len(h)/M))

Ehh = np.zeros((M, Nf))

for kk in range(M):
    hh = np.array(h[kk::M])          # transforma em numpy array
    hh_padded = np.pad(hh, (0, Nf - len(hh)), 'constant')  # completa com zeros à direita
    Ehh[kk, :] = hh_padded

buffer= np.zeros(M)

E = np.zeros((M,len(h)//M))

E0 = np.zeros((M,4))

for nn in range(len(x)):
    
    for kk in range(M):
        buffer[M-1-kk] = buffer[M-2-kk] 
    buffer[0] = x[nn]

    for mm in range(M):

        for n in range(len(h) // M):

            if mm == 0 and n == T - 1:
                 E[mm,1] = E[mm,0]
            if mm != 0 and n == T- 1:
                E[mm,0] = E[mm - 1, T - 1]
            else:
                E[mm, T - 1 - n] = E[mm, T - n - 2]
            n = n + 1        
        E[0,0] = buffer[mm]
        E0[mm, :] = Ehh[mm, :] * E[mm, :]
        mm = mm + 1
        #         
#   v = np.fft.ifft(E0)


