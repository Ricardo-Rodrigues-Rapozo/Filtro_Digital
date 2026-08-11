import numpy as np
from scipy.io import loadmat
from scipy.signal import butter, buttord, lfilter, sos2tf, sosfilt, freqz, sosfreqz, group_delay, firls, bessel, bilinear, tf2sos
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def downsample(signal, factor):
    signal = np.asarray(signal)
    downsampled = signal[..., ::factor]  # preserva todas as dimensões anteriores
    return downsampled

def estima_f_zc(s, Ts, Nppc, plot_level=0):
    """
    Zero Crossing Frequency Estimation
    
    Input:
        s : array_like
            Input Signal (1D)
        Ts : float
            Sampling Period (s)
        Nppc : int
            Numper of samples per cycle
        plot_level : int, optional
            Controls the generation of intermediate results graphics

        * 0 : No plots are generated (default).
        * 1 : Plots results.
    
    Output:
        f_zc : ndarray
            Estimated Frequency (Hz)
        f_zc_m : ndarray
            Shooth Frequency (Hz)
    """
    
    Fs = 1 / Ts  # Sampling Frequency

    # ================================================
    # Harmonic Rejection Filter Project
    # ================================================
    
    # N = 4 * Nppc      # filter order
    # Fpass = 70         
    # Fstop = 90       
    # Wpass = 1
    # Wstop = 1

    # b = firls(N+1, [0, Fpass, Fstop, Fs / 2], [1, 1, 0, 0], weight=[Wpass, Wstop], fs=Fs)
    # a = [1.0]
    
    # nutall = loadmat("Num_Nutall.mat")
    # b = np.squeeze(nutall["Num_Nutall"])
    # np.s avetxt('b_coeffs.txt', b, fmt='%.18e')
    
    b, a = bessel(6, 2*np.pi*90, analog=True)
    b, a = bilinear(b, a, fs=Fs)  
    print(f"Pre-filter coefficients (b): {b}")
    print(f"Pre-filter coefficients (a): {a}")

    sos = tf2sos(b, a)
    sos_num_gain = np.max(np.abs(sos[:, :3]), axis=1)
    sos_target_gain = np.prod(sos_num_gain) ** (1 / sos.shape[0])
    sos[:, :3] *= (sos_target_gain / sos_num_gain)[:, np.newaxis]

    for i, section in enumerate(sos, start=1):
        print(f"Pre-filter SOS section {i} [b0, b1, b2, a0, a1, a2]: {section}")   
    
    # Frequency Response and Group Delay Plot
    # ------------------------------------------------
    
    f, H = freqz(b, a, worN=4096, fs=Fs)
    w_gd, gd = group_delay((b,a), w=4096, fs=Fs)
    freq_alvo = 60  # Hz

    # Encontrar o índice mais próximo de 60 Hz
    idx = np.argmin(np.abs(w_gd - freq_alvo))
    gd_60hz = gd[idx]
    
    if plot_level >= 1:
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude (dB)", "Phase (graus)", "Group Delay (samples)"))

        fig.add_trace(go.Scatter(x=f, y=abs(H), mode='lines', name='Magnitude'), row=1, col=1)
        fig.add_trace(go.Scatter(x=f, y=np.unwrap(np.angle(H))*180/np.pi, mode='lines', name='Phase'), row=2, col=1)
        fig.add_trace(go.Scatter(x=f, y=gd, mode='lines', name='Delay'), row=3, col=1)
        # fig.update_yaxes(range=[np.mean(gd) - 1, np.mean(gd) + 1], row=3, col=1)
        fig.update_xaxes(title_text='Frequency (Hz)', row=3, col=1)
        fig.update_yaxes(title_text='Nomalized', row=1, col=1)
        fig.update_yaxes(title_text='Degrees', row=2, col=1)
        fig.update_yaxes(title_text='Samples', row=3, col=1)
        
        fig.update_layout(
        autosize=True,
        title_text="Zero Crossing Pre-Filter",
        title_font=dict(size=24, family='Arial', color='black'),  
        title_x=0.5,  
        template='gridon'
        )

        fig.show()

        zeros = np.roots(b)
        poles = np.roots(a)
        theta = np.linspace(0, 2*np.pi, 512)

        fig_pz = go.Figure()
        fig_pz.add_trace(go.Scatter(
            x=np.cos(theta),
            y=np.sin(theta),
            mode='lines',
            name='Unit circle',
            line=dict(color='gray', dash='dash')
        ))
        fig_pz.add_trace(go.Scatter(
            x=zeros.real,
            y=zeros.imag,
            mode='markers',
            name='Zeros',
            marker=dict(symbol='circle-open', size=12, color='royalblue', line=dict(width=2))
        ))
        fig_pz.add_trace(go.Scatter(
            x=poles.real,
            y=poles.imag,
            mode='markers',
            name='Poles',
            marker=dict(symbol='x', size=12, color='crimson', line=dict(width=2))
        ))

        fig_pz.update_layout(
            autosize=True,
            title_text="Pole-Zero Diagram - Zero Crossing Pre-Filter",
            title_font=dict(size=24, family='Arial', color='black'),
            title_x=0.5,
            template='gridon',
            xaxis=dict(title='Real', scaleanchor='y', scaleratio=1),
            yaxis=dict(title='Imaginary'),
            legend=dict(font=dict(size=18))
        )

        fig_pz.show()
    
    # ================================================
    # Filter Application
    # ================================================
    
    v = sosfilt(sos, s)
    
    # ================================================
    # Zero Crossing Detection
    # ================================================    
    va = 0.0
    Tsc = 1 / 60.0  
    T1 = 0.0
    
    cnt = 0
    f_zc = []
    f = 60
    for ii in range(len(v)):
        #if va >= 0:
        sig = va * v[ii]
        #else:
        #    sig = 1

        Tsc += Ts
        cnt += 1

        if sig < 0:  # houve cruzamento
            Nb = v[ii] / (v[ii] - va)
            T2 = Nb * Ts
            Tsc = Tsc + T1 - T2
            # f_zc.extend([1 / (2*Tsc)] * cnt)
            f = 1 / (2*Tsc)
            T1 = T2
            Tsc = 0
            cnt = 0

        va = v[ii]
        f_zc.append(f)## frequência ZC
    # f_zc = np.array(f_zc)
    
    # ================================================
    # Smoothing Moving Average Filter
    # ================================================
    
    # Nw = 1 * Nppc
    # w = np.ones(Nw) / Nw
    # f_zc_m = lfilter(w, 1, f_zc)
    # # f_zc_m = sosfilt(sos, f_zc)
    
    # pre_delay = gd_60hz #len(b)//2
    # zc_delay = pre_delay + Nppc//2
    # # zc_m_delay = gd_60hz + zc_delay
    # zc_m_delay = Nw//2 + zc_delay
    # print(f"Pre-filter delay: {pre_delay} samples")
    # print(f"Zero Crossing delay: {zc_delay} samples")   
    # print(f"Smoothed Zero Crossing delay: {zc_m_delay} samples")
    
    
    # bsvz, asvz = bessel(6, 2*np.pi*20, analog=True)
    # bsvz, asvz = bilinear(bsvz, asvz, fs=Fs)  
    # # normalização para ganho unitário em DC
    # w, h = freqz(bsvz, asvz, worN=[0])
    # gain = abs(h[0])
    # print(f"Pre-filter gain at DC: {gain}")
    # bsvz = bsvz / (gain)
    
    
    # # Frequency Response and Group Delay Plot   
    # # ------------------------------------------------
    # f, H = freqz(bsvz, asvz, worN=4096, fs=Fs)
    # w_gd, gd = group_delay((bsvz, asvz), w=4096, fs=Fs)
    # freq_alvo = 0  # Hz

    # # Encontrar o índice mais próximo de 60 Hz
    # idx = np.argmin(np.abs(w_gd - freq_alvo))
    # gd_0hz = gd[idx]
    
    # if plot_level >= 1:
    #     fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude (dB)", "Phase (graus)", "Group Delay (samples)"))

    #     fig.add_trace(go.Scatter(x=f, y=abs(H), mode='lines', name='Magnitude'), row=1, col=1)
    #     fig.add_trace(go.Scatter(x=f, y=np.unwrap(np.angle(H))*180/np.pi, mode='lines', name='Phase'), row=2, col=1)
    #     fig.add_trace(go.Scatter(x=f, y=gd, mode='lines', name='Delay'), row=3, col=1)
    #     # fig.update_yaxes(range=[np.mean(gd) - 1, np.mean(gd) + 1], row=3, col=1)
    #     fig.update_xaxes(title_text='Frequency (Hz)', row=3, col=1)
    #     fig.update_yaxes(title_text='Nomalized', row=1, col=1)
    #     fig.update_yaxes(title_text='Degrees', row=2, col=1)
    #     fig.update_yaxes(title_text='Samples', row=3, col=1)
        
    #     fig.update_layout(
    #     autosize=True,
    #     title_text="Zero Crossing Pre-Filter",
    #     title_font=dict(size=24, family='Arial', color='black'),  
    #     title_x=0.5,  
    #     template='gridon'
    #     )

    #     fig.show()

    #     zeros = np.roots(bsvz)
    #     poles = np.roots(asvz)
    #     theta = np.linspace(0, 2*np.pi, 512)

    #     fig_pz = go.Figure()
    #     fig_pz.add_trace(go.Scatter(
    #         x=np.cos(theta),
    #         y=np.sin(theta),
    #         mode='lines',
    #         name='Unit circle',
    #         line=dict(color='gray', dash='dash')
    #     ))
    #     fig_pz.add_trace(go.Scatter(
    #         x=zeros.real,
    #         y=zeros.imag,
    #         mode='markers',
    #         name='Zeros',
    #         marker=dict(symbol='circle-open', size=12, color='royalblue', line=dict(width=2))
    #     ))
    #     fig_pz.add_trace(go.Scatter(
    #         x=poles.real,
    #         y=poles.imag,
    #         mode='markers',
    #         name='Poles',
    #         marker=dict(symbol='x', size=12, color='crimson', line=dict(width=2))
    #     ))

    #     fig_pz.update_layout(
    #         autosize=True,
    #         title_text="Pole-Zero Diagram - Zero Crossing Pre-Filter",
    #         title_font=dict(size=24, family='Arial', color='black'),
    #         title_x=0.5,
    #         template='gridon',
    #         xaxis=dict(title='Real', scaleanchor='y', scaleratio=1),
    #         yaxis=dict(title='Imaginary'),
    #         legend=dict(font=dict(size=18))
    #     )

    #     fig_pz.show()
    
    # # ================================================
    # # Filter Application
    # # ================================================
    
    # f_zc_m = lfilter(bsvz, asvz, f_zc)*58/58.53
    
    f_zc_m = f_zc
    pre_delay = gd_60hz 
    zc_delay =  Nppc//2
    zc_m_delay = 0 
    total_delay = int(np.ceil(pre_delay + zc_delay + zc_m_delay))
    
    print(f"Pre-filter delay: {pre_delay} samples")
    print(f"Zero Crossing delay: {zc_delay} samples")   
    print(f"Smoothed Zero Crossing delay: {zc_m_delay} samples")
    print(f"Total estimated delay: {total_delay} samples")
    
    return f_zc_m, zc_m_delay, f_zc, zc_delay, total_delay
