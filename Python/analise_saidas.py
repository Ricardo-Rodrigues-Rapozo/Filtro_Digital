from contextlib import redirect_stdout
from pathlib import Path
import io
import warnings

# Este script gera a referencia em Python, executa o mesmo fluxo principal do
# principal_Naiara.py por tras dos panos e compara essa referencia com os TXT
# exportados pelo SAPHo. A ideia e manter tudo linear e facil de auditar:
# primeiro monta o caminho Python, depois le o SAPHo, depois corrige fase e
# calcula os erros.

import matplotlib
import numpy as np
from scipy.signal import lfilter

# Blocos originais usados pelo fluxo de validacao.
from sinaisIEC60255_118 import signal_frequency
from DSPEPS import (
    BSplineInterp,
    FlatTopFilterBase,
    PolyphaseFilterBank,
    downsample,
    estima_f_zc,
)
from auxiliares import TVE, wrap_to_pi

# Backend sem janela. Assim o script pode rodar direto no terminal e salvar os
# PDFs mesmo sem interface grafica aberta.
#matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ===================================================
# Parametros iguais ao principal_Naiara.py
# ===================================================
# Frequencia nominal do sistema.
f0 = 60

# Numero de pontos por ciclo nominal usado em todo o processamento.
Nppc = 256

# Frequencia de amostragem e periodo de amostragem.
Fs = f0 * Nppc
Ts = 1 / Fs

# Numero de ciclos efetivos analisados apos os descartes.
Nc = 600

# Quantidade maxima de harmonicos produzidos/esperados no banco.
hmax = 50

# Magnitude dos harmonicos injetados na geracao do sinal sintetico.
hmag = 0.05

# Frequencia de referencia usada pela interpolacao.
Fr = 60

# SNR alto para deixar o teste praticamente deterministico.
SNR = 6_000_000

# Frequencia off-nominal do caso avaliado.
f1 = 65

# Ordem do interpolador B-spline.
MBSP = 5

# Fator de decimacao: uma saida do banco por ciclo nominal.
M = Fs // f0

# Os arquivos do SAPHo estao em ponto fixo escalado por 1e6.
ESCALA = 1_000_000.0

# Caminhos relativos ao repositorio, para o script funcionar de qualquer cwd.
BASE_DIR = Path(__file__).resolve().parents[1]
DADOS_DIR = BASE_DIR / "Aurora" / "dados_simulacao"
SAIDA_DIR = DADOS_DIR / "analise_saidas"

# Arquivos brutos exportados pelo testbench/SAPHo.
ARQ_SAPHO_BANCO = DADOS_DIR / "saida_banco0.txt"
ARQ_SAPHO_FREQ = DADOS_DIR / "saida_interp2.txt"
ARQ_SAPHO_INTERP = DADOS_DIR / "saida_interp0.txt"
ARQ_SAPHO_pre_zc = DADOS_DIR / "saida_interp3.txt"
ARQ_SAPHO_freq_zc = DADOS_DIR / "saida_interp1.txt"


# Harmonicos mostrados no grafico de conferencia visual.
HARMONICOS_PLOT = (1, 13, 27, 49)

# Parametros de janela/corte. Ficam separados para facilitar testes de atraso
# sem procurar numeros magicos no meio do fluxo.
CICLOS_EXTRAS_GERACAO = 300
CICLOS_EXTRAS_ANALISE = 200
MULTIPLICADOR_DESCARTE_ZC = 2
MULTIPLICADOR_CORTE_BANCO = 4

# Tamanhos derivados dos parametros acima.
AMOSTRAS_GERACAO = (Nc + CICLOS_EXTRAS_GERACAO) * Nppc
AMOSTRAS_ANALISE = (Nc + CICLOS_EXTRAS_ANALISE) * Nppc
TAMANHO_FILTRO_BANCO = 8 * Nppc + 1


