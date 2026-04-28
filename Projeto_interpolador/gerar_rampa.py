import numpy as np
import matplotlib.pyplot as plt
from sinaisIEC60255_118 import frequency_ramp

def downsample(X, factor):
    """Decima o eixo temporal do array X (hmax x N)."""
    if factor <= 0 or not isinstance(factor, int):
        raise ValueError("factor deve ser inteiro positivo")
    return X[..., ::factor]

# ===================================================
# Parâmetros da Rampa
# ===================================================
Rf = 1.0  # Taxa de rampa (norma IEC)
fa = 55.0  # Frequência inicial
f0 = 60.0  # Frequência nominal
Nppc = 256 
Fs = f0 * Nppc  # = 15360 Hz
Frep = 60.0
hmax = 50
hmag = 0.05
SNR = float('inf') # Sem ruído
Nc = 600

N = Nc * Nppc  # Total de amostras

print("="*80)
print("GERAÇÃO DE RAMPA DE FREQUÊNCIA")
print("="*80)
print(f"\nParâmetros:")
print(f"  - Rf (taxa de rampa): {Rf} Hz/s")
print(f"  - fa (frequência inicial): {fa} Hz")
print(f"  - f0 (frequência nominal): {f0} Hz")
print(f"  - Fs (frequência amostragem): {Fs} Hz")
print(f"  - N (amostras totais): {N}")
print(f"  - Duração: {N/Fs:.2f} segundos")

# ===================================================
# 1. Gerar Rampa
# ===================================================
print(f"\n[1/1] Gerando rampa...")

try:
    x, X, f, ROCOF = frequency_ramp(Rf, N, f0, fa, Fs, Frep, hmax, hmag, SNR)
    print(f"  ✓ Rampa gerada:")
    print(f"    - x shape: {x.shape}")
    print(f"    - X shape: {X.shape}")
    print(f"    - f shape: {f.shape}")
    print(f"    - f range: [{np.min(f):.4f}, {np.max(f):.4f}] Hz")
    print(f"    - ROCOF constante: {ROCOF[0]:.4f} Hz/s")
except Exception as e:
    print(f"  ✗ Erro ao gerar rampa: {e}")
    exit(1)

# ===================================================
# 1.5 Visualizar Rampa (ANTES de quantizar)
# ===================================================
print(f"\nGerando visualizações...")

t = np.arange(N) / Fs  # Eixo de tempo

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Rampa de Frequência - Análise do Sinal', fontsize=14, fontweight='bold')

# Subplot 1: Sinal x vs tempo (com decimação para visualizar)
ax = axes[0, 0]
decimacao = 100
ax.plot(t[::decimacao], x[::decimacao], 'b-', linewidth=1, alpha=0.8)
ax.set_xlabel('Tempo (s)', fontweight='bold')
ax.set_ylabel('Amplitude', fontweight='bold')
ax.set_title('Sinal x(t) - Rampa de Frequência (decimado 100x)', fontweight='bold')
ax.grid(True, alpha=0.3)