def BSplineInterp(x, f0, f, M, Fs, plot_level=0):
    """
    B-spline Interpolation using Farrow Structure 
    
    Inputs:
        x  : array_like - input signal
        f0 : float      - nominal frequency
        f  : array_like - actual frequencya (same size as x)
        M  : int        - pre-filter order
        plot_level : int, optional
            Controls the generation of intermediate results graphics

        * 0 : No plots are generated (default).
        * 1 : Plots results.
    
    Output:
        y : array - interpolated signal
    """
    
    x = np.asarray(x)
    f = np.asarray(f)
    
    # ================================================
    # Pre-filter
    # ================================================
    s = np.sqrt(3) - 2.0
    exps = np.arange(1, M+2)           # [1, 2, ..., M+1]
    
    num_pre = -6.0 * (s ** exps)[::-1] # fliplr equivalent
    den_pre = np.array([1.0, -s])
    
    # Frequency Response and Group Delay Plot
    # ------------------------------------------------
    
    fh, H = freqz(num_pre, den_pre, worN=4096, fs=Fs)
    w_gd, gd = group_delay((num_pre, den_pre), w=4096)
    
    
    if plot_level >= 1:
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude (dB)", "Phase (graus)", "Group Delay (samples)"))

        fig.add_trace(go.Scatter(x=fh, y=abs(H), mode='lines', name='Magnitude)'), row=1, col=1)
        fig.add_trace(go.Scatter(x=fh, y=np.unwrap(np.angle(H))*180/np.pi, mode='lines', name='Phase'), row=2, col=1)
        fig.add_trace(go.Scatter(x=fh, y=gd, mode='lines', name='Delay'), row=3, col=1)
        fig.update_yaxes(range=[np.mean(gd) - 1, np.mean(gd) + 1], row=3, col=1)
        fig.update_xaxes(title_text='Frequency (Hz)', row=3, col=1)
        fig.update_yaxes(title_text='Nomalized', row=1, col=1)
        fig.update_yaxes(title_text='Degrees', row=2, col=1)
        fig.update_yaxes(title_text='Samples', row=3, col=1)
        
        fig.update_layout(
        autosize=True,
        title_text="BSpline Pre-Filter",
        title_font=dict(size=24, family='Arial', color='black'),  
        title_x=0.5,  
        template='gridon'
        )

        fig.show()
    
    # Pre-Filter Application
    # ------------------------------------------------
    x_pre = lfilter(num_pre, den_pre, x)
    
    # compensate pre-filter delay
    delay = np.zeros(M+2)
    delay[-1] = 1.0
    f = lfilter(delay, [1.0], f)
    
    # ================================================
    # Farrow Structure
    # ================================================
    buffer_farrow = np.zeros(4, dtype=float)
    alfa = 0.0
    lamb_ant = 0.0
    y = []

    for nn in range(len(x_pre)):
        
        if f[nn] != 0:        
            # lamb = f0 / (np.fix(f[nn]*(2**23))/(2**23)) 
            lamb = f0 / f[nn] 
        else: 
            0
            
        buffer_farrow = np.roll(buffer_farrow, -1)
        buffer_farrow[-1] = x_pre[nn]

        if nn >= (M+2):
            while alfa < 1.0:
                H0 = (-1.0/6.0)*buffer_farrow[0] + 0.5*buffer_farrow[1] - 0.5*buffer_farrow[2] + (1.0/6.0)*buffer_farrow[3]
                H1 = 0.5*buffer_farrow[0] - buffer_farrow[1] + 0.5*buffer_farrow[2]
                H2 = -0.5*buffer_farrow[0] + 0.5*buffer_farrow[2]
                H3 = (1.0/6.0)*buffer_farrow[0] + (2.0/3.0)*buffer_farrow[1] + (1.0/6.0)*buffer_farrow[2]

                x_int = (alfa**3)*H0 + (alfa**2)*H1 + alfa*H2 + H3
                y.append(x_int)
                
                # alfa += (lamb + lamb_ant) / 2.0
                alfa += lamb
                lamb_ant = lamb
            alfa -= 1.0
    
    y = np.array(y)
    return y 

