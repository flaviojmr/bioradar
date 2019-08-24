from scipy.io import wavfile
import matplotlib.pyplot as plt
from pylab import plot, subplot, xlabel, ylabel
from pylab import fft, ceil, log10, arange, mean
import random
import numpy as np

# Este script crea un arreglo donde los valores son los valores medios del
# archivo de sonido, en donde la muestra depende del parámetro 'dist'



def hacerfft(channel):
    tamanho = len(channel)

    fdata = fft(channel)

    print('> FFT realizada')
        
    nUniquePts = int(ceil((tamanho)/2))
    fdata = fdata[0:nUniquePts]
    fdata = abs(fdata)

    fdata = fdata/float(leng)
    fdata = fdata**2

    if leng % 2 > 0:
        fdata[1:int(ceil(len(fdata)))] = fdata[1:int(ceil(len(fdata)))] * 2
    else:
        fdata[1:int(ceil(len(fdata)))-1] = fdata[1:int(ceil(len(fdata)))-1] * 2

    freqArray = arange(0, nUniquePts, 1.0)*(fs/tamanho)
    plot(freqArray/1000, 10*log10(fdata[0:tamanho:1]))

    xlabel('Frequency (kHz)')
    ylabel('Power (dB)')
    plt.show()

    print('> FFT graficada')

    return fdata


carpeta = "../audioFiles/"
nombre = 'Sentado_30cm_interfaz_1'
ext = '.wav'
arch = carpeta + nombre + ext

fs, data = wavfile.read(arch)

print('> Archivo leído: \n\tfs:\t' + str(fs) + '\n\tdata:\t' + str(len(data)))

data = data/(2.**15)
leng = len(data)
channel1 = data[:,0]

print('> Separación de canales')

t = arange(0, leng, 1)
t = t/fs

print('> Creación de arreglo de tiempo')

plot(t, channel1)
plt.show()

print('> Gráfica de señal original realizada')

# Creación de lista vacía, para introducir valores medios
ch1av = list()

# Valor de rango de toma de datos promedio
dist = 100

print('> Parámetro de distancia: ' + str(dist))

# Evaluar el arreglo y obtener los valores promedio, 
# almacenamiento en la lista creada
'''
for x in range(0, len(channel1), dist):
    med = mean(channel1[x:x+dist])
    ch1av.append(med)
'''
'''
# Diodo
channel1[channel1 < 0] = 0

print('> Diodo aplicado')
'''

channel1 = []

for i in range(100):
    randomcito = random.randint(0, 10)
    randomcito = randomcito/1.0
    channel1.append(randomcito)    

print(channel1)
print(type(channel1))

leng = len(channel1)

n = 0
window = 6
over = 3
windowedvalues = []
bottom = 0
top = window
print("Tipo de windowedValues es: " + str(type(windowedvalues)))

while (bottom + window) <= leng:
    tempVal = mean(channel1[bottom:top])
    print(channel1[bottom:top])
    print(tempVal)
    windowedvalues.append(tempVal)
    n += 1
    bottom = n*over
    top = n*over + window

print('> Cálculo de valores medios finalizado')

# Creación de arreglo de tiempo para valores promedio, 
# correción según parámetro 'dist'
'''
tch1av = arange(0, len(ch1av), 1)
tch1av = tch1av/(fs/dist)
'''

twindowedValues = arange(0, len(windowedvalues), 1)
tn = arange(0, len(channel1), 1)


print('> Creación de arreglo de tiempo para valores promedio')

# Gráfica de señal original y la promediada
subplot(2,1,1)
plot(twindowedValues, windowedvalues, label='signal', color='k')

subplot(2,1,2)
plot(tn, channel1)

plt.show()

orderedwindowed = ceil(windowedvalues)
orderedwindowed.sort()

orderedchannel1 = channel1
orderedchannel1.sort()

subplot(2,1,1)
plot(twindowedValues, orderedwindowed, label='signal', color='k')

subplot(2,1,2)
plot(tn, orderedchannel1)

plt.show()

binsHist = arange(1,10+1,1)



channel1Hist, channel1Bin_edges = np.histogram(channel1, range=(0.0,10.0))

subplot(2,1,1)
plt.hist(windowedvalues, range=(0.0,10.0))

subplot(2,1,2)
plt.hist(binsHist, channel1Hist)

plt.show()


print('> Gráfica de valores medios y señal original realizada')