"""
Figuras do ensaio de MODULACAO para o capitulo de resultados.

Analogo de plot_dissertacao_offnominal.py e plot_dissertacao_rampa.py, dos
quais reaproveita todo o pipeline de calculo. Muda o gerador do sinal e o
limite normativo.

ATENCAO AO LIMITE: no ensaio de modulacao a IEC/IEEE 60255-118-1 admite
TVE de 3 %, e nao de 1 % como nos ensaios estatico e de rampa.

Sao quatro ensaios, dois de cada tipo de modulacao, todos com 1600 ciclos:

    ka = 0,1 / kx = 0   -> modulacao de FASE      (fm = 0,5 e 5 Hz)
    kx = 0,1 / ka = 0   -> modulacao de AMPLITUDE (fm = 0,5 e 5 Hz)

Cada um esta num commit, lido com `git show`, que nao toca a arvore de
trabalho.

Saida: dois PDFs vetoriais em
C:\\Users\\Ricardo\\Documents\\plotsDissertacao\\modulacao

Uso:
    python plot_dissertacao_modulacao.py            # usa cache quando existir
    python plot_dissertacao_modulacao.py --recalc   # ignora o cache
"""

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import plot_dissertacao_offnominal as base
from sinaisIEC60255_118 import modulation

# ==========================================================================
# Configuracao dos ensaios
# ==========================================================================
SAIDA_DIR = Path(r"C:\Users\Ricardo\Documents\plotsDissertacao\modulacao")
CACHE_DIR = Path(__file__).resolve().parent / "cache_modulacao"

PROFUNDIDADE = 0.1             # kx ou ka, conforme o tipo
N_AMOSTRAS = 1600 * base.Nppc  # 409600 amostras
N_COMUM = 280                  # frames analisados (ha 317 disponiveis)

# No ensaio de modulacao o limite de TVE e 3 %, nao 1 %.
TVE_LIM_MOD = 3.0

# (tipo, fm) -> commit
ENSAIOS = {
    ("ka", 0.5): "f4fb2bc",
    ("ka", 5.0): "1b84b49",
    ("kx", 0.5): "948f968",
    ("kx", 5.0): "7a53756",
}

TIPOS = {
    "ka": ("Modulação de fase", r"$k_a$ = 0,1"),
    "kx": ("Modulação de amplitude", r"$k_x$ = 0,1"),
}

# Cor = implementacao (como em todas as outras figuras da dissertacao);
# traco = frequencia de modulacao. Assim o par laranja/azul continua
# significando SAPHO/Python no trabalho inteiro.
ESTILO_FM = {0.5: "-", 5.0: (0, (5, 2))}

H = base.H_VALIDAS
IDX = base.IDX_VALIDAS
PAINEIS = base.PAINEIS


# ==========================================================================
# Processamento
# ==========================================================================
def processar(tipo, fm, sha):
    kx = PROFUNDIDADE if tipo == "kx" else 0.0
    ka = PROFUNDIDADE if tipo == "ka" else 0.0
    x, Xr, fr, ROCOFr = modulation(fm, kx, ka, N_AMOSTRAS, base.f0, base.Fs,
                                   base.Frep, base.hmax, base.hmag, base.SNR)
    # f_ini = 60 Hz: a modulacao oscila em torno da nominal. Os commits usavam
    # f_ini = 35 por heranca da rampa, o que e irrelevante apos 1200 ciclos de
    # descarte (verificado), mas 60 e o valor correto para este ensaio.
    return base.processar_sinal(x, Xr, fr, ROCOFr, sha, base.f0, n_comum=N_COMUM)


def carregar(tipo, fm, sha, recalc=False):
    CACHE_DIR.mkdir(exist_ok=True)
    arq = CACHE_DIR / f"{tipo}_fm{fm:g}.npz"
    if arq.exists() and not recalc:
        with np.load(arq) as d:
            return {k: d[k] for k in d.files}
    print(f"  processando {tipo}, fm = {fm:g} Hz (commit {sha}) ...", flush=True)
    res = processar(tipo, fm, sha)
    np.savez_compressed(arq, **res)
    return res


