import numpy as np
from scipy.signal import firls, lfilter, freqz, group_delay
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def downsample(signal, factor):
    signal = np.asarray(signal)
    downsampled = signal[..., ::factor]  # preserva todas as dimensões anteriores
    return downsampled

def estima_f_zc(s, Ts, Nppc):
    """
    Zero Crossing Frequency Estimation
    
    Input:
        s : array_like
            Input Signal (1D)
        Ts : float
            Sampling Period (s)
        Nppc : int
            Numper of samples per cycle
    
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
    
    
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Magnitude (dB)", "Phase (graus)", "Group Delay (samples)"))

    fig.add_trace(go.Scatter(x=f, y=abs(H), mode='lines', name='Magnitude)'), row=1, col=1)
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
    
    Nw = 2 * Nppc
    w = np.ones(Nw) / Nw
    f_zc_m = lfilter(w, 1, f_zc)

    shift = int(np.fix((Nw + N) / 2))
    if shift < len(f_zc_m):
        f_zc_m = np.concatenate((f_zc_m[shift:], [f_zc_m[-1]] * shift))
    else:
        f_zc_m = np.array([f_zc_m[-1]] * len(f_zc_m))

    return f_zc, f_zc_m


def BSplineInterp(x, f0, f, M, Fs):
    """
    B-spline Interpolation using Farrow Structure 
    
    Inputs:
        x  : array_like - input signal
        f0 : float      - nominal frequency
        f  : array_like - actual frequencya (same size as x)
        M  : int        - pre-filter order
    
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
    v = v[:,N//2:]
    
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
        wM = wM + c5[m] * np.cos(m * (2 * np.pi / N) * n)

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
        debug = 0
    #===================================================
    # Aplicação da IDFT
    #===================================================

    v = np.zeros((M,len(x)//M), dtype=complex)

    for nn in range(len(x)//M):
        v[:,nn] = M*np.fft.ifft(Eout[:,nn])
  
    return v