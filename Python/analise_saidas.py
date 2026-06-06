from pathlib import Path
import warnings

import matplotlib
import numpy as np
from scipy.signal import bessel, bilinear, group_delay

from sinaisIEC60255_118 import signal_frequency
from auxiliares import TVE, wrap_to_pi

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ======================================================================
# Parametros do caso analisado
# ======================================================================

F0 = 60
F1 = 65
N_PPC = 256
FS = F0 * N_PPC
TS = 1 / FS
NC = 600
FR = 60
HMAX = 50
HMAG = 0.05
SNR = 6_000_000
ESCALA_BANCO = 1_000_000.0

M = FS // F0
N_SIGNAL = (NC + 300) * N_PPC
N_ANALISE = (NC + 200) * N_PPC

BASE_DIR = Path(__file__).resolve().parents[1]
DADOS_DIR = BASE_DIR / "Aurora" / "dados_simulacao"
SAIDA_DIR = DADOS_DIR / "analise_saidas"

REAL_PYTHON_TXT = DADOS_DIR / "saida_real_banco.txt"
IMAG_PYTHON_TXT = DADOS_DIR / "saida_im_banco.txt"
SAPHO_TXT = DADOS_DIR / "saida_banco0.txt"
FREQ_MEDIA_SAPHO_TXT = DADOS_DIR / "saida_interp2.txt"
FREQ_ATRASADA_SAPHO_TXT = DADOS_DIR / "saida_interp4.txt"

HARMONICOS_ANALISADOS = np.arange(1, HMAX + 1, 2)
INDICES_HARMONICOS = HARMONICOS_ANALISADOS - 1
HARMONICOS_PLOT = (1, 13, 27, int(HARMONICOS_ANALISADOS[-1]))

# A saida_interp2/4 do SAPHO fica etiquetada uma amostra de entrada
# adiantada em relacao ao fluxo Python equivalente.
ADIANTAMENTO_FREQ_AMOSTRAS_SAPHO = 1

# A rotacao fixa de uma amostra no fasor SAPHO foi testada separadamente
# e piora estes dados; mantemos a fase sem esse termo constante.
AJUSTE_FASE_AMOSTRAS_SAPHO = 0.0

# Se quiser tambem mostrar as figuras em uma janela, troque para True.
ABRIR_GRAFICOS = False


def calcular_atrasos():
    """Calcula os atrasos usados no mesmo fluxo de principal_Naiara.py."""
    b, a = bessel(6, 2 * np.pi * 90, analog=True)
    b, a = bilinear(b, a, fs=FS)

    # group_delay pode avisar sobre singularidades fora da regiao de interesse.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        freq_gd, gd = group_delay((b, a), w=4096, fs=FS)

    idx_60hz = np.argmin(np.abs(freq_gd - F0))
    pre_delay = int(round(gd[idx_60hz]))

    zc_delay = pre_delay + N_PPC // 2
    zc_m_delay = N_PPC // 2 + zc_delay
    discard_samples = 2 * int(np.ceil(zc_m_delay / N_PPC) * N_PPC)

    tamanho_filtro = 8 * N_PPC + 1
    fb_delay = tamanho_filtro // (2 * M)

    return pre_delay, zc_m_delay, discard_samples, fb_delay


def carregar_saida_python():
    """Le a saida complexa exportada pelo banco polifasico em Python."""
    real = np.loadtxt(REAL_PYTHON_TXT) / ESCALA_BANCO
    imag = np.loadtxt(IMAG_PYTHON_TXT) / ESCALA_BANCO

    if real.shape != imag.shape:
        raise ValueError(
            f"Dimensoes diferentes: real={real.shape}, imag={imag.shape}"
        )

    if real.shape[0] != HMAX:
        raise ValueError(
            f"Esperava {HMAX} harmonicos na saida Python, mas veio {real.shape[0]}."
        )

    return real + 1j * imag


def erro_medio_raw(sapho, python):
    """Erro simples entre a matriz SAPHO bruta e a matriz Python bruta."""
    n_harmonicos = min(sapho.shape[0], python.shape[0])
    n_frames = min(sapho.shape[1], python.shape[1])

    sapho = sapho[:n_harmonicos, :n_frames]
    python = python[:n_harmonicos, :n_frames]

    return np.mean(np.abs(sapho - python))


