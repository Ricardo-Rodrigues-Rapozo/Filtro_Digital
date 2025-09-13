import numpy as np 

def FIR(signal, h,M,Nc,Nppc):
      # Saída com mesmo tamanho da entrada
    y = np.zeros_like(signal)
    for n in range(len(signal)):
            for k in range(len(h)):
                if n - k >= 0:  # Evita índices negativos
                    y[n] += h[k] * signal[n - k]
    return y


def dowsample(x,M): 
  
  """
  Objetivo: aplicar a formula y[n] = [n*M] 
  x : sinal usado 
  M : valor para decimação 
  return : array do sinal decimado 

  """
  xx_hands = list()
  for mm in range(len(x)): # novo sinal vai ter tamanho igual a len(x)/M
    if( mm % M == 0): ## para saber se o resto da divisão é igual a 0 e nesse caso é multiplo 
      xx_hands.append(x[mm])
  return np.array(xx_hands)
            
