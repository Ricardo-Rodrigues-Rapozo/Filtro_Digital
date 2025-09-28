def fsinal(ncilos: int, FS: float, N: int) -> float:
    """
    Calcula a frequência fundamental de um sinal senoidal.

    A função relaciona o número de ciclos da senoide, a frequência de amostragem
    e o número total de amostras, retornando a frequência fundamental obtida.

    Parâmetros
    ----------
    ncilos : int
        Número de ciclos da senoide no sinal.
    FS : float
        Frequência de amostragem (Hz).
    N : int
        Número total de amostras no sinal.

    Retorna
    -------
    float
        Frequência fundamental do sinal (Hz).
    """
    f = ncilos * FS / N
    return f


# -------------------------------
# Configuração para simulação em Python
# -------------------------------
ncilos_python = 100   # número de ciclos da senoide
FS_python = 3600      # frequência de amostragem (Hz)
N_python = 6000       # número de amostras

# -------------------------------
# Configuração para simulação em C
# -------------------------------
frequencia_fundamental = 60        # Hz
Fs_c = 50000                      # Hz (50 kHz)
tempo_total_simu = 5_000e-6        # segundos (5 ms)

N = int(tempo_total_simu * Fs_c)   # número de amostras
n_ciclos = frequencia_fundamental * tempo_total_simu
ncilos_c = frequencia_fundamental * Fs_c / N
N_c = ncilos_c * Fs_c / frequencia_fundamental


# -------------------------------
# Impressão dos resultados
# -------------------------------
print("===== Simulação em Python =====")
print(f"Número de ciclos:              {ncilos_python}")
print(f"Frequência de amostragem (Hz): {FS_python}")
print(f"Número de amostras:            {N_python}")
print(f"Frequência fundamental (Hz):   {fsinal(ncilos_python, FS_python, N_python):.2f}")
print()

print("===== Simulação em C =====")
print(f"Frequência fundamental desejada (Hz): {frequencia_fundamental}")
print(f"Frequência de amostragem (Hz):        {Fs_c}")
print(f"Tempo total de simulação (s):         {tempo_total_simu}")
print(f"Número total de amostras:             {N}")
print(f"Número de ciclos (estimado):          {n_ciclos}")
print(f"ncilos_c (ajuste):                     {ncilos_c}")
print(f"N_c (amostras calculadas):            {N_c}")
print(f"Frequência fundamental obtida (Hz):   {fsinal(ncilos_c, Fs_c, N_c):.2f}")