def candidatos_saida_sapho(fasores, componentes):
    """Gera os cortes possiveis para transformar componentes em H1..H50."""
    n_frames = fasores.size // componentes
    matriz = fasores[: componentes * n_frames].reshape(componentes, n_frames, order="F")

    if componentes == HMAX:
        yield "50 componentes: linhas 0..49 = H1..H50", matriz[:HMAX, :]
    elif componentes == HMAX + 1:
        yield "51 componentes: linhas 0..49 = H1..H50", matriz[:HMAX, :]
        yield "51 componentes: linhas 1..50 = H1..H50", matriz[1 : HMAX + 1, :]


def candidatos_saida_sapho_com_atraso_escalar(out):
    """
    Reconstrucao para a captura atual do top_level_tb.

    O banco emite 102 escalares por frame: real/imag de 51 componentes.
    Como out0_banco e registrado e o testbench escreve no mesmo posedge,
    o primeiro escalar de cada frame e o valor atrasado do frame anterior.
    Assim, H1..H49 ficam nos escalares 3..100 de cada frame.
    """
    escalares_por_frame = 2 * (HMAX + 1)

    if out.size % escalares_por_frame != 0:
        return

    frames = out.reshape(-1, escalares_por_frame)

    candidatos = [
        ("real=primeiro, imag=segundo", lambda real, imag: real + 1j * imag),
        ("real=segundo, imag=primeiro", lambda real, imag: imag + 1j * real),
        ("conjugado", lambda real, imag: real - 1j * imag),
        ("troca + conjugado", lambda real, imag: imag - 1j * real),
    ]

    for nome, montar_complexo in candidatos:
        fasores = []
        for frame in frames:
            valores_h1_h49 = frame[3:101]
            real = valores_h1_h49[0::2]
            imag = valores_h1_h49[1::2]
            fasores.append(montar_complexo(real, imag))

        matriz = np.array(fasores).T
        yield (
            "captura registrada: descarta 1 escalar/frame; "
            f"H1..H49; {nome}",
            matriz,
        )


def carregar_saida_sapho(saida_python):
    """Le a saida serial do SAPHO e escolhe o mapeamento mais parecido com Python."""
    out = np.loadtxt(SAPHO_TXT) / ESCALA_BANCO

    if out.size % 2 != 0:
        raise ValueError("saida_banco0.txt deve ter uma quantidade par de amostras.")

    primeira = out[0::2]
    segunda = out[1::2]

    ordens_complexas = [
        ("ordem Vitor: real=amostra par, imag=amostra impar", primeira + 1j * segunda),
        ("ordem invertida: real=amostra impar, imag=amostra par", segunda + 1j * primeira),
    ]

    melhores = []
    for nome_ordem, fasores in ordens_complexas:
        for componentes in (HMAX + 1, HMAX):
            if fasores.size % componentes != 0:
                continue

            for nome_corte, matriz in candidatos_saida_sapho(fasores, componentes):
                if matriz.shape[0] != HMAX:
                    continue

                erro = erro_medio_raw(matriz, saida_python)
                melhores.append((erro, nome_ordem, nome_corte, matriz))

    for nome_corte, matriz in candidatos_saida_sapho_com_atraso_escalar(out):
        erro = erro_medio_raw(matriz, saida_python)
        melhores.append((erro, "reconstrucao por frame", nome_corte, matriz))

    if not melhores:
        raise ValueError(
            "Nao foi possivel organizar saida_banco0.txt em blocos de 50 ou 51 "
            f"componentes. Total de fasores: {primeira.size}."
        )

    erro, nome_ordem, nome_corte, matriz = min(melhores, key=lambda item: item[0])

    print("\nMapeamento SAPHO escolhido:")
    print(f"  {nome_ordem}")
    print(f"  {nome_corte}")
    print(f"  erro bruto medio contra Python: {erro:.6e}")

    return matriz