def corrigir_fase(X, freq, pre_delay, fbDelay):
    """
    Corrige a fase dos fasores usando a frequencia estimada.

    X pode vir tanto do banco Python quanto do banco SAPHo. Por isso esta
    funcao nao tem nenhum ajuste especifico de origem: se Python e SAPHo
    estiverem alinhados, a mesma regra deve servir para os dois.
    """
    # Mesma correcao usada para os dois caminhos analisados: banco Python e
    # banco SAPHo. A diferenca entre eles deve vir dos fasores/frequencia de
    # entrada, nao de uma formula de fase diferente.

    # O banco retorna uma componente complexa por harmonico. O fator 2 coloca a
    # magnitude na mesma convencao da referencia gerada por signal_frequency.
    AFT = 2 * np.abs(X)

    # unwrap evita saltos artificiais de +/-pi durante a integracao/erro.
    PFT = np.unwrap(np.angle(X), axis=1)

    # delta_f e a frequencia instantanea medida em relacao a nominal.
    delta_f = freq[: X.shape[1]] - f0

    # correc_fundamental acumula a rotacao de fase da fundamental, frame a
    # frame. Ela e escalar no harmonico porque ainda representa apenas H1.
    correc_fundamental = np.zeros(len(delta_f))

    for nn in range(1, len(delta_f)):
        if nn >= fbDelay + 1:
            # Integracao trapezoidal da frequencia desviada. Como cada frame
            # esta espacadamente em M*Ts segundos, este termo vira radianos.
            correc_fundamental[nn] = (
                correc_fundamental[nn - 1]
                + np.pi * (delta_f[nn] + delta_f[nn - 1]) * (M * Ts)
            )

    # A integral abaixo compensa a rotacao acumulada entre a frequencia do
    # sinal e a frequencia nominal, frame a frame. Como o banco entrega um
    # fasor por ciclo nominal, M*Ts = 1/f0.
    #
    # O termo de meia volta do ZC (-pi) existe na deducao porque a estimacao
    # usa meio ciclo. Isso vale tanto para Python quanto para SAPHo. Nesta
    # analise, porem, os fasores dos dois bancos e a referencia ja estao na
    # mesma convencao de sinal/indice: H1 esta na linha 0 e os harmonicos
    # impares nao devem ser invertidos. Colocar -pi aqui contaria essa meia
    # volta novamente e joga o TVE para perto de 200%.
    #
    # O termo constante que ainda precisa entrar explicitamente e o atraso do
    # pre-filtro do ZC, expresso como fracao de um ciclo nominal.
    correc_fundamental = correc_fundamental + (pre_delay / Nppc) * 2 * np.pi

    # Cada harmonico gira h vezes a fase fundamental. Por isso o h nao entra
    # na realimentacao escalar acima: ele so expande a correcao de H1 para
    # H2, H3, ..., depois que a fase fundamental foi integrada.
    h = np.arange(1, X.shape[0] + 1).reshape(-1, 1)
    correc_harmonicos = h * correc_fundamental
    PFTc = np.unwrap(PFT + correc_harmonicos, axis=1)

    # Reconstroi o fasor corrigido mantendo a magnitude medida pelo banco.
    return AFT * np.exp(1j * PFTc)


def carregar_sapho_banco():
    """
    Le saida_banco0.txt no mesmo formato usado na validacao de referencia.

    Retorno: matriz [harmonico, frame], com linha 0 = H1 e linha 49 = H50.
    """
    out = np.loadtxt(ARQ_SAPHO_BANCO)

    # O primeiro escalar do arquivo pertence ao frame anterior. Tiramos esse
    # valor velho uma unica vez e depois montamos os pares real/imaginario.
    out = out[1:]

    fasores_por_frame = hmax + 1
    escalares_por_frame = 2 * fasores_por_frame
    N_frames = len(out) // escalares_por_frame
    out = out[: N_frames * escalares_por_frame]

    # Cada linha e um frame completo. O frame tem 51 fasores complexos
    # (DC, H1, ..., H50), mas no TXT isso vira 102 escalares:
    # real_DC, imag_DC, real_H1, imag_H1, ...
    frames = out.reshape(N_frames, escalares_por_frame)
    real = frames[:, 0::2] / ESCALA
    imag = frames[:, 1::2] / ESCALA
    fasor_completo = (real + 1j * imag).T

    # Descarta o indice 0, que e o nivel DC.
    return fasor_completo[1 : hmax + 1, :]


