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
    x, Xr, fr, ROCOFr = signal_frequency(f1, N_AMOSTRAS, f0, Fs, Frep, hmax, hmag, SNR)
    res = processar_sinal(x, Xr, fr, ROCOFr, sha, f_ini)
    res["f1"] = f1
    return res


def processar_sinal(x, Xr, fr, ROCOFr, sha, f_ini, n_comum=None):
    """Pipeline comum a qualquer ensaio, dado o sinal de referencia gerado.

    Separado de `processar` para que o script da rampa
    (plot_dissertacao_rampa.py) use exatamente o mesmo caminho de calculo,
    trocando apenas o gerador do sinal e o `f_ini` do Kalman.
    """
    if n_comum is None:
        n_comum = N_COMUM

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
    # fr = frequencia VERDADEIRA por frame. Nao entra em nenhum calculo do
    # pipeline; e guardada para servir de referencia ideal na figura D.
    fr = downsample(fr[:(len(fr) // Nppc) * Nppc], M)
    fr = np.concatenate((np.zeros(fbDelay), fr))

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
    sl = slice(corte, corte + n_comum)

    Aref = np.abs(Xr)[:, sl]
    Pref = np.unwrap(np.angle(Xr))[:, sl]

    # h=2 nao existe no sinal (Aref = 0): a divisao por zero e esperada e o
    # resultado nao-finito e descartado por H_VALIDAS.
    with np.errstate(divide="ignore", invalid="ignore"):
        res = dict(
            tve_py=TVE(Xc[:, sl], Xr[:, sl]),
            tve_sa=TVE(Xc_s[:, sl], Xr[:, sl]),
            emag_py=100 * np.abs(AFT[:, sl] - Aref) / Aref,
            emag_sa=100 * np.abs(AFT_s[:, sl] - Aref) / Aref,
            efas_py=wrap_to_pi(PFTc[:, sl] - Pref) * 180 / np.pi,
            efas_sa=wrap_to_pi(PFTc_s[:, sl] - Pref) * 180 / np.pi,
            freq_sa=freq_sapho[sl],
            freq_py=freq[sl],
            fr_frame=fr[:tam][sl],
            correc_sa=correc_s[sl],
            correc_py=correc[sl],
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
# Comparacao estagio a estagio entre o SAPHO e o modelo em Python
# ==========================================================================
# Cada saida do interpolador corresponde a uma etapa do pipeline e alinha
# indice a indice com a etapa equivalente em Python (lag 0, verificado).
# O pre-filtro IIR NAO esta disponivel: o `fout(5, acc*1e6)` que o exportaria
# esta comentado em proc_interp.cmm:186 e o testbench so abre os canais 0..4.
ESTAGIOS = [
    ("zc", "Zero-crossing", "saida_interp1.txt", "Hz"),
    ("kalman", "Kalman", "saida_interp2.txt", "Hz"),
    ("atraso", "Sinal atrasado", "saida_interp3.txt", "p.u."),
    ("bspline", "B-spline (Farrow)", "saida_interp0.txt", "p.u."),
]

JANELA = 1024              # amostras por ponto (~1/15 s)
DESCARTE_TRANSITORIO = 8 * Nppc


def _media_movel(dif, janela=JANELA):
    """Media do valor absoluto da diferenca, por janela.

    Do valor absoluto, e nao da diferenca com sinal: o erro oscila em torno de
    zero e a media simples daria ~0, escondendo a amplitude.
    """
    n = len(dif) // janela
    if n == 0:
        return np.array([]), np.array([])
    d = dif[:n * janela].reshape(n, janela)
    return np.mean(np.abs(d), axis=1), (np.arange(n) + 0.5) * janela


def comparar_estagios(f1, sha):
    x, _, _, _ = signal_frequency(f1, N_AMOSTRAS, f0, Fs, Frep, hmax, hmag, SNR)
    return comparar_estagios_sinal(x, sha, f1, float(f1))


def comparar_estagios_sinal(x, sha, f_ini, base_freq):
    """Diferenca media SAPHO - Python em cada etapa do pipeline.

    O eixo de tempo e ABSOLUTO (desde o inicio da simulacao), porque as etapas
    comecam em instantes diferentes: ZC e Kalman cobrem o registro inteiro,
    enquanto o sinal atrasado e o interpolado so sao despejados apos os 1200
    ciclos de descarte. `base_freq` e a frequencia usada para normalizar as
    grandezas em Hz (a do ensaio no off-nominal, a media da rampa na rampa).
    """
    _, _, py_zc, _, total_delay = estima_f_zc(x, Ts, Nppc, plot_level=0)

    d1 = 4 * Nppc
    py_kalman = kf_trend_poly(py_zc[d1:], f_ini, Ts, 1, Q_KALMAN, R_KALMAN)["b"].squeeze()

    atraso = np.zeros(total_delay + 1)
    atraso[-1] = 1.0
    x_at = lfilter(atraso, [1.0], x[d1:])

    d2 = 1200 * Nppc
    py_atraso = x_at[d2:]
    freq = py_kalman[d2:]
    n = min(len(py_atraso), len(freq))
    py_bspline = BSplineInterp(py_atraso[:n], f0, freq[:n], MBSP, Fs, plot_level=0)

    # Amostra de entrada correspondente ao indice 0 de cada fluxo
    origem = {"zc": 0, "kalman": d1, "atraso": d1 + d2, "bspline": d1 + d2}
    python = {"zc": py_zc, "kalman": py_kalman,
              "atraso": py_atraso, "bspline": py_bspline}
    escala = {"zc": (1e6, 0.0), "kalman": (1e6, -60.0),
              "atraso": (1e6, 0.0), "bspline": (1e6, 0.0)}

    # Base de normalizacao: frequencia do ensaio para as grandezas em Hz, e a
    # amplitude eficaz do sinal para as grandezas em p.u. Sem isso nao daria
    # para pôr Hz e p.u. no mesmo eixo.
    base = {"zc": base_freq, "kalman": base_freq,
            "atraso": float(np.sqrt(np.mean(x ** 2))),
            "bspline": float(np.sqrt(np.mean(x ** 2)))}

    res = {}
    for chave, _, arquivo, _ in ESTAGIOS:
        div, off = escala[chave]
        sa = _git_show(sha, arquivo)[1:] / div - off
        py = python[chave]
        m = min(len(sa), len(py))
        dif = sa[:m] - py[:m]

        corte = DESCARTE_TRANSITORIO if chave in ("zc", "kalman") else 0
        media, centro = _media_movel(dif[corte:])

        # O B-spline sai na taxa reamostrada (lambda = f0/f1 amostras de
        # entrada por amostra de saida); mapeia-se linearmente de volta para a
        # taxa de entrada pela razao entre os comprimentos do proprio Python.
        passo = (n / len(py_bspline)) if chave == "bspline" else 1.0
        res[f"t_{chave}"] = (origem[chave] + corte + centro * passo) / Fs
        res[f"dif_{chave}"] = media
        res[f"med_{chave}"] = float(np.mean(np.abs(dif[corte:])))
        res[f"base_{chave}"] = base[chave]
    return res


def carregar_estagios(f1, sha, recalc=False):
    CACHE_DIR.mkdir(exist_ok=True)
    arq = CACHE_DIR / f"estagios_f{f1}.npz"
    if arq.exists() and not recalc:
        with np.load(arq) as d:
            return {k: d[k] for k in d.files}
    print(f"  comparando estagios em {f1} Hz ...", flush=True)
    res = comparar_estagios(f1, sha)
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



# ==========================================================================
# Figura C - divergencia SAPHO x Python etapa a etapa
# ==========================================================================
def figura_estagios(estagios):
    """Onde, ao longo da cadeia, o hardware se afasta do modelo.

    Painel unico. Como as etapas medem grandezas diferentes (Hz no
    zero-crossing e no Kalman, p.u. no interpolado), tudo e normalizado pela
    propria grandeza e mostrado como diferenca RELATIVA (adimensional) - so
    assim as tres curvas dividem um eixo com significado. Escala logaritmica
    porque elas cobrem quatro decadas.

    O eixo do tempo comeca em zero no inicio da JANELA ANALISADA (~5 s). A
    simulacao tem 1600 ciclos = 26,7 s, mas os primeiros 1200 ciclos sao
    descarte de acomodacao e nao sao despejados pelo interpolador.

    Por que o B-spline chega a ~4e-3 (verificado nas 10 frequencias,
    medido/previsto = 0,67 +- 0,10): o interpolador INTEGRA a diferenca de
    frequencia. Os ~4e-7 de diferenca relativa na saida do Kalman acumulam, em
    5 s, um deslocamento de tempo de ~2 us. Num sinal com harmonicas ate
    2850 Hz, 2 us aparecem como ~0,4 % de diferenca amostra a amostra:

        dif_RMS = tau * 2*pi*f1 * sqrt(sum_h (A_h * h)^2 / 2)

    Ou seja, e um deslocamento no TEMPO, nao um erro de amplitude - e por isso
    que o TVE da fundamental fica em 0,05 % apesar dos 4000 ppm daqui. A
    comparacao amostra a amostra e a metrica mais dura possivel para um sinal
    reamostrado.
    """
    freqs = sorted(estagios)
    # Verde/roxo/cinza de proposito: nas figuras A e B laranja e azul
    # significam SAPHO e Python, e aqui TODA curva ja e uma diferenca.
    series = [("zc", "Zero-crossing", "#1b7837"),
              ("kalman", "Kalman", "#3b78b0"),
              ("bspline", "B-spline (Farrow)", "#762a83")]

    fig, ax = plt.subplots(figsize=(6.3, 3.9))

    t0 = max(estagios[freqs[0]][f"t_{c}"][0] for c, _, _ in series)
    menor, maior = np.inf, 0.0
    for chave, nome, cor in series:
        # Os fluxos tem comprimentos diferentes por frequencia (o B-spline
        # emite mais amostras quanto maior f1): corta-se pelo mais curto.
        n = min(len(estagios[f][f"dif_{chave}"]) for f in freqs)
        t = estagios[freqs[0]][f"t_{chave}"][:n]
        pilha = np.array([estagios[f][f"dif_{chave}"][:n] / estagios[f][f"base_{chave}"]
                          for f in freqs])
        m = t >= t0
        # Tempo relativo ao inicio da janela analisada, nao ao inicio da
        # simulacao: os primeiros 1200 ciclos sao descarte de acomodacao.
        tj = t[m] - t0
        ax.fill_between(tj, pilha.min(axis=0)[m], pilha.max(axis=0)[m],
                        color=cor, alpha=0.18, linewidth=0)
        ax.plot(tj, pilha.mean(axis=0)[m], color=cor, lw=1.5, label=nome)
        menor = min(menor, pilha.min(axis=0)[m].min())
        maior = max(maior, pilha.max(axis=0)[m].max())

    # Limites colados nos dados: sem decada vazia no topo. A legenda fica FORA
    # da area de plotagem, senao teria de haver folga so para acomoda-la.
    ax.set_yscale("log")
    ax.set_ylim(menor / 2.0, maior * 1.6)
    ax.set_xlim(0, None)
    ax.set_xlabel("Tempo dentro da janela analisada (s)")
    ax.set_ylabel("Diferença média entre SAPHO\ne Python, relativa")
    ax.grid(True, which="minor", linestyle=":", linewidth=0.4, alpha=0.25)
    ax.legend(ncol=3, loc="lower left", bbox_to_anchor=(0, 1.01),
              columnspacing=1.8, borderaxespad=0)
    salvar(fig, "figC_divergencia_por_estagio.pdf")


# ==========================================================================
# Figura D - a correcao de fase como integrador
# ==========================================================================
def _integral_fase(dfreq):
    """Integral trapezoidal do desvio de frequencia, em graus.

    Mesma recursao de `corrigir_fase`, mas na taxa de frame e devolvendo graus.
    """
    c = np.zeros(len(dfreq))
    for n in range(1, len(dfreq)):
        c[n] = c[n - 1] + np.pi * (dfreq[n] + dfreq[n - 1]) / Frep
    return c * 180 / np.pi


def figura_correcao(res, salvar_fn, nome, h_ref=50):
    """Erro da correcao de fase: SAPHO e modelo em Python contra a ideal.

    Nao adianta plotar as duas correcoes brutas: elas chegam a milhares de
    graus e diferem entre si por 1 parte em 100 mil, o que e sub-pixel em
    qualquer escala. Aqui se plota o ERRO de cada uma em relacao a correcao
    ideal - a integral da frequencia VERDADEIRA de referencia. Nessa escala as
    duas curvas se separam visivelmente: a do modelo fica colada no zero e a do
    SAPHO se afasta linearmente, que e o efeito do integrador.

    RESSALVA para o texto: esta e a parcela do erro devida a correcao de fase,
    nao o erro total. O interpolador reamostra usando f_estimada e a correcao
    desfaz a reamostragem usando a MESMA f_estimada, entao um erro em
    f_estimada entra duas vezes com sinais contrarios e as parcelas se cancelam
    em boa parte. Em 57 Hz e h=50: +2,3 graus desta parcela contra -3,5 da
    reamostragem, resultando em -1,2.
    """
    ideal = _integral_fase(res["fr_frame"] - f0)
    erro_sa = (_integral_fase(res["freq_sa"] - f0) - ideal) * h_ref
    erro_py = (_integral_fase(res["freq_py"] - f0) - ideal) * h_ref
    t = np.arange(len(ideal)) / Frep

    fig, ax = plt.subplots(figsize=(6.3, 3.9))

    ax.axhline(0, color=COR_TINTA, lw=1.0, ls="--")
    ax.annotate("correção ideal", xy=(t[-1], 0), xytext=(-4, 4),
                textcoords="offset points", ha="right", va="bottom",
                fontsize=8.5, color=COR_TINTA)
    ax.plot(t, erro_py, color=COR_PY, lw=1.6, ls=(0, (5, 2)),
            label="Modelo em Python")
    ax.plot(t, erro_sa, color=COR_SAPHO, lw=1.8, label="SAPHO")

    ax.set_xlim(0, t[-1])
    ax.margins(y=0.18)
    ax.set_xlabel("Tempo dentro da janela analisada (s)")
    ax.set_ylabel(f"Erro da correção de fase\nem $h$ = {h_ref} (°)")
    ax.legend(loc="best", handlelength=2.4)
    salvar_fn(fig, nome)


def salvar(fig, nome):
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        fig.savefig(SAIDA_DIR / nome)
        print(f"  gravado: {SAIDA_DIR / nome}")
    except PermissionError:
        # Tipicamente o PDF esta aberto num visualizador: avisa e segue, para
        # nao perder as demais figuras da rodada.
        print(f"  NAO gravado (arquivo em uso): {SAIDA_DIR / nome}")
    finally:
        plt.close(fig)


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

    print("\nDivergencia SAPHO x Python por estagio do pipeline")
    print("(o pre-filtro IIR nao esta nos dados: fout(5) comentado no .cmm)")
    estagios = {f1: carregar_estagios(f1, sha, recalc)
                for f1, sha in sorted(COMMITS.items())}
    print(f"{'estagio':>20} {'unid':>5} {'media |dif|':>12} {'relativa':>10} "
          f"{'inicio':>10} {'fim':>10} {'razao':>7}")
    for chave, nome, _, unid in ESTAGIOS:
        med = np.mean([estagios[f][f"med_{chave}"] for f in estagios])
        rel = np.mean([estagios[f][f"med_{chave}"] / estagios[f][f"base_{chave}"]
                       for f in estagios])
        ini = np.mean([estagios[f][f"dif_{chave}"][0] for f in estagios])
        fim = np.mean([estagios[f][f"dif_{chave}"][-1] for f in estagios])
        print(f"{nome:>20} {unid:>5} {med:>12.3e} {rel:>10.2e} {ini:>10.3e} "
              f"{fim:>10.3e} {fim/ini:>7.1f}x")
    print("  (o sinal atrasado nao entra na figura: e so o buffer de 255 "
          "amostras,\n   e sua diferenca e o piso de quantizacao Q15 da entrada)")

    # A figura do integrador precisa de UM ensaio: usa-se o de maior deriva
    # acumulada na correcao, que e o caso mais ilustrativo.
    pior = max(dados, key=lambda f: abs(np.mean(dados[f]["freq_sa"] - dados[f]["freq_py"])))
    d = (dados[pior]["correc_sa"] - dados[pior]["correc_py"]) * 180 / np.pi
    print(f"\nIntegrador da correcao (f1 = {pior} Hz, maior deriva): entrada media "
          f"{np.mean(dados[pior]['freq_sa'] - dados[pior]['freq_py'])*1e6:+.1f} uHz -> "
          f"saida {d[-1]-d[0]:+.3f} graus em h=1 ({(d[-1]-d[0])*50:+.1f} em h=50)")

    print("\nGerando figuras ...")
    figura_envelope(est)
    figura_por_frequencia(est)
    figura_estagios(estagios)
    figura_correcao(dados[pior], salvar, "figD_correcao_integrador.pdf")


if __name__ == "__main__":
    main()