def diagnosticar_saida_sapho(saida_sapho, saida_python, fb_delay):
    """Mostra avisos simples sobre problemas comuns na saida SAPHO."""
    if saida_sapho.shape[0] < 2 or saida_sapho.shape[1] == 0:
        return

    n_frames = min(saida_sapho.shape[1], saida_python.shape[1])
    inicio = min(2 * fb_delay, max(n_frames - 1, 0))
    sapho = saida_sapho[:, inicio:n_frames]
    python = saida_python[:, inicio:n_frames]

    if sapho.size == 0 or python.size == 0:
        return

    media_sapho = np.mean(np.abs(sapho), axis=1)
    media_python = np.mean(np.abs(python), axis=1)

    razao_h1 = media_sapho[0] / max(media_python[0], 1e-12)
    razao_harmonicos = np.median(
        media_sapho[2::2] / np.maximum(media_python[2::2], 1e-12)
    )

    print("\nDiagnostico SAPHO bruto:")
    print(f"  |H1| SAPHO/Python = {razao_h1:.3f}")
    print(f"  mediana |H3..H49| SAPHO/Python = {razao_harmonicos:.3f}")

    if razao_harmonicos < 0.2:
        print(
            "  Aviso: os harmonicos do SAPHO estao muito menores que os do Python."
        )
        print(
            "  Isso costuma indicar entrada diferente no testbench ou exportacao/calculo "
            "dos bins harmonicos ainda incorreto."
        )


def gerar_referencia(pre_delay, zc_m_delay, discard_samples, fb_delay):
    """Gera Xr por signal_frequency e aplica os mesmos cortes principais."""
    _, Xr, _, _ = signal_frequency(F1, N_SIGNAL, F0, FS, FR, HMAX, HMAG, SNR)

    # Alinha com o atraso da estimacao de frequencia por zero crossing.
    zeros_zc = np.zeros((HMAX, zc_m_delay), dtype=complex)
    Xr = np.hstack((zeros_zc, Xr))
    Xr = Xr[:, discard_samples : discard_samples + N_ANALISE]

    # Alinha com a saida decimada do banco polifasico.
    Xr = Xr[:, : (NC + fb_delay) * N_PPC]
    Xr = Xr[..., ::M]

    zeros_fb = np.zeros((HMAX, fb_delay), dtype=complex)
    Xr = np.hstack((zeros_fb, Xr))
    Xr = Xr[:, :-fb_delay]

    return Xr


def reconstruir_frequencia_interpolada(freq_entrada):
    """
    Reconstroi a frequencia associada a cada amostra interpolada do SAPHO.

    saida_interp2/saida_interp4 sao gravadas uma vez por amostra de entrada.
    Ja saida_interp0 pode gerar 1 ou 2 amostras para a mesma entrada, conforme
    o acumulador alfa do Farrow. Este loop repete a frequencia com a mesma
    logica de lambda = 60/frequencia usada em proc_interp.cmm.
    """
    freq_interpolada = []
    alfa = 0.0
    cnt = 0

    for freq in np.asarray(freq_entrada, dtype=float):
        lambda_val = FR / freq if freq != 0.0 else 0.0

        if cnt > 6:
            if lambda_val <= 0.0:
                continue

            while alfa < 1.0:
                freq_interpolada.append(freq)
                alfa += lambda_val

            alfa -= 1.0
        else:
            cnt += 1

    return np.asarray(freq_interpolada)


def compensar_adiantamento_amostras(vetor, adiantamento_amostras):
    """
    Ajusta vetores exportados por amostra quando o SAPHO registra o instante
    uma amostra adiantado em relacao ao fluxo equivalente em Python.
    """
    vetor = np.asarray(vetor)
    adiantamento_amostras = int(adiantamento_amostras)

    if adiantamento_amostras == 0:
        return vetor

    if abs(adiantamento_amostras) >= vetor.size:
        raise ValueError("Deslocamento de amostras maior que o vetor de entrada.")

    if adiantamento_amostras > 0:
        preenchimento = np.full(adiantamento_amostras, vetor[0], dtype=vetor.dtype)
        return np.concatenate((preenchimento, vetor))[: vetor.size]

    atraso = -adiantamento_amostras
    preenchimento = np.full(atraso, vetor[-1], dtype=vetor.dtype)
    return np.concatenate((vetor[atraso:], preenchimento))


