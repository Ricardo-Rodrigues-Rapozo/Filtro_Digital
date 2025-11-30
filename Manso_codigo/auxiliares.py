
import numpy as np

def TVE(X, Xr):

    X_re = np.real(X)
    X_im = np.imag(X)

    Xr_re = np.real(Xr)
    Xr_im = np.imag(Xr)

    TVE = 100 * np.sqrt(((X_re - Xr_re) ** 2 + (X_im - Xr_im) ** 2) / (Xr_re ** 2 + Xr_im ** 2))

    return TVE


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)


def upsample_with_zeros(signal, factor, target_len=None):
    upsampled = np.zeros(len(signal) * factor)
    upsampled[::factor] = signal

    if target_len is not None:
        if len(upsampled) > target_len:
            upsampled = upsampled[:target_len]  # corta excesso
        elif len(upsampled) < target_len:
            upsampled = np.pad(upsampled, (0, target_len - len(upsampled)))  # completa com zeros

    return upsampled

    return upsampled


def downsample(signal, factor):
    downsampled = signal[::factor]
    return downsampled


def filtro_base(N):

    c5 = [1.0005967, 1.9991048, 1.9097925, 1.4448987, 0.66403725, 0.1304229]

    M = len(c5)
    n = np.arange(-(N - 1) / 2, 1 + (N - 1) / 2, 1)

    wM = np.zeros(N)
    for m in range(M):
        wM = wM + c5[m] * np.cos(m * (2 * np.pi / N) * n)

    wM = wM / np.sum(wM)

    return wM