def FlatTopFilterBank(x, f0, hmax, Fs):
    
    # ================================================
    # Calculo do Filtro Base
    # ================================================
    
    c5 = [1.0005967, 1.9991048, 1.9097925, 1.4448987, 0.66403725, 0.1304229]

    M = len(c5)
    N = 13*(Fs//f0)+1
    n = np.arange(-(N - 1) / 2, 1 + (N - 1) / 2, 1)

    wM = np.zeros(N)
    for m in range(M):
        wM = wM + c5[m] * np.cos(m * (2 * np.pi / N) * n)

    wM = wM / np.sum(wM)
    
    v_list = []
    for hh in range(1, hmax + 1):  
        wMh = wM*np.exp(1j*2*np.pi*hh*f0*n/Fs)
        v_hh = lfilter(wMh, 1, x)  
        v_list.append(v_hh)
    
    v = np.array(v_list)
    # v = v[:,N//2:]
    
    return v

def FlatTopFilterBase(N):    
    # ================================================
    # Calculo do Filtro Base
    # ================================================
    
    c5 = [1.0005967, 1.9991048, 1.9097925, 1.4448987, 0.66403725, 0.1304229]

    M = len(c5)
    n = np.arange(-(N - 1) / 2, 1 + (N - 1) / 2, 1)

    wM = np.zeros(N)
    for m in range(M):
        wM = wM + c5[m] * np.cos(m * (2*np.pi / N) * n)

    wM = wM / np.sum(wM)
    
    return wM

def PolyphaseFilterBank(h, M, x):
    #===================================================
    # Decomposição Polifásica
    #===================================================

    Nf = int(np.ceil(len(h)/M))
    E = np.zeros((M, Nf))

    for kk in range(M):
        hh = np.array(h[kk::M])          # transforma em numpy array
        hh_padded = np.pad(hh, (0, Nf - len(hh)), 'constant')  # completa com zeros à direita
        E[kk, :] = hh_padded  
        
    #===================================================
    # Aplicação dos Filtros
    #===================================================

    Eout = np.zeros((M,len(x)//M))
    for mm in range(M):    
        
        x_slice = x[0:len(x)-mm]
        zeros = np.zeros(mm, dtype=x.dtype)
        
        xxa = np.concatenate((zeros, x_slice)) 

        xx = downsample(xxa, M)
        
        Eout[mm,:] = lfilter(E[mm],1,xx)
        
    #===================================================
    # Aplicação da IDFT
    #===================================================

    v = np.zeros((M,len(x)//M), dtype=complex)

    for nn in range(len(x)//M):
        v[:,nn] = M*np.fft.ifft(Eout[:,nn])
        
    return v

def kf_trend_poly(f, Ts, order, q, r):
    """
    kf_trend_poly
    Estima tendência polinomial (ordem 0/1/2) em f[k] via Filtro de Kalman.

    Modelo:
        y_k     = b_k + (senoide desconhecida) + ruído
        x_{k+1} = F x_k + w_k
        y_k     = H x_k + v_k

    Parâmetros:
        f     : vetor de amostras (1D array)
        Ts    : período de amostragem
        order : 0 (constante), 1 (linear), 2 (quadrático)
        q     : intensidade do ruído de processo
        r     : variância do ruído de medição efetivo

    Retorno (dict):
        out['b']     : tendência estimada
        out['db']    : 1a derivada (se order >= 1)
        out['ddb']   : 2a derivada (se order == 2)
        out['x']     : estados estimados (M x N)
        out['Pdiag'] : diagonal de P ao longo do tempo (M x N)
    """

    f = np.asarray(f).ravel() ## garante que f seja um vetor 1D
    N = f.size

    # Define F, H, Q conforme a ordem
    if order == 0:
        F = np.array([[1.0]])
        H = np.array([[1.0]])
        Q = np.array([[q]])     # random walk
        M = 1

    elif order == 1:
        F = np.array([[1.0, Ts], [0.0, 1.0]])
        H = np.array([[1.0, 0.0]])
        Q = q * np.array([[Ts**3/3, Ts**2/2], [Ts**2/2, Ts]])
        M = 2

    elif order == 2:
        F = np.array([[1.0, Ts, Ts**2/2], [0.0, 1.0, Ts], [0.0, 0.0, 1.0]])
        H = np.array([[1.0, 0.0, 0.0]])
        Q = q * np.array([[Ts**5/20, Ts**4/8,  Ts**3/6], [Ts**4/8,  Ts**3/3,  Ts**2/2], [Ts**3/6,  Ts**2/2,  Ts]])
        M = 3

    else:
        raise ValueError("order deve ser 0, 1 ou 2.")

    R = r

    # Inicialização
    x = np.zeros((M, 1))
    x[0, 0] = 63
    P = 1e6 * np.eye(M)  ## cria uma matriz identidade de tamanho MxM e multiplica por 1e6 para definir a incerteza inicial alta

    x_hist = np.zeros((M, N))
    Pdiag = np.zeros((M, N))

    # Loop do Filtro de Kalman
    for k in range(N):
        # Predição
        x = F @ x
        P = F @ P @ F.T + Q

        # Atualização
        y = f[k]
        S = H @ P @ H.T + R
        K = (P @ H.T) / S
        e = y - (H @ x)[0, 0]

        x = x + K * e
        P = (np.eye(M) - K @ H) @ P

        x_hist[:, k] = x.ravel()
        Pdiag[:, k] = np.diag(P)

    out = {
        "x": x_hist,
        "Pdiag": Pdiag,
        "b": x_hist[0, :].reshape(-1, 1)
    }

    if order >= 1:
        out["db"] = x_hist[1, :].reshape(-1, 1)
    if order == 2:
        out["ddb"] = x_hist[2, :].reshape(-1, 1)

    return out




def Kalman_filter(f, Ts, order, q, r):
    """
    Filtro de Kalman em baixo nivel para o caso de ordem 1.

    Este codigo faz a mesma ideia do caso:

        x = [frequencia]
            [ROCOF     ]

    mas sem escrever as contas como multiplicacao de matrizes.

    Entradas:
        f     : frequencia medida pelo zero-crossing, amostra por amostra
        Ts    : periodo de amostragem
        order : por enquanto esta funcao escalar implementa apenas order = 1
        q     : intensidade do ruido de processo
        r     : variancia do ruido de medicao

    Saidas:
        fout : frequencia estimada pelo Kalman
        df   : ROCOF estimado pelo Kalman
    """


    # Garante vetor 1D em ponto flutuante. Isso evita perda de casas decimais
    # caso f venha como inteiro.
    f = np.asarray(f, dtype=float).ravel()

    # Vetores de saida: guardam o estado corrigido em cada amostra.
    fout = np.zeros_like(f, dtype=float)  # frequencia estimada
    df = np.zeros_like(f, dtype=float)    # derivada da frequencia, ou ROCOF

    # Estados internos do filtro.
    # freq  corresponde a x[0].
    # rocof corresponde a x[1].
    freq = 60.0
    freq = 60
    rocof = 0.0

    # Matriz P aberta em quatro escalares:
    #
    #     P = [p00 p01]
    #         [p10 p11]
    #
    # p00: incerteza da frequencia.
    # p11: incerteza do ROCOF.
    # p01/p10: acoplamento entre erro de frequencia e erro de ROCOF.
    #
    # Comeca grande porque no inicio o filtro ainda nao confia no estado
    # inicial escolhido acima.
    p00 = 1e6
    p01 = 0.0
    p10 = 0.0
    p11 = 1e6

    # Matriz Q aberta em escalares. Esta e a mesma Q usada no modelo
    # matricial de ordem 1:
    #
    #     Q = q * [Ts^3/3  Ts^2/2]
    #             [Ts^2/2  Ts    ]
    #
    # Q representa o quanto aceitamos que o modelo "freq + Ts*rocof"
    # esteja errado entre uma amostra e outra.
    q00 = q * Ts**3 / 3.0
    q01 = q * Ts**2 / 2.0
    q10 = q * Ts**2 / 2.0
    q11 = q * Ts

    # R e a variancia do ruido de medicao. Aqui a medicao e f[i].
    R = r

    for i in range(len(f)):
        # ==============================================================
        # 1) Predicao do estado
        # ==============================================================
        # Modelo:
        #     freq[k]  = freq[k-1] + Ts * rocof[k-1]
        #     rocof[k] = rocof[k-1]
        #
        # Esta e a forma escalar de:
        #     x = F @ x
        freq_pred = freq + Ts * rocof
        rocof_pred = rocof

        # ==============================================================
        # 2) Predicao da incerteza P
        # ==============================================================
        # Esta e a forma escalar de:
        #     P = F @ P @ F.T + Q
        #
        # com:
        #     F = [1 Ts]
        #         [0  1]
        p00_pred = p00 + Ts*p10 + Ts*p01 + Ts*Ts*p11 + q00
        p01_pred = p01 + Ts*p11 + q01
        p10_pred = p10 + Ts*p11 + q10
        p11_pred = p11 + q11

        # ==============================================================
        # 3) Medicao do "sensor"
        # ==============================================================
        # No seu projeto, f[i] e a frequencia medida pelo zero-crossing.
        y = f[i]

        # ==============================================================
        # 4) Erro de predicao, tambem chamado inovacao
        # ==============================================================
        # H = [1 0], entao H*x pega apenas a frequencia prevista.
        #
        # Forma matricial:
        #     erro = y - (H @ x)[0, 0]
        erro = y - freq_pred

        # ==============================================================
        # 5) Incerteza da inovacao
        # ==============================================================
        # Forma matricial:
        #     S = H @ P @ H.T + R
        #
        # Como H = [1 0], isso vira apenas:
        #     S = p00_pred + R
        S = p00_pred + R

        # ==============================================================
        # 6) Ganho de Kalman
        # ==============================================================
        # Forma matricial:
        #     K = (P @ H.T) / S
        #
        # Como H.T = [1; 0], isso vira:
        #     K0 = p00_pred / S
        #     K1 = p10_pred / S
        #
        # K0 corrige a frequencia.
        # K1 corrige o ROCOF.
        K0 = p00_pred / S
        K1 = p10_pred / S

        # ==============================================================
        # 7) Correcao do estado
        # ==============================================================
        # Forma matricial:
        #     x = x + K * erro
        #
        # Forma escalar:
        #     freq  = freq_pred  + K0 * erro
        #     rocof = rocof_pred + K1 * erro
        freq = freq_pred + K0 * erro
        rocof = rocof_pred + K1 * erro

        # ==============================================================
        # 8) Correcao da incerteza P
        # ==============================================================
        # Forma matricial:
        #     P = (I - K @ H) @ P
        #
        # Com H = [1 0] e K = [K0; K1], a matriz (I - K@H) fica:
        #
        #     [1-K0   0]
        #     [-K1    1]
        #
        # Multiplicando essa matriz por P_pred, obtemos:
        p00 = (1.0 - K0) * p00_pred
        p01 = (1.0 - K0) * p01_pred
        p10 = p10_pred - K1 * p00_pred
        p11 = p11_pred - K1 * p01_pred

        # ==============================================================
        # 9) Salva as saidas deste instante
        # ==============================================================
        # Estas duas variaveis sao o estado corrigido pelo Kalman.
        fout[i] = freq
        df[i] = rocof

    return fout, df
