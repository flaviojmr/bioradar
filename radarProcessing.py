import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
from scipy.signal import find_peaks, savgol_filter
from pylab import fft, arange, ceil, log10, argmax, multiply, corrcoef
from pylab import plot, xlabel, ylabel, subplot

# Este programa filtra una señal que contiene información de ritmo cardiaco,
# filtrándola y obteniendo la información almacenada en la amplitud. Esta señal
# es de de dos canales, se vuelve mono, se pasa por un diodo y luego se utiliza 
# filtros digitales Butterworth. Se halla la FFT de la señal, en distintas etapas 
# del proceso; se grafica esta y también la señal en el tiempo. 
# Al final del programa, se muestran las señales filtrada y sin filtrado.

carpeta = "../audioFiles/"
nombre = 'Sentado_Tranquilo_UNmetroYMedio_3'
ext = '.wav'
arch = carpeta + nombre + ext

fs, data = wavfile.read(arch)

print('> Archivo leído')

data = data/(2.**15)
leng = len(data)
canal1 = data[:,0]

print('> Duración de la muestra: ' + str(leng/fs) + "s")

print('> Canales spliteados')

timeArray = arange(0, leng, 1)
canal1 = canal1[0:leng:1]           #Señal lista para trabajar
print('> Arreglo de tiempo y canal creados')

timeArray = timeArray/fs

def grafica(timeArray, channel, texto):
    plot(timeArray, channel)
    ylabel('Amplitude')
    if texto == None:
        xlabel('Time (s)')
    else:
        xlabel('Time (s) ' + " | " + str(texto))
    plt.show()

def convert_hertz(freq):
    return freq * 2.0 / 44100.0

def hacerfft(channel, texto=None):
    fdata = fft(channel)

    print('> FFT realizada')
        
    nUniquePts = int(ceil((leng)/2))
    fdata = fdata[0:nUniquePts]
    fdata = abs(fdata)

    fdata = fdata/float(leng)
    fdata = fdata**2

    if leng % 2 > 0:
        fdata[1:int(ceil(len(fdata)))] = fdata[1:int(ceil(len(fdata)))] * 2
    else:
        fdata[1:int(ceil(len(fdata)))-1] = fdata[1:int(ceil(len(fdata)))-1] * 2

    freqArray = arange(0, nUniquePts, 1.0)*(fs/leng)
    plot(freqArray/1000, 10*log10(fdata[0:leng:1]))

    if texto == None: 
        xlabel('Frequency (kHz)')
    else:
        xlabel('Frequency (kHz)' + " | " + str(texto))
    ylabel('Power (dB)')
    plt.show()

    print('> FFT graficada')

    return fdata, freqArray

#hacerfft(canal1, "original")
#grafica(timeArray, canal1, "original")

# Primer filtro pasabajos, diseño y aplicación
gpass = 3
gstop = 15

# a no ser que se esté a más de 12 metros, este filtro no serviría, 
# estando a 12m, la frecuencia de batido es 1000Hz
ord, wn = signal.buttord(convert_hertz(1000), convert_hertz(1200), gpass, gstop)
b, a = signal.butter(ord, wn, btype='lowpass')

canal1Filtrado = signal.lfilter(b, a, canal1)
#canal1Filtrado = canal1

print('     > Orden del filtro pasabajos: ' + str(ord))

print('> Primer filtro aplicado, 1000Hz')

#hacerfft(canal1Filtrado, "Pasabajos 1000Hz")
#grafica(timeArray, canal1Filtrado, "Pasabajos 1000Hz")

# Pasabanda @ 25Hz
# acá se pasará a modelar la frecuencia de batido de manera variable
# se están haciendo pruebas
# se ha adquirido data a 0.3, 1.5 y 3 metros
# los valores de frecuencia son 25, 125 y 250Hz respectivamente

# IMPORTANTE: buscar alrededor de este valor, la frecuencia adecuada

centro = 150
ancho = 4
downpass = (centro - (ancho/2))
uppass = (centro + (ancho/2))
downstop = downpass - ancho
upstop = uppass + ancho
ord, wn = signal.buttord([convert_hertz(downpass), convert_hertz(uppass)], [convert_hertz(downstop), convert_hertz(upstop)], 1, 20)
b, a = signal.butter(ord, wn, btype='bandpass')
canal1Filtrado = signal.lfilter(b, a, canal1Filtrado)

print('     > Orden del filtro pasabanda: ' + str(ord))

print('> Segundo filtro aplicado, @' + str(centro) + 'Hz')

fdata1, freqArray1 = hacerfft(canal1Filtrado, "Pasabanda @" + str(centro) + "Hz")
#grafica(timeArray, canal1Filtrado, "Pasabanda @" + str(centro) + "Hz")

# Etapa de mezclado
# Generación de señal senoidal

arraysMaxValue = ((argmax(fdata1)*fs)/(2*len(freqArray1)))