def carregar_freq_sapho(n_frames, fbDelay):
    """
    Le a frequencia do SAPHo e coloca na taxa de fasores do banco.

    A saida_interp2 e gravada na taxa de amostras interpoladas/entrada do
    banco; depois ela e decimada por M para virar uma frequencia por frame.
    """
    # saida_interp2 deve ser o fout2 gravado junto com cada fout0 valido.
    # Assim ela fica no eixo da entrada do banco polifasico, igual ao arquivo
    # de frequencia usado no validacaoOffnominal/ValidacaoRampa.
    freq_interp = np.loadtxt(ARQ_SAPHO_FREQ) / ESCALA

    if ARQ_SAPHO_INTERP.exists(): ## 
        interp = np.loadtxt(ARQ_SAPHO_INTERP)
        if (
            len(freq_interp) == len(interp)
            and freq_interp[0] == 0
            and freq_interp[1] != 0
        ):
            # O primeiro zero e apenas o dummy inicial exportado antes da
            # primeira amostra interpolada util.
            freq_interp = freq_interp[1:]

    # Agora a frequencia pode ser decimada diretamente, no mesmo estilo:
    # freq = fr[::M].
    freq = downsample(freq_interp, M)

    # Compensa o atraso do banco polifasico no eixo de frames.
    freq = np.concatenate((np.zeros(fbDelay), freq))
    freq = freq[:-fbDelay]

    return freq[:n_frames]


def calcular_metricas(nome, Xc, Xr):
    """
    Calcula magnitude, fase e TVE por harmonico impar.

    Xc e a estimativa corrigida; Xr e a referencia. Ambas devem estar no mesmo
    eixo [harmonico, frame].
    """
    # Primeiro iguala a quantidade de harmonicos e frames disponiveis.
    n_h = min(Xc.shape[0], Xr.shape[0])
    n_f = min(Xc.shape[1], Xr.shape[1])

    # O teste de interesse usa apenas harmonicos impares: H1, H3, ..., H49.
    # Como H1 esta no indice 0, os impares ficam nos indices 0, 2, 4...
    indh = np.arange(0, n_h, 2)

    Xc = Xc[:n_h, :n_f][indh]
    Xr = Xr[:n_h, :n_f][indh]

    # Separa magnitude e fase para relatorios especificos.
    AFT = np.abs(Xc)
    Aref = np.abs(Xr)
    PFT = np.unwrap(np.angle(Xc), axis=1)
    Pref = np.unwrap(np.angle(Xr), axis=1)

    # Erro relativo de magnitude em porcentagem.
    erro_mag = 100 * np.abs(AFT - Aref) / Aref

    # Erro de fase limitado a [-pi, pi] antes de converter para graus.
    erro_fase = np.abs(wrap_to_pi(PFT - Pref)) * 180 / np.pi

    # TVE ja retorna percentual pela funcao auxiliar do projeto.
    tve = TVE(Xc, Xr)

    # Uma linha por harmonico: H, erro medio/max de magnitude, fase e TVE.
    resumo = np.column_stack(
        (
            indh + 1,
            np.mean(erro_mag, axis=1),
            np.max(erro_mag, axis=1),
            np.mean(erro_fase, axis=1),
            np.max(erro_fase, axis=1),
            np.mean(tve, axis=1),
            np.max(tve, axis=1),
        )
    )

    return nome, resumo


