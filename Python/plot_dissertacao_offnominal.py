"""
Figuras de desempenho do estimador off-nominal (IEC/IEEE 60255-118-1) para o
capitulo de resultados da dissertacao.

A campanha off-nominal esta inteiramente no historico do git: um commit por
frequencia, cada um sobrescrevendo os mesmos arquivos em Aurora/dados_simulacao/.
Este script le esses dados via `git show <sha>:<caminho>`, que NAO toca a arvore
de trabalho (que hoje contem os dados nao commitados de um teste de rampa).

Saida: PDFs vetoriais em C:\\Users\\Ricardo\\Documents\\plotsDissertacao

Uso:
    python plot_dissertacao_offnominal.py            # usa cache quando existir
    python plot_dissertacao_offnominal.py --recalc   # ignora o cache
"""

import io
import subprocess
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.signal import lfilter

from DSPEPS import (BSplineInterp, FlatTopFilterBase, PolyphaseFilterBank,
                    downsample, estima_f_zc, kf_trend_poly)
from sinaisIEC60255_118 import signal_frequency
from auxiliares import TVE, wrap_to_pi

# ==========================================================================
# Configuracao
# ==========================================================================
BASE_DIR = Path(__file__).resolve().parents[1]          # repositorio Dissertacao
CACHE_DIR = Path(__file__).resolve().parent / "cache_offnominal"
SAIDA_DIR = Path(r"C:\Users\Ricardo\Documents\plotsDissertacao")

# Um commit por ensaio off-nominal. 60 Hz nao foi ensaiado (e a nominal).
COMMITS = {
    55: "00942a9", 56: "a83fded", 57: "2248789", 58: "8a1b100", 59: "9e4293b",
    61: "b76ecc7", 62: "0a6ccaf", 63: "d8970a2", 64: "e28c346", 65: "b2afa4c",
}

# Parametros do ensaio (identicos aos do commit 00942a9)
Nppc = 256
f0 = 60.0
Fs = f0 * Nppc
Ts = 1 / Fs
Frep = 60.0
hmax = 50
hmag = 0.05
SNR = 1e18
N_AMOSTRAS = 1600 * Nppc
Q_KALMAN = 1e-1
R_KALMAN = 20
MBSP = 5

# Os ensaios tem de 291 a 317 frames; as estatisticas usam a mesma janela para
# que a comparacao entre frequencias seja justa.
N_COMUM = 280

TVE_LIM = 1.0  # limite IEC/IEEE 60255-118-1, em %

# A 2a harmonica nao existe no sinal de teste: em sinaisIEC60255_118.py o laco de
# sintese e `for hh in range(3, hmax+1)`, entao Xr[1,:] fica exatamente 0+0j e
# TVE/erro de magnitude em h=2 sao divisao por zero. h=2 e omitida em tudo.
H_VALIDAS = np.array([1] + list(range(3, hmax + 1)))
IDX_VALIDAS = H_VALIDAS - 1