def alinhar_frequencia_com_banco(freq_interpolada, n_frames, fb_delay, offset=0):
    """Decima a frequencia interpolada e aplica o atraso do banco polifasico."""
    if offset >= freq_interpolada.size:
        raise ValueError("Offset maior que o vetor de frequencia interpolada.")

    freq_frames = freq_interpolada[offset::M]
    freq_frames = np.concatenate((np.zeros(fb_delay), freq_frames))[:-fb_delay]

    if freq_frames.size == 0:
        raise ValueError("Nao ha amostras suficientes para alinhar a frequencia.")

    if freq_frames.size < n_frames:
        freq_frames = np.pad(freq_frames, (0, n_frames - freq_frames.size), mode="edge")

    return freq_frames[:n_frames]


def preparar_frequencia_sapho(
    n_frames,
    fb_delay,
    saida_sapho=None,
    referencia=None,
    pre_delay=None,
    adiantamento_freq_amostras=0,
    ajuste_fase_amostras=0.0,
):
    """
    Carrega a frequencia estimada pelo SAPHO para usar na correcao de fase.

    Preferimos saida_interp4.txt porque ela e a freq_atrasada usada pelo Farrow.
    Se ela nao existir, usamos saida_interp2.txt, que e a frequencia media fcc.
    """
    fontes = [
        (FREQ_ATRASADA_SAPHO_TXT, "saida_interp4.txt (freq_atrasada usada pelo Farrow)"),
        (FREQ_MEDIA_SAPHO_TXT, "saida_interp2.txt (fcc: media movel da frequencia)"),
    ]
    fontes = [(caminho, descricao) for caminho, descricao in fontes if caminho.exists()]

    if not fontes:
        print("\nFrequencia SAPHO nao encontrada; usando F1 constante na fase.")
        return None

    melhor = None
    usar_referencia = (
        saida_sapho is not None and referencia is not None and pre_delay is not None
    )

    for caminho, descricao in fontes:
        freq_entrada = np.loadtxt(caminho) / ESCALA_BANCO
        freq_entrada = compensar_adiantamento_amostras(
            freq_entrada,
            adiantamento_freq_amostras,
        )
        freq_interpolada = reconstruir_frequencia_interpolada(freq_entrada)

        for offset in range(M):
            freq_frames = alinhar_frequencia_com_banco(
                freq_interpolada,
                n_frames,
                fb_delay,
                offset=offset,
            )

            if usar_referencia:
                estimado = corrigir_fase(
                    saida_sapho,
                    pre_delay,
                    fb_delay,
                    freq_frames,
                    adiantamento_amostras=ajuste_fase_amostras,
                )
                resultado = calcular_metricas(
                    "teste_freq_sapho",
                    estimado,
                    referencia,
                    fb_delay,
                )
                pontuacao = np.mean(resultado["resumo"][:, 5])
            else:
                pontuacao = 0.0

            if melhor is None or pontuacao < melhor["pontuacao"]:
                melhor = {
                    "pontuacao": pontuacao,
                    "caminho": caminho,
                    "descricao": descricao,
                    "offset": offset,
                    "freq_interpolada": freq_interpolada,
                    "freq_frames": freq_frames,
                }

            if not usar_referencia:
                break

    freq_frames = melhor["freq_frames"]
    freq_validos = freq_frames[2 * fb_delay :]

    print("\nFrequencia SAPHO usada na correcao de fase:")
    print(f"  arquivo: {melhor['descricao']}")
    print(f"  ajuste da saida_interp SAPHO: {adiantamento_freq_amostras} amostra(s)")
    print(f"  ajuste fixo de fase SAPHO: {ajuste_fase_amostras} amostra(s)")
    print(f"  amostras na saida interpolada: {melhor['freq_interpolada'].size}")
    print(f"  frames do banco: {freq_frames.size}")
    print(f"  offset na saida interpolada: {melhor['offset']} amostras")
    print(
        "  media/desvio dos frames validos: "
        f"{np.mean(freq_validos):.6f} Hz / {np.std(freq_validos):.6f} Hz"
    )
    if usar_referencia:
        print(f"  TVE medio usado para alinhamento: {melhor['pontuacao']:.6f} %")

    return freq_frames


