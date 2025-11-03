from pathlib import Path
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
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

##------------------------------------------------------------------------------------------------------
## ---------------------------------- coeficientes -------------------------------------------------------
##------------------------------------------------------------------------------------------------------
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

##------------------------------------------------------------------------------------------------------
## ---------------------------------- Caminhos para sinal de entrada -----------------------------------
##------------------------------------------------------------------------------------------------------
dir_base = Path(r"C:\Users\Ricardo\Documents\Dissertação\procTest_00\Simulation")
dir_base2 = Path(r"C:\Users\Ricardo\Documents\Dissertação\python")
arq1 = dir_base / "input_0.txt"
x1 = ler_coluna(arq1, col=0) ## entrada multiplicada por 1000

plt.figure()
plt.plot(x1)
plt.show()
##------------------------------------------------------------------------------------------------------
## ---------------------------------- PARAMETROS -------------------------------------------------------
##------------------------------------------------------------------------------------------------------
Q = 0.001 #; // Fator de decimação
M = 5 #; // Decimação e numero e numero de fases
L = len(h) #; // Tamanho do filtro
buffer_circular = np.zeros(int(np.ceil((M * L)/M))) #; // Buffer circular 
tamanho_buffer_circular = len(buffer_circular) #; // Tamanho do buffer circular

contador_IDFT = 0 #; // Contador de IDFTs realizadas
contador_posicao_buffer_circular = 0 #; // Cabeça do buffer circular
contador_tempo_real = 0 #; // Tempo real (índice de leitura do sinal de entrada)
contador_amostra_subfiltro_Exx = 0 #; // Contador de amostras do subfiltro
contador_posicao_buffer_taps = 0 #; // Contador de posição do buffer de taps
contador_taps = 0 #; // Contador de taps do subfiltro
m = 0 #; // Contador de fases do subfiltro
n = 0 #; // Contador de taps do subfiltro
cont_n = 0 #; // Contador auxiliar
P = int(np.ceil(L / M))
Exx = np.zeros((M, P))#; //  (// divisao inteira)Matriz que armazena as fases do filtro polifásico
y = np.zeros(M) ## Matriz de saida filtrada
yy = np.zeros((M, len(x1) // M)) ## Sinal de saída final
##------------------------------------------------------------------------------------------------------
## ---------------------------------- Funções -------------------------------------------------------
##------------------------------------------------------------------------------------------------------

def downsampling(a,b): 
    '''
    Função que verifica se a é multiplo de b
    '''
    if(a % b == 0):
        return b
    return 0

#FASES DO FILTRO
def matriz_coeficientes(h, M):      
    m = 0
    c = 0   
    L = len(h) 
    P = int(np.ceil(L / M)) 
    Ehh = np.zeros((M,P))#; //  (// divisao inteira)Matriz que armazena as fases do filtro polifásico
    while(m < M):
        c = 0
        while(c < P):
            r = m + c * M
            Ehh[m, c] = h[r] if r < L else 0.0
            c = c + 1
        m = m + 1
        
    return Ehh
    
Enn = matriz_coeficientes(h, M)

##------ Loop principal --------------
while(contador_tempo_real < len(x1)):
    # Se amostra for multiplo de M, armazena no buffer circular
    if(downsampling(contador_tempo_real, M)):
        # Armazena no buffer circular a amostra atual 
        buffer_circular[contador_posicao_buffer_circular] = x1[contador_tempo_real] * Q
        Pb = 0 ## Varre o buffer circular 
        m = 0 # Varre as fases da matriz de subfiltros 

        n = 0 # Varre os taps da matriz de subfiltros 
        while(m < M):
            while(n < P):    
                Exx[m,n] = buffer_circular[Pb]
                ##Logica do filtro abaixo  
                y[m] += Exx[m,n] * Enn[m,n]
                # Faz IDFT
                n = n + 1
                Pb = Pb + 1
            
            m = m + 1
            n = 0
        yy[:,contador_IDFT] = np.fft.ifft(y[:])
        y[:] = 0 ### zera o y para proxima fase 
        # Contadores 
        contador_IDFT = contador_IDFT + 1
        contador_posicao_buffer_circular = (contador_posicao_buffer_circular + 1) % tamanho_buffer_circular

        # Incrementa contador do subfiltro apenas quando a cabeça do buffer circular voltar para 0
        if(contador_posicao_buffer_circular == 0):
            contador_amostra_subfiltro_Exx = (contador_amostra_subfiltro_Exx + 1) % P



    contador_tempo_real = contador_tempo_real + 1

# Sinal de saída final
# plt.figure()
# plt.plot(yy[0,:])
# plt.plot(yy[1,:])
# plt.plot(yy[2,:])
# plt.plot(yy[3,:])
# plt.plot(yy[4,:])
# plt.show()
for i in range(contador_IDFT):
    plt.plot(abs(yy[:,i])*2/np.sqrt(2), label = 'Estimado %d' %i)
plt.show()


plt.figure()
plt.suptitle('Fase Fasores')
for hh in range(1200):
    plt.plot(np.unwrap(np.angle(yy[:,hh])), label = 'Estimado %d' %hh)
    #plt.plot(np.angle(Xref[hh-1,:]), label = 'Referência %d' %hh)
    # plt.ylim(-np.pi-1, np.pi+1)
    # plt.xlabel('Tempo (s)')
    # plt.ylabel('Fases (rad)')
    # plt.legend()
    # plt.grid()
#mplcursors.cursor(hover=True)
plt.show()

### Tarefa: Entender como funciona a IDFT do python para aplicar direito aqui

print(len(x1), "Numero de saidas que o meu vetor deve ter: ,",len(x1)/M)
print(yy.shape)