def processar_estagios(tipo, fm, sha):
    kx = PROFUNDIDADE if tipo == "kx" else 0.0
    ka = PROFUNDIDADE if tipo == "ka" else 0.0
    x, _, _, _ = modulation(fm, kx, ka, N_AMOSTRAS, base.f0, base.Fs,
                            base.Frep, base.hmax, base.hmag, base.SNR)
    # Normaliza as grandezas em Hz pela nominal: a modulacao oscila em torno
    # dela, entao 60 Hz e a base natural.
    return base.comparar_estagios_sinal(x, sha, base.f0, base.f0)


def carregar_estagios(tipo, fm, sha, recalc=False):
    CACHE_DIR.mkdir(exist_ok=True)
    arq = CACHE_DIR / f"estagios_{tipo}_fm{fm:g}.npz"
    if arq.exists() and not recalc:
        with np.load(arq) as d:
            return {k: d[k] for k in d.files}
    print(f"  comparando estagios {tipo}, fm = {fm:g} Hz ...", flush=True)
    res = processar_estagios(tipo, fm, sha)
    np.savez_compressed(arq, **res)
    return res


def salvar(fig, nome):
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        fig.savefig(SAIDA_DIR / nome)
        print(f"  gravado: {SAIDA_DIR / nome}")
    except PermissionError:
        print(f"  NAO gravado (arquivo em uso): {SAIDA_DIR / nome}")
    finally:
        plt.close(fig)


# ==========================================================================
# Figura: um arquivo por tipo de modulacao, com as duas frequencias
# ==========================================================================
def figura(tipo, dados):
    fms = sorted(fm for (t, fm) in ENSAIOS if t == tipo)
    fig, axs = plt.subplots(3, 1, figsize=(6.3, 6.4), sharex=True)

    for ax, (chave, nome, unid, com_limite) in zip(axs, PAINEIS):
        for fm in fms:
            res = dados[(tipo, fm)]
            for quem, cor in (("sa", base.COR_SAPHO), ("py", base.COR_PY)):
                m = np.abs(res[f"{chave}_{quem}"][IDX]).mean(axis=1)
                ax.plot(H, m, color=cor, lw=1.5, ls=ESTILO_FM[fm])

        ax.set_ylabel(f"{nome} médio ({unid})")
        ax.set_xlim(0, 51)
        ax.set_ylim(bottom=0)
        ax.margins(y=0.12)

        if com_limite:
            base.marcar_limite(ax, TVE_LIM_MOD, x=50.6, ha="right")
            # Folga acima do limite para caber o rotulo e a legenda: aqui o
            # limite (3 %) fica bem acima dos dados, entao ele e quem manda
            # no topo do eixo.
            ax.set_ylim(0, TVE_LIM_MOD * 1.35)

    axs[-1].set_xlabel("Componentes harmônicas")
    axs[-1].set_xticks([1, 10, 20, 30, 40, 50])

    # Legenda em duas partes: a cor diz a implementacao, o traco diz o fm.
    handles = [
        Line2D([], [], color=base.COR_SAPHO, lw=1.8, label="SAPHO"),
        Line2D([], [], color=base.COR_PY, lw=1.8, label="Modelo em Python"),
    ] + [Line2D([], [], color=base.COR_TINTA, lw=1.5, ls=ESTILO_FM[fm],
                label=f"$f_m$ = {fm:g} Hz".replace(".", ","))
         for fm in fms]
    axs[0].legend(handles=handles, ncol=2, loc="upper left", columnspacing=1.4,
                  handlelength=2.4)

    fig.subplots_adjust(hspace=0.12)
    salvar(fig, f"fig_modulacao_{tipo}.pdf")


# ==========================================================================
# Figura de divergencia por estagio, no mesmo formato da figC do off-nominal
# ==========================================================================
ESTAGIOS_FIG = [("zc", "Zero-crossing", "#1b7837"),
                ("kalman", "Kalman", "#3b78b0"),
                ("bspline", "B-spline (Farrow)", "#762a83")]