# ==========================================================================
# Estilo: figuras para LaTeX (ABNT). Sem titulo interno - a legenda e do LaTeX.
# ==========================================================================
plt.rcParams.update({
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8.5,
    "axes.grid": True,
    "grid.linestyle": ":",
    "grid.linewidth": 0.6,
    "grid.alpha": 0.45,
    "grid.color": "#9aa0a6",
    "axes.edgecolor": "#5f6368",
    "axes.linewidth": 0.7,
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "axes.axisbelow": True,
    "legend.frameon": False,
    "pdf.fonttype": 42,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

# Cores herdadas de teste_python.py, para coerencia com o resto do trabalho
COR_PY = "#2a78d6"
COR_SAPHO = "#eb6834"
COR_LIM = "#d03b3b"
COR_TINTA = "#202124"
COR_BANDA = "#b0b4b8"

# f1 e ordinal e centrada na nominal: mapa divergente com escuridao = distancia
# de 60 Hz. Azul = sub-nominal, vermelho = super-nominal, sem matiz no centro
# (60 Hz nao foi ensaiada, o "meio neutro" e a propria lacuna).
COR_FREQ = {
    55: "#08306b", 56: "#08519c", 57: "#2171b5", 58: "#4292c6", 59: "#6baed6",
    61: "#fc8d72", 62: "#fb6a4a", 63: "#ef3b2c", 64: "#cb181d", 65: "#7f0000",
}


# ==========================================================================
# Leitura dos dados do SAPHO a partir do historico do git
# ==========================================================================
def _git_show(sha, nome):
    """Le um arquivo de dados de um commit sem tocar na arvore de trabalho."""
    caminho = f"{sha}:Aurora/dados_simulacao/{nome}"
    res = subprocess.run(["git", "show", caminho], cwd=BASE_DIR,
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git show {caminho} falhou: {res.stderr.strip()}")
    return np.loadtxt(io.StringIO(res.stdout), dtype=float)


def ler_banco(sha):
    """Desempacota saida_banco0.txt: frames de 103 valores, escala 1e6.

    Layout de um frame: [freq | Re{X0} Im{X0} ... Re{X50} Im{X50}].
    A frequencia sai do interpolador como (f - 60) + 10, dai o +50.
    """
    bruto = np.atleast_1d(_git_show(sha, "saida_banco0.txt"))
    bruto = bruto[1:]  # 1a linha e o zero de reset

    fasores_por_frame = hmax + 1
    amostras_por_frame = 1 + 2 * fasores_por_frame

    n_frames = len(bruto) // amostras_por_frame
    frames = bruto[:n_frames * amostras_por_frame].reshape(n_frames, amostras_por_frame)

    freq_frame = frames[:, 0] / 1e6 + 50.0
    fasores = frames[:, 1:]
    real = fasores[:, 0::2] / 1e6
    imag = fasores[:, 1::2] / 1e6

    completo = (real + 1j * imag).T
    return completo[1:hmax + 1, :], freq_frame  # descarta o termo DC


# ==========================================================================
# Correcao de fase (integral trapezoidal do desvio de frequencia)
# ==========================================================================
def corrigir_fase(freq_frame, fbDelay, M, PFT):
    """Aplica a correcao de fase acumulada a cada ordem harmonica.

    A correcao e uma INTEGRAL do desvio de frequencia multiplicada por h. Todo
    erro sistematico na base de tempo, por menor que seja, nao se cancela:
    acumula linearmente no tempo e e amplificado pela ordem harmonica. E esse
    o caminho pelo qual o piso aritmetico do SAPHO chega ao TVE (figura 3).
    """
    delta_f = freq_frame - f0
    correc = np.zeros(len(delta_f))
    for nn in range(1, len(delta_f)):
        if nn >= fbDelay + 1:
            correc[nn] = correc[nn - 1] + np.pi * (delta_f[nn] + delta_f[nn - 1]) * (M * Ts)
    correc = correc - 2 * np.pi / Nppc

    h = np.arange(1, hmax + 1).reshape(-1, 1)
    correcH = h * correc
    return np.unwrap(PFT + np.unwrap(correcH)), correc


# ==========================================================================
# Pipeline completo de um ensaio
# ==========================================================================
def processar(f1, sha, f_ini=None):
    """Replica o pipeline de teste_python.py para um ensaio off-nominal."""
    if f_ini is None:
        f_ini = f1

    # -- referencia analitica ------------------------------------------------
    x, Xr, fr, ROCOFr = signal_frequency(f1, N_AMOSTRAS, f0, Fs, Frep, hmax, hmag, SNR)

    # -- saidas do SAPHO -----------------------------------------------------
    X_sapho, freq_banco_sapho = ler_banco(sha)

    # -- estimacao de frequencia por zero-crossing ---------------------------
    _, _, f_zc, _, total_delay = estima_f_zc(x, Ts, Nppc, plot_level=0)

    tam = min(len(f_zc), len(fr))
    f_zc, fr = f_zc[:tam], fr[:tam]

    descarte = 4 * Nppc
    x = x[descarte:]
    f_zc = f_zc[descarte:]
    fr = fr[descarte:]
    ROCOFr = ROCOFr[descarte:]
    Xr = Xr[:, descarte:]

    # -- tendencia da frequencia (Kalman) ------------------------------------
    freq = kf_trend_poly(f_zc, f_ini, Ts, 1, Q_KALMAN, R_KALMAN)["b"].squeeze()

    tam = min(len(freq), len(fr))
    freq, fr = freq[:tam], fr[:tam]

    # -- atraso do sinal para compensar o atraso da estimacao ----------------
    atraso = np.zeros(total_delay + 1)
    atraso[-1] = 1.0
    x = lfilter(atraso, [1.0], x)

    fr = np.concatenate((np.zeros(total_delay), fr))
    Xr = np.hstack((np.zeros((hmax, total_delay)), Xr))
    ROCOFr = np.concatenate((np.zeros(total_delay), ROCOFr))

    descarte = 1200 * Nppc
    freq = freq[descarte:]
    x = x[descarte:]
    fr = fr[descarte:]
    Xr = Xr[:, descarte:]
    fr = fr[:len(freq)]

    # -- interpolacao B-spline (estrutura de Farrow) -------------------------
    tam = min(len(x), len(freq))
    x = x[:tam]
    xi = BSplineInterp(x, f0, freq, MBSP, Fs, plot_level=0)

    # -- banco de filtros polifasico -----------------------------------------
    M = int(Fs // f0)
    h_base = FlatTopFilterBase(8 * Nppc + 1)
    fbDelay = len(h_base) // (2 * M)

    xi = xi[:(len(xi) // Nppc) * Nppc]
    Xr = Xr[:, :(Xr.shape[1] // Nppc) * Nppc]
    freq = freq[:(len(freq) // Nppc) * Nppc]

    X = PolyphaseFilterBank(h_base, M, xi)[1:hmax + 1, :]

    freq = downsample(freq, M)
    Xr = downsample(Xr, M)

    freq = np.concatenate((np.zeros(fbDelay), freq))
    Xr = np.hstack((np.zeros((hmax, fbDelay)), Xr))
    freq_sapho = np.concatenate((np.zeros(fbDelay), freq_banco_sapho))

    tam = min(X.shape[1], X_sapho.shape[1], len(freq), len(freq_sapho), Xr.shape[1])
    X, X_sapho = X[:, :tam], X_sapho[:, :tam]
    freq, freq_sapho, Xr = freq[:tam], freq_sapho[:tam], Xr[:, :tam]

    AFT, PFT = 2 * np.abs(X), np.unwrap(np.angle(X))
    AFT_s, PFT_s = 2 * np.abs(X_sapho), np.unwrap(np.angle(X_sapho))

    PFTc, correc = corrigir_fase(freq, fbDelay, M, PFT)
    PFTc_s, correc_s = corrigir_fase(freq_sapho, fbDelay, M, PFT_s)

    Xc = AFT * np.exp(1j * PFTc)
    Xc_s = AFT_s * np.exp(1j * PFTc_s)

    # -- erros ----------------------------------------------------------------
    corte = 2 * fbDelay
    sl = slice(corte, corte + N_COMUM)

    Aref = np.abs(Xr)[:, sl]
    Pref = np.unwrap(np.angle(Xr))[:, sl]

    # h=2 nao existe no sinal (Aref = 0): a divisao por zero e esperada e o
    # resultado nao-finito e descartado por H_VALIDAS.
    with np.errstate(divide="ignore", invalid="ignore"):
        res = dict(
            f1=f1,
            tve_py=TVE(Xc[:, sl], Xr[:, sl]),
            tve_sa=TVE(Xc_s[:, sl], Xr[:, sl]),
            emag_py=100 * np.abs(AFT[:, sl] - Aref) / Aref,
            emag_sa=100 * np.abs(AFT_s[:, sl] - Aref) / Aref,
            efas_py=wrap_to_pi(PFTc[:, sl] - Pref) * 180 / np.pi,
            efas_sa=wrap_to_pi(PFTc_s[:, sl] - Pref) * 180 / np.pi,
            freq_sa=freq_sapho[sl],
            freq_py=freq[sl],
            correc_sa=correc_s[sl],
            n_frames_total=X_sapho.shape[1],
        )
    return res


def carregar(f1, sha, recalc=False):
    CACHE_DIR.mkdir(exist_ok=True)
    arq = CACHE_DIR / f"f{f1}.npz"
    if arq.exists() and not recalc:
        with np.load(arq) as d:
            return {k: d[k] for k in d.files}
    print(f"  processando {f1} Hz (commit {sha}) ...", flush=True)
    res = processar(f1, sha)
    np.savez_compressed(arq, **res)
    return res


# ==========================================================================
# Estatisticas
# ==========================================================================
def por_harmonica(m, reducao):
    """Reduz a janela temporal, por ordem harmonica, apenas em h validas."""
    return reducao(np.abs(m[IDX_VALIDAS, :]), axis=1)


def inclinacao_deriva(erro_fase, t):
    """Inclinacao (graus/s) do erro de fase, por ordem harmonica."""
    return np.array([np.polyfit(t, erro_fase[h - 1], 1)[0] for h in H_VALIDAS])


def montar(dados):
    """Empilha as estatisticas de todas as frequencias.

    O TVE do SAPHO NAO e estacionario: o erro de fase e uma rampa, entao
    qualquer estatistica depende da duracao do registro. A linha principal das
    figuras e a MEDIA sobre a janela comum (4,7 s), e a duracao tem de constar
    da legenda. Para referencia, em h=50: media 1,28 % contra maximo 2,33 %
    sobre 4,7 s, e 0,59 % de media sobre 1 s.
    """
    freqs = sorted(dados)
    t = np.arange(N_COMUM) / Frep
    est = {}
    for chave in ("tve", "emag", "efas"):
        for quem in ("sa", "py"):
            k = f"{chave}_{quem}"
            est[f"{k}_med"] = np.array([por_harmonica(dados[f][k], np.mean) for f in freqs])
            est[f"{k}_max"] = np.array([por_harmonica(dados[f][k], np.max) for f in freqs])

    # Deriva do erro de fase. A inclinacao e proporcional a h (base de tempo
    # comum), entao um ajuste pela origem sobre todas as harmonicas da o erro
    # de frequencia efetivo: incl(h) = 360 * h * eps_ef. Nao vira figura, mas
    # e o numero que justifica a degradacao no texto.
    est["incl_sa"] = np.array([inclinacao_deriva(dados[f]["efas_sa"], t) for f in freqs])
    est["incl_py"] = np.array([inclinacao_deriva(dados[f]["efas_py"], t) for f in freqs])

    h = H_VALIDAS.astype(float)
    est["eps_ef"] = est["incl_sa"] @ h / np.sum(h * h) / 360.0
    est["r2"] = np.array([
        1 - np.sum((y - k * 360 * h) ** 2) / np.sum((y - y.mean()) ** 2)
        for y, k in zip(est["incl_sa"], est["eps_ef"])
    ])
    est["freqs"] = np.array(freqs)
    return est


PAINEIS = [("tve", "TVE", "%", True),
           ("emag", "Erro de magnitude", "%", False),
           ("efas", "Erro de fase", "°", False)]


def marcar_limite(ax):
    ax.axhline(TVE_LIM, color=COR_LIM, ls="--", lw=1.1, zorder=6)
    ax.annotate("Limite IEC/IEEE 60255-118-1 (1 %)", xy=(1.4, TVE_LIM),
                xytext=(0, 4), textcoords="offset points", ha="left",
                va="bottom", fontsize=8, color=COR_LIM)


# ==========================================================================
# Figura A - envelope entre as frequencias (2 curvas + faixa media->maximo)
# ==========================================================================
def figura_envelope(est):
    """Leitura mais direta: a media de cada implementacao e o quanto o pior
    caso entre as 10 frequencias se afasta dela."""
    fig, axs = plt.subplots(3, 1, figsize=(6.3, 6.4), sharex=True)

    for ax, (chave, nome, unid, com_limite) in zip(axs, PAINEIS):
        # O Python vai por ultimo e tracejado: no painel de magnitude as duas
        # curvas coincidem, e e isso que precisa ficar visivel (o erro de
        # magnitude e igual; toda a diferenca esta na fase).
        for quem, cor in (("sa", COR_SAPHO), ("py", COR_PY)):
            med = est[f"{chave}_{quem}_med"].mean(axis=0)
            mx = est[f"{chave}_{quem}_max"].max(axis=0)
            ax.fill_between(H_VALIDAS, med, mx, color=cor, alpha=0.16, linewidth=0)
            ax.plot(H_VALIDAS, med, color=cor, lw=1.6,
                    ls="-" if quem == "sa" else (0, (5, 2)))

        if com_limite:
            marcar_limite(ax)

        ax.set_ylabel(f"{nome} ({unid})")
        ax.set_xlim(0, 51)
        ax.set_ylim(bottom=0)
        ax.margins(y=0.12)

    axs[-1].set_xlabel("Componentes harmônicas")
    axs[-1].set_xticks([1, 10, 20, 30, 40, 50])

    handles = [
        Line2D([], [], color=COR_SAPHO, lw=1.8, label="SAPHO — média"),
        Patch(facecolor=COR_SAPHO, alpha=0.16, label="SAPHO — até o máximo"),
        Line2D([], [], color=COR_PY, lw=1.8, ls="--", label="Python — média"),
        Patch(facecolor=COR_PY, alpha=0.16, label="Python — até o máximo"),
    ]
    axs[0].legend(handles=handles, ncol=2, loc="upper left", columnspacing=1.4,
                  handlelength=1.9)
    fig.subplots_adjust(hspace=0.12)
    salvar(fig, "figA_erros_envelope.pdf")


# ==========================================================================
# Figura B - uma linha por frequencia off-nominal
# ==========================================================================
def figura_por_frequencia(est):
    """Preserva a identidade de cada ensaio: mostra que 63 e 64 Hz se comportam
    melhor que as demais, o que o envelope da figura A esconde."""
    freqs = est["freqs"]
    fig, axs = plt.subplots(3, 1, figsize=(6.3, 6.4), sharex=True)

    for ax, (chave, nome, unid, com_limite) in zip(axs, PAINEIS):
        py = est[f"{chave}_py_med"]
        ax.fill_between(H_VALIDAS, py.min(axis=0), py.max(axis=0),
                        color=COR_BANDA, alpha=0.6, linewidth=0, zorder=1)
        ax.plot(H_VALIDAS, py.mean(axis=0), color="#4a4f54", lw=1.3, zorder=5)

        for k, f1 in enumerate(freqs):
            ax.plot(H_VALIDAS, est[f"{chave}_sa_med"][k], color=COR_FREQ[f1],
                    lw=1.15, zorder=3)

        if com_limite:
            marcar_limite(ax)

        ax.set_ylabel(f"{nome} médio ({unid})")
        ax.set_xlim(0, 51)
        ax.set_ylim(bottom=0)
        ax.margins(y=0.12)

    axs[-1].set_xlabel("Componentes harmônicas")
    axs[-1].set_xticks([1, 10, 20, 30, 40, 50])

    handles = [Line2D([], [], color=COR_FREQ[f], lw=1.6, label=f"{f} Hz")
               for f in freqs]
    handles.append(Line2D([], [], color="#4a4f54", lw=1.5,
                          label="Python\n(média)"))
    handles.append(Patch(facecolor=COR_BANDA, alpha=0.6,
                         label="Python\n(mín.–máx.)"))
    fig.legend(handles=handles, loc="center left", bbox_to_anchor=(0.90, 0.5),
               handlelength=1.4, labelspacing=0.42, borderaxespad=0)
    fig.subplots_adjust(right=0.88, hspace=0.12)
    salvar(fig, "figB_erros_por_frequencia.pdf")



def salvar(fig, nome):
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(SAIDA_DIR / nome)
    plt.close(fig)
    print(f"  gravado: {SAIDA_DIR / nome}")


# ==========================================================================
def main():
    recalc = "--recalc" in sys.argv

    print("Lendo os ensaios off-nominal do historico do git ...")
    dados = {f1: carregar(f1, sha, recalc) for f1, sha in sorted(COMMITS.items())}
    est = montar(dados)

    ULP = 2.0 ** -23
    print("\nTVE (%%) - MEDIA sobre %d frames = %.2f s  [maximo entre colchetes]"
          % (N_COMUM, N_COMUM / Frep))
    print(f"{'f1':>4} {'frames':>7} {'eps_ef':>8} {'ULP':>5} "
          + "".join(f"{'h=' + str(h):>32}" for h in (1, 25, 50)))
    print(f"{'':>4} {'':>7} {'(uHz)':>8} {'':>5} "
          + "".join(f"{'SAPHO':>16}{'Python':>16}" for _ in range(3)))
    for k, f1 in enumerate(est["freqs"]):
        linha = (f"{f1:>4} {dados[f1]['n_frames_total']:>7} "
                 f"{est['eps_ef'][k]*1e6:>8.2f} "
                 f"{abs(est['eps_ef'][k])/f0/ULP:>5.2f} ")
        for h in (1, 25, 50):
            i = int(np.where(H_VALIDAS == h)[0][0])
            for quem in ("sa", "py"):
                linha += (f"{est[f'tve_{quem}_med'][k, i]:>8.3f}"
                          f"{'[' + format(est[f'tve_{quem}_max'][k, i], '.2f') + ']':>8}")
        print(linha)

    print(f"\nO TVE do SAPHO nao e estacionario: o erro de fase e uma rampa, entao"
          f"\ntoda estatistica depende da duracao do registro. Em h=50, media de"
          f"\n{est['tve_sa_med'][:, -1].mean():.2f} % sobre {N_COMUM/Frep:.1f} s contra "
          f"maximo de {est['tve_sa_max'][:, -1].max():.2f} %.")
    print(f"Deriva do modelo em Python (float64), h=50: "
          f"max |incl| = {np.abs(est['incl_py'][:, -1]).max():.4f} deg/s "
          f"(SAPHO: {np.abs(est['incl_sa'][:, -1]).max():.4f} deg/s)")
    print(f"Erro de base de tempo implicito: {np.abs(est['eps_ef']).mean()*1e6:.1f} uHz "
          f"= {np.abs(est['eps_ef']).mean()/f0/ULP:.2f} ULP do float de 23 bits "
          f"(R2 minimo do ajuste em h = {est['r2'].min():.5f})")

    print("\nGerando figuras ...")
    figura_envelope(est)
    figura_por_frequencia(est)


if __name__ == "__main__":
    main()