def salvar_resumo(nome_arquivo, resumo):
    """Salva o resumo numerico em TXT com cabecalho legivel."""
    cabecalho = (
        "harmonico erro_mag_medio_percent erro_mag_max_percent "
        "erro_fase_medio_graus erro_fase_max_graus "
        "tve_medio_percent tve_max_percent"
    )
    np.savetxt(
        SAIDA_DIR / nome_arquivo,
        resumo,
        fmt=["%d", "%.10f", "%.10f", "%.10f", "%.10f", "%.10f", "%.10f"],
        header=cabecalho,
    )


def plotar_erros(nome_arquivo, titulo, resumo):
    """Gera um PDF com erro medio e maximo por harmonico."""
    # Primeira coluna do resumo guarda o numero do harmonico.
    harmonicos = resumo[:, 0]

    # Tres linhas: magnitude, fase e TVE.
    fig, axes = plt.subplots(3, 1, figsize=(9, 10), sharex=True, constrained_layout=True)
    fig.suptitle(titulo)

    # Cada entrada define um subplot: titulo, eixo y, curva media, curva maxima.
    dados = [
        ("Erro de magnitude", "Erro (%)", resumo[:, 1], resumo[:, 2], "royalblue"),
        ("Erro de fase", "Erro (graus)", resumo[:, 3], resumo[:, 4], "seagreen"),
        ("Total Vector Error", "TVE (%)", resumo[:, 5], resumo[:, 6], "crimson"),
    ]

    for ax, (subtitulo, ylabel, medio, maximo, cor) in zip(axes, dados):
        # Curva continua para media; curva tracejada para pior caso.
        ax.plot(harmonicos, medio, "o-", color=cor, label="Medio")
        ax.plot(harmonicos, maximo, "o--", color=cor, label="Maximo")
        ax.set_title(subtitulo)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        ax.legend()

    # Linha de referencia do limite classico de 1% de TVE.
    axes[2].axhline(1.0, color="black", linestyle=":", label="Limite TVE 1%")
    axes[2].set_xlabel("Harmonico")
    axes[2].legend()

    # Salva e fecha para nao acumular figuras em memoria.
    fig.savefig(SAIDA_DIR / nome_arquivo, format="pdf")
    plt.close(fig)


def plotar_tres_sinais(Xr, X_python, X_sapho):
    """
    Plota referencia, banco Python e SAPHo para harmonicos escolhidos.

    Este grafico nao e a metrica final; ele serve para olhar se a divergencia
    esta mais evidente na magnitude, na fase, ou em algum harmonico especifico.
    """
    # Usa apenas o trecho comum entre os tres sinais.
    n_h = min(Xr.shape[0], X_python.shape[0], X_sapho.shape[0])
    n_f = min(Xr.shape[1], X_python.shape[1], X_sapho.shape[1])

    Xr = Xr[:n_h, :n_f]
    X_python = X_python[:n_h, :n_f]
    X_sapho = X_sapho[:n_h, :n_f]

    # Uma linha por harmonico e duas colunas: magnitude e fase.
    fig, axes = plt.subplots(
        len(HARMONICOS_PLOT),
        2,
        figsize=(13, 12),
        sharex=True,
        constrained_layout=True,
    )
    fig.suptitle("Referencia x Python x SAPHo")

    sinais = [
        ("Referencia", Xr, "black"),
        ("Python", X_python, "royalblue"),
        ("SAPHo", X_sapho, "crimson"),
    ]

    for linha, harmonico in enumerate(HARMONICOS_PLOT):
        # A matriz usa indice zero: H1 -> 0, H13 -> 12, etc.
        idx = harmonico - 1
        if idx >= n_h:
            continue

        x = np.arange(n_f)
        for nome, sinal, cor in sinais:
            # Magnitude no painel esquerdo.
            axes[linha, 0].plot(x, np.abs(sinal[idx]), color=cor, label=nome)

            # Fase desembrulhada em graus no painel direito.
            axes[linha, 1].plot(
                x,
                np.rad2deg(np.unwrap(np.angle(sinal[idx]))),
                color=cor,
                label=nome,
            )

        axes[linha, 0].set_title(f"H{harmonico} - magnitude")
        axes[linha, 1].set_title(f"H{harmonico} - fase")
        axes[linha, 0].grid(True, alpha=0.3)
        axes[linha, 1].grid(True, alpha=0.3)

    axes[0, 0].legend()
    axes[-1, 0].set_xlabel("Frame")
    axes[-1, 1].set_xlabel("Frame")

    # PDF unico de conferencia visual dos tres caminhos.
    fig.savefig(SAIDA_DIR / "comparacao_ref_python_sapho_harmonicos.pdf", format="pdf")
    plt.close(fig)


