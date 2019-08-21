from scipy.io import wavfile
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from pylab import arange, plot
#import peakutils

carpeta = "../audioFiles/"
nombre = 'Sentado_30cm_interfaz_1'
ext = '.wav'
arch = carpeta + nombre + ext

fs, data = wavfile.read(arch)

print('> Archivo leído: fs, data')

data = data/(2.**15)
channel1 = data[:,0]

print('> Separación de canales')

t = arange(0, len(channel1), 1)
t = t/fs

print('> Creación de arreglo de tiempo')

# Diodo
channel1[channel1 < 0] = 0

print('> Diodo aplicado')

# Distancia entre picos, y hallado de arreglo de picos y valores
dist = 2700
peaks, values = find_peaks(channel1, height=0, distance = dist)

print('> Posiciones de picos y valores hallados: peaks, values')

# Grafica de señal original y de los picos hallados (envolvente)
plot(t, channel1)
plot(peaks/fs, channel1[peaks])         # Para graficar, solo se utiliza el arreglo que indica la posiciones de los picos
plt.show()

print('> Gráfica de señal original y envolvente realizada')

print('> Programa utilizando "find_peaks"')

'''
print("Esto es peaks: " + str(peaks))
print("Tamaño de peaks: " + str(len(peaks)))

print("Esto es values: " + str(values))
print("Tamaño de values: " + str(type(values)))
'''
#print("Averrrrr " + str(values['peak_heights']))

#print()