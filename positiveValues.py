import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp, savgol_filter
from pylab import arange, mean
from pylab import plot, subplot
from scipy import signal

#   Este script crea un arreglo donde los valores son los valores medios del
#   archivo de sonido, en donde la muestra depende del parámetro dist

#Esta es una prueba para commit

lalalalalalala

def convert_hertz(freq):
    return freq * 2.0 / 44100.0

carpeta = "../audioFiles/"
nombre = 'Sentado_30cm_interfaz_1'
ext = '.wav'
arch = carpeta + nombre + ext

fs, data = wavfile.read(arch)

print('> Archivo leído')

data = data/(2.**15)
leng = len(data)
channel1 = data[:,0]

t = arange(0, leng, 1)
t = t/fs

signalllll = chirp(t, 100.0, t[-1], 1500.0)
signalllll = signalllll * (3.0 + 0.9 * np.sin(2.0*np.pi*3.0*t) )

'''
print("Original array:")
print(channel1)
print("Replace the negative values of the said array with 0:")
channel1[channel1 < 0] = 0
print(channel1)
'''

#channel1filtered = savgol_filter(channel1, 201, 7)

'''
corrvalue = corrcoef(channel1, channel1filtered)
print(mean(corrvalue))
'''

'''
analytic_signal = hilbert(channel1)
amplitude_envelope = np.abs(analytic_signal)
'''

ch1av = list()

dist = 100

for x in range(0, len(channel1), dist):
    med = mean(channel1[x:x+dist])
    ch1av.append(med)
   

tch1av = arange(0, len(ch1av), 1)

plot(t, channel1)
#plot(t, amplitude_envelope, label='envelope', color='k')
plt.show()

'''
analytic_signal1 = hilbert(tch1av)
amplitude_envelope1 = np.abs(analytic_signal1)
'''

subplot(2,1,1)
plot(tch1av/441, ch1av, label='signal', color='k')
#plot(tch1av, amplitude_envelope1)


subplot(2,1,2)
plot(t, channel1)
#plot(t, amplitude_envelope)

plt.show()