# Garante que a pasta de saida exista antes de salvar TXT/PDF.
SAIDA_DIR.mkdir(parents=True, exist_ok=True)

# ===================================================
# 1. Principal
# ===================================================
# O sinal e a referencia sao gerados um pouco mais longos que a janela final.
# Esses ciclos extras permitem descartar o transitorio do ZC/interpolador sem
# encurtar a analise de Nc ciclos.
x, Xr, fr, _ = signal_frequency(f1, AMOSTRAS_GERACAO, f0, Fs, Fr, hmax, hmag, SNR)

# estima_f_zc imprime/avisa coisas que aqui nao interessam. Como este script
# e de analise automatica, suprimimos a saida e guardamos apenas os vetores e
# atrasos retornados.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    with redirect_stdout(io.StringIO()):
        f_zc_m, zc_m_delay,f_zc, zc_delay,v = estima_f_zc(
            x,
            1 / Fs,
            Nppc,
            plot_level=1,
        )

atraso_meio_ciclo_zc = Nppc // 2
pre_delay = zc_delay - atraso_meio_ciclo_zc

freq = f_zc_m
delay = np.zeros(zc_m_delay + 1)
delay[-1] = 1.0
x = lfilter(delay, [1.0], x)

fr = np.concatenate((np.zeros(zc_m_delay), fr))
Xr = np.hstack((np.zeros((hmax, zc_m_delay), dtype=complex), Xr))

# ===================================================
# 2. Saida SAPHo
# ===================================================
# Banco SAPHo bruto: fasores complexos por harmonico/frame.
#X_sapho = carregar_sapho_banco()

filtro_pre_zc = np.loadtxt(ARQ_SAPHO_pre_zc) / ESCALA
filtro_pre_zc = filtro_pre_zc[1:]

plt.figure(figsize=(10, 4))
plt.plot(filtro_pre_zc,"o-", label="filtro_pre_zc sapho")
plt.plot(v[:len(filtro_pre_zc)],"o-", label="filtro_pre_zc python")
plt.legend()
plt.title("Frequencias usadas no banco SAPHo e no banco Python")
plt.xlabel("Frame")
plt.ylabel("Frequencia (Hz)")
plt.grid(True, alpha=0.3)
plt.show(block=False)

# Frequencia SAPHo no mesmo eixo de frames do banco.
#freq_sapho = carregar_freq_sapho(X_sapho.shape[1],0)
freq_zc_sapho = np.loadtxt(ARQ_SAPHO_freq_zc) / ESCALA
freq_zc_sapho = freq_zc_sapho[1:]

plt.figure(figsize=(10, 4))
plt.plot(freq_zc_sapho,"o-", label="freq_ZC_sapho")
plt.plot(f_zc[:len(freq_zc_sapho)],"o-", label="freq_ZC_python")
plt.plot(fr[:len(freq_zc_sapho)], label="fr")
plt.legend()
plt.title("Frequencias ZC usadas no banco SAPHo e no banco Python")
plt.xlabel("Frame")
plt.ylabel("Frequencia (Hz)")
plt.grid(True, alpha=0.3)
plt.show(block=False)

# Frequencia SAPHo no mesmo eixo de frames do banco.
#freq_sapho = carregar_freq_sapho(X_sapho.shape[1],0)
freq_sapho = np.loadtxt(ARQ_SAPHO_FREQ) / ESCALA
freq_sapho = freq_sapho[1:]

