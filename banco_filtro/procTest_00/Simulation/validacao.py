import numpy as np
import matplotlib.pyplot as plt

out = np.loadtxt("output_1.txt")

real = out[0::2]
imag = out[1::2]

fasores = real + 1j*imag

N = len(fasores)//50
fasores = fasores[0:50*N]

fasor_h = fasores.reshape(50, N, order='F')

mag = np.abs(fasor_h)
ang = np.angle(fasor_h)

plt.figure()
plt.subplot(2,2,1)
plt.plot(mag[1,:], marker='o', linestyle='-')
plt.title('Fundamental Magnitude')

plt.subplot(2,2,2)
plt.plot(mag[3,:], marker='o', linestyle='-')
plt.title('3rd Magnitude')

plt.subplot(2,2,3)
plt.plot(mag[5,:], marker='o', linestyle='-')
plt.title('5th Magnitude')

plt.subplot(2,2,4)
plt.plot(mag[7,:], marker='o', linestyle='-')
plt.title('7th Magnitude')

plt.show(block=False)

plt.figure()
plt.subplot(2,2,1)
plt.plot(ang[1,:], marker='o', linestyle='-')
plt.title('Fundamental Phase')

plt.subplot(2,2,2)
plt.plot(ang[3,:], marker='o', linestyle='-')
plt.title('3rd Phase')

plt.subplot(2,2,3)
plt.plot(ang[5,:], marker='o', linestyle='-')
plt.title('5th Phase')

plt.subplot(2,2,4)
plt.plot(ang[7,:], marker='o', linestyle='-')
plt.title('7th Phase')

plt.show()