def corrigir_fase(
    fasores,
    pre_delay,
    fb_delay,
    freq_frames=None,
    adiantamento_amostras=0.0,
):
    """Converte a saida do banco em fasor corrigido, como no fluxo principal."""
    n_frames = fasores.shape[1]
    n_harmonicos = fasores.shape[0]

    magnitude = 2 * np.abs(fasores)
    fase = np.unwrap(np.angle(fasores), axis=1)

    if freq_frames is None:
        freq = F1 * np.ones(n_frames)
    else:
        freq = np.asarray(freq_frames, dtype=float)
        if freq.size < n_frames:
            freq = np.pad(freq, (0, n_frames - freq.size), mode="edge")
        freq = freq[:n_frames]

    delta_f = freq - F0
    correc = np.zeros(n_frames)

    for nn in range(1, n_frames):
        if nn >= fb_delay + 1:
            correc[nn] = (
                correc[nn - 1]
                + np.pi * (delta_f[nn] + delta_f[nn - 1]) * (M * TS)
            )
        else:
            correc[nn] = correc[nn - 1]

    # Nos TXT exportados pelo banco, o termo -pi inverte os harmonicos impares.
    # Por isso mantemos apenas o ajuste do atraso do pre-filtro.
    correc = correc + ((pre_delay - adiantamento_amostras) / N_PPC) * 2 * np.pi

    harmonicos = np.arange(1, n_harmonicos + 1).reshape(-1, 1)
    fase_corrigida = np.unwrap(fase + harmonicos * correc, axis=1)

    return magnitude * np.exp(1j * fase_corrigida)


def calcular_metricas(nome, estimado, referencia, fb_delay):
    """Corta sinais no mesmo tamanho e calcula metricas dos harmonicos impares."""
    n_frames = min(estimado.shape[1], referencia.shape[1])
    n_harmonicos = min(estimado.shape[0], referencia.shape[0])

    estimado = estimado[:n_harmonicos, :n_frames]
    referencia = referencia[:n_harmonicos, :n_frames]

    # Remove o transitorio inicial do banco polifasico.
    inicio = 2 * fb_delay
    estimado = estimado[:, inicio:]
    referencia = referencia[:, inicio:]

    indices_harmonicos = INDICES_HARMONICOS[INDICES_HARMONICOS < n_harmonicos]
    harmonicos_analisados = indices_harmonicos + 1

    estimado = estimado[indices_harmonicos, :]
    referencia = referencia[indices_harmonicos, :]

    mag_est = np.abs(estimado)
    mag_ref = np.abs(referencia)

    fase_est = np.unwrap(np.angle(estimado), axis=1)
    fase_ref = np.unwrap(np.angle(referencia), axis=1)

    erro_mag = 100 * np.abs(mag_est - mag_ref) / mag_ref
    erro_fase = np.abs(wrap_to_pi(fase_est - fase_ref)) * 180 / np.pi
    tve = TVE(estimado, referencia)

    matrizes = {
        "erro_mag": erro_mag,
        "erro_fase": erro_fase,
        "tve": tve,
    }

    for chave, matriz in matrizes.items():
        if not np.all(np.isfinite(matriz)):
            raise ValueError(f"{nome}: matriz {chave} contem NaN ou infinito.")

    resumo = np.column_stack(
        (
            harmonicos_analisados,
            np.mean(erro_mag, axis=1),
            np.max(erro_mag, axis=1),
            np.mean(erro_fase, axis=1),
            np.max(erro_fase, axis=1),
            np.mean(tve, axis=1),
            np.max(tve, axis=1),
        )
    )

    return {
        "nome": nome,
        "n_frames_usados": estimado.shape[1],
        "resumo": resumo,
        "erro_mag": erro_mag,
        "erro_fase": erro_fase,
        "tve": tve,
    }