def figura_estagios(tipo, estagios):
    """Divergencia SAPHO x Python etapa a etapa, como na figC do off-nominal.

    Cor = estagio do pipeline; traco = frequencia de modulacao. Tudo
    normalizado pela propria grandeza (Hz pela nominal, p.u. pela amplitude
    eficaz) e mostrado como diferenca relativa, unica forma de por Hz e p.u.
    no mesmo eixo. Escala logaritmica: as curvas cobrem varias decadas.
    """
    fms = sorted(fm for (t, fm) in ENSAIOS if t == tipo)
    fig, ax = plt.subplots(figsize=(6.3, 3.9))

    t0 = max(estagios[(tipo, fm)][f"t_{c}"][0] for fm in fms for c, _, _ in ESTAGIOS_FIG)
    menor, maior = np.inf, 0.0

    for chave, nome, cor in ESTAGIOS_FIG:
        for fm in fms:
            est = estagios[(tipo, fm)]
            t = est[f"t_{chave}"]
            v = est[f"dif_{chave}"] / est[f"base_{chave}"]
            m = t >= t0
            ax.plot(t[m] - t0, v[m], color=cor, lw=1.3, ls=ESTILO_FM[fm])
            menor, maior = min(menor, v[m].min()), max(maior, v[m].max())

    ax.set_yscale("log")
    ax.set_ylim(menor / 2.0, maior * 1.6)
    ax.set_xlim(0, None)
    ax.set_xlabel("Tempo dentro da janela analisada (s)")
    ax.set_ylabel("Diferença média entre SAPHO\ne Python, relativa")
    ax.grid(True, which="minor", linestyle=":", linewidth=0.4, alpha=0.25)

    handles = [Line2D([], [], color=c, lw=1.6, label=n) for _, n, c in ESTAGIOS_FIG]
    handles += [Line2D([], [], color=base.COR_TINTA, lw=1.4, ls=ESTILO_FM[fm],
                       label=f"$f_m$ = {fm:g} Hz".replace(".", ","))
                for fm in fms]
    ax.legend(handles=handles, ncol=3, loc="lower left", bbox_to_anchor=(0, 1.01),
              columnspacing=1.4, borderaxespad=0)
    salvar(fig, f"figC_modulacao_{tipo}.pdf")


# ==========================================================================
def main():
    recalc = "--recalc" in sys.argv

    print(f"Ensaios de modulacao: profundidade {PROFUNDIDADE}, "
          f"{N_AMOSTRAS / base.Fs:.1f} s, limite de TVE = {TVE_LIM_MOD:g} %")
    dados = {k: carregar(k[0], k[1], sha, recalc) for k, sha in sorted(ENSAIOS.items())}

    print(f"\nTVE (%) - media sobre {N_COMUM} frames = "
          f"{N_COMUM / base.Frep:.2f} s [maximo entre colchetes]")
    print(f"{'ensaio':>22} " + "".join(f"{'h=' + str(h):>32}" for h in (1, 25, 50)))
    print(f"{'':>22} " + "".join(f"{'SAPHO':>16}{'Python':>16}" for _ in range(3)))
    for (tipo, fm), res in sorted(dados.items()):
        rot = f"{TIPOS[tipo][0].split()[-1]} fm={fm:g}Hz"
        linha = f"{rot:>22} "
        for h in (1, 25, 50):
            for quem in ("sa", "py"):
                v = np.abs(res[f"tve_{quem}"][h - 1])
                linha += f"{v.mean():>8.3f}{'[' + format(v.max(), '.2f') + ']':>8}"
        print(linha)

    estagios = {k: carregar_estagios(k[0], k[1], sha, recalc)
                for k, sha in sorted(ENSAIOS.items())}

    print("\nDivergencia SAPHO x Python por estagio (media da janela, relativa):")
    print(f"{'ensaio':>22} " + "".join(f"{n:>20}" for _, n, _ in ESTAGIOS_FIG))
    for (tipo, fm), est in sorted(estagios.items()):
        rot = f"{TIPOS[tipo][0].split()[-1]} fm={fm:g}Hz"
        linha = f"{rot:>22} "
        for chave, _, _ in ESTAGIOS_FIG:
            linha += f"{est[f'med_{chave}'] / est[f'base_{chave}']:>20.2e}"
        print(linha)

    print("\nGerando figuras ...")
    for tipo in ("ka", "kx"):
        figura(tipo, dados)
        figura_estagios(tipo, estagios)


if __name__ == "__main__":
    main()