plt.figure(figsize=(10, 4))
plt.plot(freq_sapho,"o-", label="freq_sapho")
plt.plot(freq[:len(freq_sapho)],"o-", label="freq_python")
plt.plot(fr[:len(freq_sapho)], label="fr")
plt.legend()
plt.title("Frequencias usadas no banco SAPHo e no banco Python")
plt.xlabel("Frame")
plt.ylabel("Frequencia (Hz)")
plt.grid(True, alpha=0.3)
plt.show(block=False)

# O descarte e arredondado para ciclos inteiros para nao introduzir fase
# fracionaria extra na referencia.
ciclos_descartados_zc = int(np.ceil(zc_m_delay / Nppc))
discard_samples = MULTIPLICADOR_DESCARTE_ZC * ciclos_descartados_zc * Nppc
fim_analise = discard_samples + AMOSTRAS_ANALISE

# A partir daqui todos os vetores continuam com a mesma origem temporal.
freq = freq[discard_samples:fim_analise]
x = x[discard_samples:fim_analise]
fr = fr[discard_samples:fim_analise]
Xr = Xr[:, discard_samples:fim_analise]

# Interpolacao B-spline exatamente como no principal_Naiara, mas usando as
# variaveis acima para deixar explicito qual frequencia alimenta o processo.
xi = BSplineInterp(x, f0, freq, MBSP, Fs, plot_level=0)


# ===================================================
# 3. Saida SAPHo
# ===================================================
# Banco SAPHo bruto: fasores complexos por harmonico/frame.
#X_sapho = carregar_sapho_banco()

# Frequencia SAPHo no mesmo eixo de frames do banco.
#freq_sapho = carregar_freq_sapho(X_sapho.shape[1],0)
xi_sapho = np.loadtxt(ARQ_SAPHO_INTERP) / ESCALA
xi_sapho = xi_sapho[1:]

plt.figure(figsize=(10, 4))
plt.plot(xi_sapho,"o-", label="xi_sapho")
plt.plot(xi[:len(xi_sapho)],"o-", label="xi")
plt.legend()
plt.title("Frequencias usadas no banco SAPHo e no banco Python")
plt.xlabel("Frame")
plt.ylabel("Frequencia (Hz)")
plt.grid(True, alpha=0.3)
plt.show(block=True)

h = FlatTopFilterBase(TAMANHO_FILTRO_BANCO)
fbDelay = len(h) // (2 * M)

# O banco consome amostras e entrega um fasor por ciclo nominal. Mantemos
# fbDelay ciclos extras na entrada porque eles serao usados para compensar o
# atraso de grupo do filtro polifasico depois da decimacao.
amostras_entrada_banco = (Nc + fbDelay) * Nppc

# O mesmo corte e aplicado ao sinal interpolado, a referencia e a frequencia.
xi = xi[:amostras_entrada_banco]
Xr = Xr[:, :amostras_entrada_banco]
freq = freq[:amostras_entrada_banco]
fr = fr[:amostras_entrada_banco]

# O banco tambem calcula a componente DC. Como a comparacao comeca em H1,
# descartamos a linha zero da saida completa.
X_python_com_dc = PolyphaseFilterBank(h, M, xi)
X_python = X_python_com_dc[1 : hmax + 1, :] 

# A frequencia e a referencia saem da taxa de amostras para a taxa de fasores.
freq_python = downsample(freq, M)
Xr = downsample(Xr, M)
fr = downsample(fr, M)

# Compensacao do atraso do banco: o mesmo numero de frames zero e inserido na
# frequencia e na referencia para comparar com o fasor que saiu do filtro.
freq_python = np.concatenate((np.zeros(fbDelay), freq_python))
fr = np.concatenate((np.zeros(fbDelay), fr))
Xr = np.hstack((np.zeros((hmax, fbDelay), dtype=complex), Xr))

freq_python = freq_python[:-fbDelay]
fr = fr[:-fbDelay]
Xr = Xr[:, :-fbDelay]