def salvar_resumo(nome_arquivo, resultado):
    """Salva um TXT com uma linha por harmonico analisado."""
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    cabecalho = (
        "harmonico erro_mag_medio_percent erro_mag_max_percent "
        "erro_fase_medio_graus erro_fase_max_graus tve_medio_percent "
        "tve_max_percent"
    )
    np.savetxt(
        SAIDA_DIR / nome_arquivo,
        resultado["resumo"],
        fmt=["%d", "%.10f", "%.10f", "%.10f", "%.10f", "%.10f", "%.10f"],
        header=cabecalho,
    )


def remover_html_antigo():
    """Remove os HTMLs antigos gerados por versoes anteriores deste script."""
    if not SAIDA_DIR.exists():
        return

    for caminho in SAIDA_DIR.glob("*.html"):
        caminho.unlink()


def salvar_grafico(nome_arquivo, resultado):
    """Salva um grafico PDF com erros medios e maximos por harmonico."""
    resumo = resultado["resumo"]
    harmonicos = resumo[:, 0]

    SAIDA_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(9, 10),
        sharex=True,
        constrained_layout=True,
    )
    fig.suptitle(f"Analise de saida - {resultado['nome']}")

    series = [
        (axes[0], "Erro de magnitude", "Erro (%)", resumo[:, 1], resumo[:, 2], "royalblue"),
        (axes[1], "Erro de fase", "Erro (graus)", resumo[:, 3], resumo[:, 4], "seagreen"),
        (axes[2], "Total Vector Error (TVE)", "TVE (%)", resumo[:, 5], resumo[:, 6], "crimson"),
    ]

    for ax, titulo, ylabel, media, maximo, cor in series:
        ax.plot(harmonicos, media, "o-", color=cor, label="Medio")
        ax.plot(harmonicos, maximo, "o--", color=cor, label="Maximo")
        ax.set_title(titulo)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        ax.legend()

    axes[2].axhline(1.0, color="black", linestyle=":", label="Limite TVE 1%")
    axes[2].legend()
    axes[2].set_xlabel("Harmonico")

    fig.savefig(SAIDA_DIR / nome_arquivo, format="pdf")
    plt.close(fig)

    if ABRIR_GRAFICOS:
        plt.show()


def analisar_saida(
    nome,
    fasores,
    referencia,
    pre_delay,
    fb_delay,
    freq_frames=None,
    adiantamento_amostras=0.0,
):
    """Aplica correcao de fase, calcula metricas e salva resultados."""
    estimado = corrigir_fase(
        fasores,
        pre_delay,
        fb_delay,
        freq_frames,
        adiantamento_amostras=adiantamento_amostras,
    )
    resultado = calcular_metricas(nome, estimado, referencia, fb_delay)
    resultado["fasores_corrigidos"] = estimado

    nome_base = nome.lower().replace(" ", "_")
    salvar_resumo(f"resumo_{nome_base}.txt", resultado)
    salvar_grafico(f"grafico_{nome_base}.pdf", resultado)

    return resultado


def cortar_sinais_para_plot(referencia, python_corrigido, sapho_corrigido, fb_delay):
    """Alinha os tres sinais no menor tamanho comum e remove o transitorio."""
    n_frames = min(
        referencia.shape[1],
        python_corrigido.shape[1],
        sapho_corrigido.shape[1],
    )
    inicio = 2 * fb_delay

    return (
        referencia[:, :n_frames][:, inicio:],
        python_corrigido[:, :n_frames][:, inicio:],
        sapho_corrigido[:, :n_frames][:, inicio:],
    )