print("El punto máximo es: " + str(arraysMaxValue))


freq = arraysMaxValue - 0.0000138
time1 = np.arange(leng) / fs
generatedSignal = 2*np.sin(2*np.pi*freq*time1)

print('> Señal arbitraria de ' + str(freq) + ' creada')
canal1Filtrado = multiply(canal1Filtrado, generatedSignal)

print('> La señal ha sido mezclada')

#hacerfft(canal1Filtrado, "Señal mezclada y puesta en banda base")
#grafica(timeArray, canal1Filtrado, "Señal mezclada y puesta en banda base")

# Tercer filtro, pasabajos

ord, wn = signal.buttord([convert_hertz(298), convert_hertz(302)], [convert_hertz(295), convert_hertz(305)], 4, 16)
b, a = signal.butter(ord, wn, btype='bandpass')

canal1Filtrado = signal.lfilter(b, a, canal1Filtrado)

print('     > Orden del tercer filtro (pasabajos): ' + str(ord))

print('> Tercer filtro aplicado, banda base')

#hacerfft(canal1Filtrado, "Pasabajos para banda base")
#grafica(timeArray, canal1Filtrado, "Pasabajos para banda base")

# Diodo
#canal1Filtrado[canal1Filtrado < 0] = 0

#grafica(timeArray, canal1Filtrado, "| Diodo (filtrado)")

#print("> Diodo aplicado a señal filtrada")

distancia = 2700

# Hallado de picos
peaksFiltrado, valuesFiltrado = find_peaks(canal1Filtrado, height=0, distance = distancia)

print("> Picos hallados")
'''
plot(timeArray, canal1Filtrado)
plot(peaksFiltrado/fs, canal1Filtrado[peaksFiltrado])
plt.show()
'''
# Diodo
canalNoFiltro = canal1
#canalNoFiltro[canalNoFiltro < 0] = 0

#grafica(timeArray, canalNoFiltro, "| Diodo (no filtrado)")

print("> Diodo aplicado a señal no-filtrada")

# Hallado de picos sin filtraje
peaksNoFiltro, valuesNoFiltro = find_peaks(canalNoFiltro, height=0, distance = distancia)
'''
plot(timeArray, canal1)
plot(peaksNoFiltro/fs, canalNoFiltro[peaksNoFiltro])
plt.show()

newArray = savgol_filter(canal1Filtrado, 101, 2)
'''
# Gráfica resumen
subplot(2,1,1)
plot(timeArray, canal1Filtrado)
plot(peaksFiltrado/fs, canal1Filtrado[peaksFiltrado])
#plot(timeArray, newArray, color='k')
ylabel('Amplitude')
xlabel('Time (s)  ' + "|  Processed Signal")

subplot(2,1,2)
plot(timeArray, canal1)
plot(peaksNoFiltro/fs, canalNoFiltro[peaksNoFiltro])
ylabel('Amplitude')
xlabel('Time (s)  ' + "|  No Processed Signal")

plt.show()

unaVariableMas = canal1Filtrado[peaksFiltrado]
print(unaVariableMas)
print("El tamaño de unaVariableMas, usando len, es: " + str(len(unaVariableMas)))
print("El tamaño de unaVariableMas, usando shape, es: " + str(unaVariableMas.shape))
print("El tamaño de unaVariableMas, usando size, es: " + str(unaVariableMas.size))

newArray = savgol_filter(unaVariableMas, 51, 5)
print("El tamaño de newArray, usando len, es: " + str(len(newArray)))
print("El tamaño de newArray, usando shape, es: " + str(newArray.shape))
print("El tamaño de newArray, usando size, es: " + str(newArray.size))
plot(peaksFiltrado/fs, newArray, color='k') #,linewidth=3.5)
plot(peaksFiltrado/fs, unaVariableMas)

plt.show()

print(corrcoef(unaVariableMas, newArray))

print('linea de espera')
print('siguiente linea de espera')

'''
print("Correlación de ubicación de puntos máximos" + str(np.corrcoef(peaksFiltrado, peaksNoFiltro)))

print("Correlación de valores de puntos máximos" + str(np.corrcoef(valuesFiltrado, valuesNoFiltro)))


posPicosFiltrado = list(peaksFiltrado)
valoresFiltrado = list(valuesFiltrado['peak_heights'])

print(type(posPicosFiltrado))
print(type(valuesFiltrado))
print(type(valoresFiltrado))
print(len(peaksFiltrado))
print(len(valuesFiltrado))
print(len(valoresFiltrado))

newValuesFiltered = arange(0, leng, 1)

for x in range(leng):
    if (x in peaksFiltrado):
        newValuesFiltered[x] = valoresFiltrado[posPicosFiltrado.index(x)]
        #print(x)
    else:
        newValuesFiltered[x] = 0
    #print(x)

print(newValuesFiltered[1100:1120])

print("plsssss")

'''