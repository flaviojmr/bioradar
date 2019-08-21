from pylab import fft, arange, ceil, log10, argmax
from pylab import plot, xlabel, ylabel
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal.filter_design import butter, buttord
import time

carpeta = "../audioFiles/"
nombre = 'Sentado_30cm_interfaz_1'
ext = '.wav'
arch = carpeta + nombre + ext

fs, data = wavfile.read(arch)

print('> Archivo leído')

data = data/(2.**15)
print ("El tamaño de la primera dimensión es: ", str(data.shape[0]))
leng = len(data)

channel1 = data[:,0]
channel2 = data[:,1]

print('> Canales spliteados')

t = arange(0, leng, 1)
t = t/fs

print('> Arreglo de tiempo creado')

print('> Realizando FFT...')

t1 = time.time()

fdata = fft(channel1)

t2 = time.time()

print('> Transformada Rápida de Fourier realidad (FFT)')

print(' > Duración de la FFT: ', str(t2-t1))

nUniquePts = int(ceil((leng+1)/2))
fdata = fdata[0:nUniquePts]
fdata = abs(fdata)

fdata = fdata/float(leng)
fdata = fdata**2

if leng % 2 > 0:
   fdata[1:int(ceil(len(fdata)))] = fdata[1:int(ceil(len(fdata)))] * 2
else:
    fdata[1:int(ceil(len(fdata)))-1] = fdata[1:int(ceil(len(fdata)))-1] * 2

freqArray = arange(0, nUniquePts, 1.0)*(fs/leng)
plot(freqArray/1, 10*log10(fdata))
xlabel('Frequency (kHz)')
ylabel('Power (dB)')
plt.show()

print('El valor máximo es: ' + str(10*log10(max(fdata))))

print('El punto del valor máximo es: ' + str((argmax(fdata)*fs)/(2*len(freqArray))))


plot(t, channel1)

ylabel('Amplitude')
xlabel('Time (s)')
plt.show()