def salvar_grafico_harmonicos(referencia, python_corrigido, sapho_corrigido, fb_delay):
    """Plota magnitude e fase de harmonicos escolhidos para ref, Python e SAPHO."""
    referencia, python_corrigido, sapho_corrigido = cortar_sinais_para_plot(
        referencia,
        python_corrigido,
        sapho_corrigido,
        fb_delay,
    )

    SAIDA_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(
        len(HARMONICOS_PLOT),
        2,
        figsize=(13, 12),
        sharex=True,
        constrained_layout=True,
    )
    fig.suptitle("Comparacao Ref x Python x SAPHO")

    sinais = [
        ("Referencia", referencia, "black"),
        ("Python", python_corrigido, "royalblue"),
        ("SAPHO", sapho_corrigido, "crimson"),
    ]

    for linha, harmonico in enumerate(HARMONICOS_PLOT):
        idx = harmonico - 1
        x = np.arange(referencia.shape[1])
        ax_mag = axes[linha, 0]
        ax_fase = axes[linha, 1]

        for nome, sinal, cor in sinais:
            ax_mag.plot(
                x,
                np.abs(sinal[idx, :]),
                color=cor,
                label=nome,
            )
            ax_fase.plot(
                x,
                np.rad2deg(np.unwrap(np.angle(sinal[idx, :]))),
                color=cor,
                label=nome,
            )

        ax_mag.set_title(f"H{harmonico} - magnitude")
        ax_fase.set_title(f"H{harmonico} - fase")
        ax_mag.set_ylabel("Magnitude")
        ax_fase.set_ylabel("Fase (graus)")
        ax_mag.grid(True, alpha=0.3)
        ax_fase.grid(True, alpha=0.3)

    axes[0, 0].legend()
    axes[-1, 0].set_xlabel("Frame")
    axes[-1, 1].set_xlabel("Frame")

    fig.savefig(SAIDA_DIR / "comparacao_ref_python_sapho_harmonicos.pdf", format="pdf")
    plt.close(fig)

    if ABRIR_GRAFICOS:
        plt.show()


def imprimir_resumo(resultado):
    """Mostra no terminal um resumo curto para conferencia rapida."""
    resumo = resultado["resumo"]
    tve_medio_global = np.mean(resumo[:, 5])
    tve_max_global = np.max(resumo[:, 6])

    print(f"\n{resultado['nome']}")
    print(f"  Frames usados apos descartes: {resultado['n_frames_usados']}")
    print(f"  TVE medio global: {tve_medio_global:.6f} %")
    print(f"  TVE maximo global: {tve_max_global:.6f} %")


def main():
    remover_html_antigo()

    pre_delay, zc_m_delay, discard_samples, fb_delay = calcular_atrasos()

    referencia = gerar_referencia(pre_delay, zc_m_delay, discard_samples, fb_delay)
    saida_python = carregar_saida_python()
    saida_sapho = carregar_saida_sapho(saida_python)
    diagnosticar_saida_sapho(saida_sapho, saida_python, fb_delay)
    freq_sapho = preparar_frequencia_sapho(
        saida_sapho.shape[1],
        fb_delay,
        saida_sapho,
        referencia,
        pre_delay,
        ADIANTAMENTO_FREQ_AMOSTRAS_SAPHO,
        AJUSTE_FASE_AMOSTRAS_SAPHO,
    )

    print("Arquivos carregados:")
    print(f"  Python: {saida_python.shape}")
    print(f"  SAPHO:  {saida_sapho.shape}")
    print(f"  Xr:     {referencia.shape}")
    print("\nAtrasos usados:")
    print(f"  pre_delay={pre_delay}")
    print(f"  zc_m_delay={zc_m_delay}")
    print(f"  discard_samples={discard_samples}")
    print(f"  fb_delay={fb_delay}")
    print(f"  adiantamento_freq_amostras_sapho={ADIANTAMENTO_FREQ_AMOSTRAS_SAPHO}")
    print(f"  ajuste_fase_amostras_sapho={AJUSTE_FASE_AMOSTRAS_SAPHO}")

    resultado_python = analisar_saida(
        "python_banco", saida_python, referencia, pre_delay, fb_delay
    )
    resultado_sapho = analisar_saida(
        "sapho_banco",
        saida_sapho,
        referencia,
        pre_delay,
        fb_delay,
        freq_sapho,
        AJUSTE_FASE_AMOSTRAS_SAPHO,
    )
    salvar_grafico_harmonicos(
        referencia,
        resultado_python["fasores_corrigidos"],
        resultado_sapho["fasores_corrigidos"],
        fb_delay,
    )

    imprimir_resumo(resultado_python)
    imprimir_resumo(resultado_sapho)

    print(f"\nResultados salvos em: {SAIDA_DIR}")


if __name__ == "__main__":
    main()
