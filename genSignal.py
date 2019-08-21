import matplotlib.pyplot as plt
import numpy as np
from pylab import mean, ceil,  log10, arange, fft
from pylab import plot, subplot, xlabel, ylabel

# Este script genera dos señales de frecuencias distintas y arbitrarias,
# luego las multiplica. Para cada señal se grafica en tiempo y en frecuencia

def grafica(time, channel, titulo):
    plot(time, channel)
    ylabel('Amplitude')
    xlabel('Time (s) ' + str(titulo))
    plt.show()


def hacerfft(channel, freq):          # en Hz
    fdata = fft(channel)

    print('> FFT realizada: ' + str(freq))
        
    nUniquePts = int(ceil((N)/2))
    fdata = fdata[0:nUniquePts]
    fdata = abs(fdata)

    fdata = fdata/float(N)
    fdata = fdata**2

    if N % 2 > 0:
        fdata[1:int(ceil(len(fdata)))] = fdata[1:int(ceil(len(fdata)))] * 2
    else:
        fdata[1:int(ceil(len(fdata)))-1] = fdata[1:int(ceil(len(fdata)))-1] * 2

    freqArray = arange(0, nUniquePts, 1.0)*(fs/N)
    plot(freqArray, 10*log10(fdata[0:int(N):1]))

    xlabel('Frequency (Hz)')
    ylabel('Power (dB)')
    plt.show()

    print('> FFT graficada ' + str(freq))

    return fdata

# Inicialización de datos: Frecuencia, Cantidad de Datos, Tiempo
fs = 10e3           # = 10000.0
N = 1e3             # = 1000.0
time = np.arange(N) / fs

# Señal 1, frecuencia y amplitud. Acá se puede modificar según el tipo de modulación
amp = 2*np.sqrt(2)
freq1 = 200.0
x = 8 + amp*np.sin(2*np.pi*freq1*time)

titulo1 = " | Gráfica en " + str(freq1) + " Hz"

grafica(time, x, titulo1)

hacerfft(x, freq1)

# Señal 2, frecuencia y amplitud. 

freq2 = 50.0
y = amp*np.sin(2*np.pi*freq2*time)

titulo2 = " | Gráfica en " + str(freq2) + " Hz"

grafica(time, y, titulo2)

hacerfft(y, freq2)

# Señal 3, multiplicación de la señal

msignal = np.multiply(x, y)

titulo3 = " | Gráfica de señal mezclada"

grafica(time, msignal, titulo3)

hacerfft(msignal, "Señal mezclada")