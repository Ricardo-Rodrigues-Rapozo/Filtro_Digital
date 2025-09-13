import numpy as np
from scipy.signal import freqz, lfilter, firls, upfirdn
import matplotlib.pyplot as plt
import mplcursors
import sinaisIEC60255_118
from scipy.signal import firwin
import numpy as np
from pathlib import Path



def salvar_uma_coluna(caminho_txt: str | Path, x: np.ndarray, fmt: str = "%.10f") -> Path:
    caminho = Path(caminho_txt)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    x_mag = (x)                   # magnitude
    np.savetxt(caminho, x_mag, fmt=fmt, comments="")
    return caminho



#===================================================
# Parametros
#===================================================
f0 = 60 
Nppc = 60 # numero de pontos por ciclo 
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

#===================================================
# Quantização
#===================================================
Q = 1000


#===================================================
# Sinal de Teste
#===================================================



x,Xr,f1r,ROCOFr = sinaisIEC60255_118.signal_frequency(f1, (Nc+1)*Nppc, f0, Fs, Fr, hmax, hmag, SNR)
x = x[:Nc*Nppc] 
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
plt.show(block = True)

#===================================================
# Filtro FIR (ordem 10) - LOWPASS
#===================================================
order = 10
numtaps = order + 1
fc = 80.0  # Hz (ajuste conforme desejado)
h = firwin(numtaps=numtaps, cutoff=fc, fs=Fs, window='hamming', pass_zero='lowpass')
print(h)
# resposta ao impulso (opcional)
w, H = freqz(h, worN=2048, fs=Fs)
plt.figure()
plt.plot(w, 20*np.log10(np.maximum(np.abs(H), 1e-12)))
plt.grid(True); plt.xlabel('Frequência (Hz)'); plt.ylabel('Magnitude (dB)')
plt.title('FIR Lowpass (ordem 10)')
plt.show(block=True)

# aplicar o filtro
y = lfilter(h, 1.0, x)
plt.figure()
plt.plot(t, y[:Nc*Nppc])
plt.grid(); plt.xlabel('Tempo (s)'); plt.ylabel('Magnitude'); plt.title('Sinal Filtrado (FIR Lowpass)')
mplcursors.cursor(hover=True)
plt.show(block=True)
#print(x.shape, Nc*Nppc)

caminho_saida = r"C:\Users\Ricardo\Documents\Codigos_C\primeiro\procTest_00\Simulation\input_0.txt"   # ajuste o caminho
arquivo = salvar_uma_coluna(caminho_saida, Q*x[:Nc*Nppc], fmt="%d")
print(f"OK! Arquivo salvo em: {arquivo}")