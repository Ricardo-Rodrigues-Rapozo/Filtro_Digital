"""
Resposta em frequencia (magnitude, em dB) do filtro base flat-top do banco.

O filtro e o que o pipeline usa: `FlatTopFilterBase(8*Nppc + 1)`, com Nppc = 256
amostras por ciclo e Fs = 60 x 256 = 15360 Hz - 2049 coeficientes, janela de
8,0039 ciclos de 60 Hz.

O ponto da figura e a atenuacao na frequencia de dobra da decimacao: o banco
decima por M = Nppc = 256, a saida sai a 60 quadros/s e a dobra fica em
Fs/2M = 30 Hz, onde o filtro atenua apenas 9,6 dB (-3 dB em 22,8 Hz, 1o nulo so
em 45 Hz). Ordem alta nao e o mesmo que banda estreita: a meia-largura do lobo
principal de uma janela de cossenos de Mt termos e Mt*Fs/N = 6 x 7,4963 =
45 Hz, e nao muda se Nppc aumentar (N e Fs crescem juntos).

Saida em C:/Users/Ricardo/Documents/plotsDissertacao:
    PNG a 300 dpi (2700 x 1500 px) para slides e PDF vetorial para o LaTeX.

Uso:
    python plot_dissertacao_flattop.py
"""

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from DSPEPS import FlatTopFilterBase

# ==========================================================================
# Configuracao - identica a do pipeline (plot_dissertacao_offnominal.py)
# ==========================================================================
SAIDA_DIR = Path(r"C:\Users\Ricardo\Documents\plotsDissertacao")
NOME = "fig_flattop_resposta_frequencia"

Nppc = 256
f0 = 60.0
Fs = f0 * Nppc
N = 8 * Nppc + 1          # 2049 coeficientes
M = Nppc                  # decimacao do banco polifasico
F_DOBRA = Fs / (2 * M)    # 30 Hz - Nyquist da taxa de quadros

F_MAX = 200.0             # extensao do eixo pedida
NFFT = 1 << 22            # zero-padding: resolucao Fs/NFFT = 3,7 mHz
DPI = 300                 # figura de 9 x 5 pol -> 2700 x 1500 px

# ==========================================================================
# Estilo: fontes maiores que as das figuras do texto, porque a figura entra em
# slide e sera reduzida na projecao.
# ==========================================================================
plt.rcParams.update({
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "font.size": 14,
    "axes.labelsize": 15,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "axes.grid": True,
    "grid.linestyle": ":",
    "grid.linewidth": 0.8,
    "grid.alpha": 0.5,
    "grid.color": "#9aa0a6",
    "axes.edgecolor": "#5f6368",
    "axes.linewidth": 0.9,
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "axes.axisbelow": True,
    "pdf.fonttype": 42,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

COR_CURVA = "#2a78d6"     # mesmo azul das demais figuras da dissertacao
COR_LIM = "#d03b3b"       # frequencia de dobra da decimacao


# ==========================================================================
# Resposta em frequencia
# ==========================================================================
def resposta(h, f):
    """H(f) avaliada exatamente nas frequencias f (Hz), sem interpolacao.

    A janela e simetrica em torno de n = 0, entao a soma com cosseno ja da a
    resposta de fase zero. Conferida contra scipy.signal.freqz e contra a
    amplitude medida na saida de lfilter para senoides puras - as tres batem
    em 0,01 dB.
    """
    n = np.arange(-(len(h) - 1) / 2, (len(h) - 1) / 2 + 1)
    return (h[None, :] * np.cos(2 * np.pi * np.outer(np.atleast_1d(f), n) / Fs)).sum(1)


def varredura(h):
    """Curva densa de 0 a F_MAX via DFT com zero-padding.

    Amostrar a DTFT pela FFT de h com zeros a direita e exato nos pontos
    k*Fs/NFFT - o deslocamento no tempo so afeta a fase, e aqui so a magnitude
    e usada. Evita a matriz densa que a avaliacao direta exigiria.
    """
    H = np.fft.rfft(h, NFFT)
    f = np.arange(len(H)) * Fs / NFFT
    m = f <= F_MAX
    return f[m], 20 * np.log10(np.maximum(np.abs(H[m]), 1e-300))


def main():
    h = FlatTopFilterBase(N)
    f, AdB = varredura(h)
    A_dobra = 20 * np.log10(np.abs(resposta(h, F_DOBRA)[0]))

    print(f"N = {N} coeficientes, Fs = {Fs:.0f} Hz, janela = {N/Nppc:.4f} ciclos")
    print(f"decimacao M = {M}, taxa de quadros = {Fs/M:.0f} Hz, dobra em {F_DOBRA:.0f} Hz")
    print(f"-3 dB em {f[np.argmin(np.abs(AdB + 3))]:.2f} Hz; 1o nulo em {6*Fs/N:.2f} Hz")
    print(f"|H({F_DOBRA:.0f} Hz)| = {A_dobra:.2f} dB")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(f, AdB, color=COR_CURVA, lw=1.8, zorder=3)

    # Frequencia de dobra da decimacao, com a atenuacao em destaque.
    ax.axvline(F_DOBRA, color=COR_LIM, lw=1.6, ls=(0, (5, 2)), zorder=2)
    ax.plot([F_DOBRA], [A_dobra], "o", ms=9, color=COR_LIM, zorder=5,
            markeredgecolor="white", markeredgewidth=1.2)
    rotulo = f"{F_DOBRA:.0f} Hz: {A_dobra:.1f} dB"
    ax.annotate(rotulo.replace(".", ",").replace("-", "\u2212"),
                xy=(F_DOBRA, A_dobra), xytext=(14, -6),
                textcoords="offset points", fontsize=15, color=COR_LIM,
                fontweight="bold", zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor="none", alpha=0.9))

    ax.set_xlim(0, F_MAX)
    ax.set_xticks(np.arange(0, F_MAX + 1, 20))
    ax.set_ylim(-210, 20)
    ax.set_yticks(np.arange(-200, 1, 40))
    ax.set_xlabel("Frequência (Hz)")
    ax.set_ylabel("$|H(f)|$ (dB)")

    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    for ext in (".png", ".pdf"):
        try:
            fig.savefig(SAIDA_DIR / (NOME + ext), dpi=DPI)
            print(f"  gravado: {SAIDA_DIR / (NOME + ext)}")
        except PermissionError:
            print(f"  NAO gravado (arquivo em uso): {SAIDA_DIR / (NOME + ext)}")
    plt.close(fig)


if __name__ == "__main__":
    main()
