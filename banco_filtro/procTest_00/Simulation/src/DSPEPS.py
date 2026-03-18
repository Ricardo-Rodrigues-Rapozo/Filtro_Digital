import numpy as np
from scipy.signal import firls, lfilter, freqz, group_delay
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
    
    N = 4 * Nppc      # filter order
    Fpass = 70         
    Fstop = 120       
    Wpass = 1
    Wstop = 1

    b = firls(N+1, [0, Fpass, Fstop, Fs / 2], [1, 1, 0, 0], weight=[Wpass, Wstop], fs=Fs)
    
    # Frequency Response and Group Delay Plot
    # ------------------------------------------------
    
    f, H = freqz(b, worN=4096, fs=Fs)
    w_gd, gd = group_delay((b,1), w=4096)
    
    if plot_level >= 1:
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude (dB)", "Phase (graus)", "Group Delay (samples)"))

        fig.add_trace(go.Scatter(x=f, y=abs(H), mode='lines', name='Magnitude'), row=1, col=1)
        fig.add_trace(go.Scatter(x=f, y=np.unwrap(np.angle(H))*180/np.pi, mode='lines', name='Phase'), row=2, col=1)
        fig.add_trace(go.Scatter(x=f, y=gd, mode='lines', name='Delay'), row=3, col=1)
        fig.update_yaxes(range=[np.mean(gd) - 1, np.mean(gd) + 1], row=3, col=1)
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
    
    # ================================================
    # Filter Application
    # ================================================
    
    v = lfilter(b, [1.0], s)
    
    # ================================================
    # Zero Crossing Detection
    # ================================================    
    va = 0.0
    Tsc = 1 / 60.0  
    T1 = 0.0
    
    cnt = 0
    f_zc = []
    for ii in range(len(v)):
        if va >= 0:
            sig = va * v[ii]
        else:
            sig = 1

        Tsc += Ts
        cnt += 1

        if sig < 0:  # houve cruzamento
            Nb = v[ii] / (v[ii] - va)
            T2 = Nb * Ts
            Tsc = Tsc + T1 - T2
            f_zc.extend([1 / Tsc] * cnt)
            T1 = T2
            Tsc = 0
            cnt = 0

        va = v[ii]

    
    if len(f_zc) < len(v):
        f_zc.extend([f_zc[-1]] * (len(v) - len(f_zc)))

    f_zc = np.array(f_zc)
    
    # ================================================
    # Smoothing Moving Average Filter
    # ================================================
    
    Nw = 4 * Nppc
    w = np.ones(Nw) / Nw
    f_zc_m = lfilter(w, 1, f_zc)

    shift = int(np.fix((Nw + N) / 2))
    if shift < len(f_zc_m):
        f_zc_m = np.concatenate((f_zc_m[shift:], [f_zc_m[-1]] * shift))
    else:
        f_zc_m = np.array([f_zc_m[-1]] * len(f_zc_m))

    return f_zc, f_zc_m


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
    y = []

    for nn in range(len(x_pre)):
        
        if f[nn] != 0:        
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
                
                alfa += lamb
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

    f = np.asarray(f).ravel()
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
    x[0, 0] = 60.0
    P = 1e6 * np.eye(M)

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