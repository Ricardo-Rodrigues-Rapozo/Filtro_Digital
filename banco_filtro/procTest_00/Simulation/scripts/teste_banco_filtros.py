import numpy as np


np.set_printoptions(precision=4, suppress=True)

M = 4
h = np.array([1.0, 2.0, 3.0, 4.0, 10.0, 20.0, 30.0, 40.0], dtype=float)
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=float)

Nf = len(h) // M
Ehh = np.zeros((M, Nf))

for kk in range(M):
    Ehh[kk, :] = h[kk::M]

buffer = np.zeros(M)
E = np.zeros((M, Nf))

print("=== DADOS DO TESTE ===")
print("Entrada x =", x)
print("Filtro h =", h)
print("Matriz polifasica Ehh =")
print(Ehh)

for nn in range(len(x)):
    for kk in range(M - 1):
        buffer[M - 1 - kk] = buffer[M - 2 - kk]
    buffer[0] = x[nn]

    if (nn % M) == 0:
        E0 = np.zeros(M)

        for mm in range(M):
            for kk in range(Nf - 1, 0, -1):
                E[mm, kk] = E[mm, kk - 1]
            E[mm, 0] = buffer[mm]
            E0[mm] = np.dot(Ehh[mm, :], E[mm, :])

        vv = M * np.fft.ifft(E0)

        print(f"dd=== BLOCO nn = {nn} ===")
        print("buffer =")
        print(buffer)
        print("E =")
        print(E)
        print("E0 =")
        print(E0)
        print("vv =")
        print(vv)


print("\n=== GABARITO PARA CONFERIR NO OLHO ===")
print("No bloco nn = 0:")
print("buffer esperado = [1. 0. 0. 0.]")
print("E esperado =")
print(np.array([[1., 0.],
                [0., 0.],
                [0., 0.],
                [0., 0.]]))
print("E0 esperado = [1. 0. 0. 0.]")
print("vv esperado = [1.+0.j 1.+0.j 1.+0.j 1.+0.j]")

print("\nNo bloco nn = 4:")
print("buffer esperado = [5. 4. 3. 2.]")
print("E esperado =")
print(np.array([[5., 1.],
                [4., 0.],
                [3., 0.],
                [2., 0.]]))
print("E0 esperado = [15.  8.  9.  8.]")
print("vv esperado = [40.+0.j  6.+0.j  8.+0.j  6.+0.j]")