# Subplot 2: Frequência f vs tempo (mostrando a rampa linear)
ax = axes[0, 1]
ax.plot(t, f, 'r-', linewidth=2, alpha=0.8)
ax.set_xlabel('Tempo (s)', fontweight='bold')
ax.set_ylabel('Frequência (Hz)', fontweight='bold')
ax.set_title('Frequência f(t) - Rampa Linear', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axhline(y=f0, color='green', linestyle='--', linewidth=1, label=f'f0={f0} Hz')
ax.axhline(y=fa, color='orange', linestyle='--', linewidth=1, label=f'fa={fa} Hz')
ax.legend()

# Subplot 3: Magnitude de X[0,:] (fundamental)
ax = axes[1, 0]
X_mag_fund = np.abs(X[0, :])
ax.plot(t, X_mag_fund, 'purple', linewidth=1, alpha=0.8)
ax.set_xlabel('Tempo (s)', fontweight='bold')
ax.set_ylabel('Magnitude', fontweight='bold')
ax.set_title('Magnitude de X[0,:] (Fundamental)', fontweight='bold')
ax.grid(True, alpha=0.3)

# Subplot 4: Espectrograma simplificado (magnitude ao longo do tempo)
ax = axes[1, 1]
X_mag_all = np.abs(X)  # (50, N)
im = ax.imshow(X_mag_all, aspect='auto', origin='lower', cmap='viridis', 
               extent=[t[0], t[-1], 1, hmax])
ax.set_xlabel('Tempo (s)', fontweight='bold')
ax.set_ylabel('Ordem Harmônica', fontweight='bold')
ax.set_title('Espectrograma (Magnitude de X ao longo do tempo)', fontweight='bold')
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Magnitude', fontweight='bold')

plt.tight_layout()
plt.show()

# ===================================================
# Salvar vetor de frequência original
# ===================================================
print(f"\nSalvando dados...")
try:
    np.savetxt('f_rampa_original.txt', f, fmt='%.6e')
    np.savetxt('x_rampa_original.txt', x, fmt='%.6e')
    np.savetxt('ROCOF_rampa.txt', ROCOF, fmt='%.6e')
    print(f"  ✓ Dados salvos:")
    print(f"    - f_rampa_original.txt ({len(f)} amostras)")
    print(f"    - x_rampa_original.txt ({len(x)} amostras)")
    print(f"    - ROCOF_rampa.txt")
except Exception as e:
    print(f"  ✗ Erro ao salvar: {e}")

print(f"  ✓ Visualizações geradas!")

# ===================================================
# 2. Salvar X (matriz complexa)
# ===================================================
print(f"\nSalvando X (matriz complexa)...")

# Dividir em parte real e imaginária
X_real = X.real
X_imag = X.imag

try:
    # Salvar com precisão %.6e (SINAIS INTEIROS)
    np.savetxt('X_rampa_real.txt', X_real, fmt='%.6e')
    np.savetxt('X_rampa_imag.txt', X_imag, fmt='%.6e')
    
    # -----------------------------------------------------------
    # NOVO: GERAR E SALVAR REFERÊNCIAS DECIMADAS APENAS PARA O X
    # -----------------------------------------------------------
    X_ref_real = downsample(X_real, Nppc)
    X_ref_imag = downsample(X_imag, Nppc)
    np.savetxt('X_rampa_real_ref.txt', X_ref_real, fmt='%.6e')
    np.savetxt('X_rampa_imag_ref.txt', X_ref_imag, fmt='%.6e')
    
    # Verificar tamanho dos arquivos
    import os
    tamanho_real = os.path.getsize('X_rampa_real.txt') / (1024**2)
    tamanho_imag = os.path.getsize('X_rampa_imag.txt') / (1024**2)
    tamanho_total = tamanho_real + tamanho_imag
    
    print(f"  ✓ Arquivos X salvos:")
    print(f"    - X_rampa_real.txt ({tamanho_real:.2f} MB)")
    print(f"    - X_rampa_imag.txt ({tamanho_imag:.2f} MB)")
    print(f"    - X_rampa_real_ref.txt (decimado shape: {X_ref_real.shape})")
    print(f"    - X_rampa_imag_ref.txt (decimado shape: {X_ref_imag.shape})")
    print(f"    - Shape X: {X.shape}")
    print(f"    - Total: {tamanho_total:.2f} MB")
    
except Exception as e:
    print(f"  ✗ Erro ao salvar X: {e}")
    exit(1)

# ===================================================
# 3. Salvar f (frequência variável)
# ===================================================
print(f"\nSalvando f (frequência variável)...")

try:
    # Salvar frequência multiplicada por 16384 (quantizada, sem decimais)
    np.savetxt('f_rampa.txt', np.round((f/65) * 2**22), fmt='%d')
    
    tamanho_f = os.path.getsize('f_rampa.txt') / (1024**2)
    
    print(f"  ✓ Arquivo f salvo:")
    print(f"    - f_rampa.txt ({tamanho_f:.4f} MB)")
    print(f"    - Escala: ×16384 (valores variam de {np.min(f*16384.0):.0f} até {np.max(f*16384.0):.0f})")
    
except Exception as e:
    print(f"  ✗ Erro ao salvar f: {e}")
    exit(1)

# ===================================================
# 4. Salvar sinal x também
# ===================================================
print(f"\nSalvando x (sinal no tempo)...")

try:
    # Quantizar para inteiro (×16384 como estava sendo feito)
    x_int = (x * 16384.0).astype(np.int32)
    
    np.savetxt('x_rampa.txt', x_int, fmt='%d')
    
    tamanho_x = os.path.getsize('x_rampa.txt') / (1024**2)
    
    print(f"  ✓ Arquivo x salvo:")
    print(f"    - x_rampa.txt ({tamanho_x:.2f} MB)")
    
except Exception as e:
    print(f"  ✗ Erro ao salvar x: {e}")
    exit(1)

# ===================================================
# 5. Salvar ROCOF também (para completude)
# ===================================================
print(f"\nSalvando ROCOF (taxa de mudança de frequência)...")

try:
    np.savetxt('ROCOF_rampa.txt', ROCOF, fmt='%.4f')
    
    tamanho_rocof = os.path.getsize('ROCOF_rampa.txt') / (1024**2)
    
    print(f"  ✓ Arquivo ROCOF salvo:")
    print(f"    - ROCOF_rampa.txt ({tamanho_rocof:.4f} MB)")
    
except Exception as e:
    print(f"  ✗ Erro ao salvar ROCOF: {e}")
    exit(1)