# ===================================================
# 3. Correcao de fase e corte do transitorio
# ===================================================
# Antes da metrica, todos os sinais sao cortados para o menor tamanho comum.
# Isso evita comparar frames que existem em um caminho mas nao em outro.
n_h = min(X_python.shape[0], X_sapho.shape[0], Xr.shape[0])
n_f = min(X_python.shape[1], X_sapho.shape[1], Xr.shape[1], len(freq_sapho))

X_python = X_python[:n_h, :n_f] ## normaliza tamanho para o menor entre os tamanhos
X_sapho = X_sapho[:n_h, :n_f] ## normaliza tamanho para o menor entre os tamanhos
Xr = Xr[:n_h, :n_f] ## normaliza tamanho para o menor entre os tamanhos
freq_python = freq_python[:n_f] ## normaliza tamanho para o menor entre os tamanhos
freq_sapho = freq_sapho[:n_f] ## normaliza tamanho para o menor entre os tamanhos

# Aplica exatamente a mesma correcao de fase no banco Python e no SAPHo.
Xc_python = corrigir_fase(X_python, freq_python, pre_delay, fbDelay)
Xc_sapho = corrigir_fase(X_sapho, freq_sapho, pre_delay, fbDelay)

# Remove frames iniciais ainda influenciados pelo transitorio do banco.
corte = MULTIPLICADOR_CORTE_BANCO * fbDelay
Xc_python = Xc_python[:, corte:]  ## tira um pedaço do iniio do python para tirar o transitorio do banco
Xc_sapho = Xc_sapho[:, corte:] ## tira um pedaço do iniio do sapho para tirar o transitorio do banco
Xr = Xr[:, corte:] ## tira um pedaço do iniio da referencia para tirar o transitorio do banco

# ===================================================
# 4. Analise de desempenho
# ===================================================
# Calcula uma tabela separada para o banco Python e para o SAPHo.
nome_python, resumo_python = calcular_metricas("python_banco", Xc_python, Xr)
nome_sapho, resumo_sapho = calcular_metricas("sapho_banco", Xc_sapho, Xr)

# Salva TXT e graficos individuais de erro.
salvar_resumo("resumo_python_banco.txt", resumo_python)
salvar_resumo("resumo_sapho_banco.txt", resumo_sapho)
plotar_erros("grafico_python_banco.pdf", nome_python, resumo_python)
plotar_erros("grafico_sapho_banco.pdf", nome_sapho, resumo_sapho)

# Salva grafico comparando referencia, Python e SAPHo no mesmo desenho.
plotar_tres_sinais(Xr, Xc_python, Xc_sapho)

# Resumo curto no terminal para conferir rapidamente o alinhamento usado.
print("Analise finalizada.")
print(
    "ZC: "
    f"meio_ciclo={atraso_meio_ciclo_zc}, "
    f"pre_delay={pre_delay}, "
    f"zc_delay={zc_delay}, "
    f"zc_m_delay={zc_m_delay}"
)
print(
    "Banco: "
    f"tamanho_filtro={TAMANHO_FILTRO_BANCO}, "
    f"fbDelay={fbDelay}, "
    f"corte={corte}"
)
print(f"Janelas: descarte={discard_samples}, entrada_banco={amostras_entrada_banco}")
print(f"Referencia: {Xr.shape}")
print(f"Python:     {Xc_python.shape}")
print(f"SAPHo:      {Xc_sapho.shape}")
print()

# Resumo global: media dos TVEs medios por harmonico e pior TVE maximo.
print(f"Python TVE medio/max: {np.mean(resumo_python[:, 5]):.6f}% / {np.max(resumo_python[:, 6]):.6f}%")
print(f"SAPHo  TVE medio/max: {np.mean(resumo_sapho[:, 5]):.6f}% / {np.max(resumo_sapho[:, 6]):.6f}%")
print(f"Resultados salvos em: {SAIDA_DIR}")
