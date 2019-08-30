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

# Grafica la señal en tiempo, donde las entradas tiene que cumplir
# lo siguiente: el eje X y el Y [x, y=f(x)]. La señal que se quiere
# graficar debe ser el segundo parámetro
# Además se puede introducir un mensaje opcional para xlabel
def grafica(timeArray, channel, texto=None):
    plot(timeArray, channel)
    ylabel('Amplitude')
    if texto == None:
        xlabel('Time (s)')
    else:
        xlabel('Time (s)  |  ' + str(texto))
    plt.show()

# Convierte las frecuencias deseadas a frecuencias normalizadas, 
# cumpliendo el criterio de Nyquist. Normaliza de 0 a 1, donde 1
# es la frecuencia de Nyquist
def convert_hertz(freq, fs=fs):
    return freq * 2.0 / fs

# Grafica la transformada de Fourier de la señal, utiliza FFT.
# Devuelve los valores de fdata y freqArray, por si quieren 
# ser utilizados fuera de la función
# Además se puede introducir un mensaje opcional para xlabel
def hacerfft(channel, texto=None):
    fdata = fft(channel)

    print('\t> FFT realizada')
        
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
        xlabel('Frequency (kHz)  |  ' + str(texto))
    ylabel('Power (dB)')
    plt.show()

    print('\t> FFT graficada')

    return fdata, freqArray

hacerfft(canal1, "original")
grafica(timeArray, canal1, "original")

# Primer filtro pasabajos, diseño y aplicación

print("> Etapa de PRIMER filtro")

gpass = 3
gstop = 15

# a no ser que se esté a más de 12 metros, este filtro no serviría, 
# estando a 12m, la frecuencia de batido es 1000Hz
ord, wn = signal.buttord(convert_hertz(1000), convert_hertz(1200), gpass, gstop)
b, a = signal.butter(ord, wn, btype='lowpass')

canal1Filtrado = signal.lfilter(b, a, canal1)
#canal1Filtrado = canal1

print('\t> Orden del filtro pasabajos (1): ' + str(ord))

print('\t> Primer filtro aplicado, 1000Hz')

hacerfft(canal1Filtrado, "Pasabajos 1000Hz")
grafica(timeArray, canal1Filtrado, "Pasabajos 1000Hz")

# Pasabanda @ 25Hz
# acá se pasará a modelar la frecuencia de batido de manera variable
# se están haciendo pruebas
# se ha adquirido data a 0.3, 1.5 y 3 metros
# los valores de frecuencia son 25, 125 y 250Hz respectivamente

# IMPORTANTE: buscar alrededor de este valor, la frecuencia adecuada

print("> Etapa de SEGUNDO filtro")

centro = 150
ancho = 4
downpass = (centro - (ancho/2))
uppass = (centro + (ancho/2))
downstop = downpass - ancho
upstop = uppass + ancho
ord, wn = signal.buttord([convert_hertz(downpass), convert_hertz(uppass)], [convert_hertz(downstop), convert_hertz(upstop)], 1, 20)
print('\t> Orden del filtro pasabanda (2): ' + str(ord))
b, a = signal.butter(ord, wn, btype='bandpass')
canal1Filtrado = signal.lfilter(b, a, canal1Filtrado)

print('\t> Segundo filtro aplicado, @' + str(centro) + 'Hz')

fdata1, freqArray1 = hacerfft(canal1Filtrado, "Pasabanda @" + str(centro) + "Hz")
grafica(timeArray, canal1Filtrado, "Pasabanda @" + str(centro) + "Hz")
'''
# Etapa de mezclado
# Generación de señal senoidal

print("> Etapa de mezclado")

arraysMaxValue = ((argmax(fdata1)*fs)/(2*len(freqArray1)))      # Valor de mayor potencia, en frecuencia (Hz)

print("\t> La frecuencia máxima después del segundo filtrado es: " + str(arraysMaxValue))

freq = arraysMaxValue
generatedSignal = 2*np.sin(2*np.pi*freq*timeArray)

print('\t> Señal arbitraria de "' + str(freq) + '" creada')
canal1Filtrado = multiply(canal1Filtrado, generatedSignal)

print('\t> La señal ha sido mezclada')

hacerfft(canal1Filtrado, "Señal mezclada y puesta en banda base")
grafica(timeArray, canal1Filtrado, "Señal mezclada y puesta en banda base")
'''
'''
# Tercer filtro, pasabajos  # C A M B I O S
print("> Etapa de TERCER filtro")

ord, wn = signal.buttord([convert_hertz(1.5), convert_hertz(14.5)], [convert_hertz(0.1), convert_hertz(15.9)], 0.5, 3)
print('\t> Orden del filtro pasabajos (3): ' + str(ord))
b, a = signal.butter(ord, wn, btype='bandpass')
canal1Filtrado = signal.lfilter(b, a, canal1Filtrado)

print('\t> Tercer filtro aplicado, banda base')

hacerfft(canal1Filtrado, "Pasabajos para banda base")
grafica(timeArray, canal1Filtrado, "Pasabajos para banda base")
'''
# Diodo
'''
canal1Filtrado[canal1Filtrado < 0] = 0

grafica(timeArray, canal1Filtrado, "| Diodo (filtrado)")

print("> Diodo aplicado a señal filtrada")
'''
distancia = 2700

# Hallado de picos
print("> Etapa de búsqueda de picos")
peaksFiltrado, valuesFiltrado = find_peaks(canal1Filtrado, height=0, distance = distancia)

print("\t> Picos de señal procesada hallados")
'''
plot(timeArray, canal1Filtrado)
plot(peaksFiltrado/fs, canal1Filtrado[peaksFiltrado])
plt.show()
'''
# Diodo
canalNoFiltro = canal1      # se usa cuando no se usa el diodo
'''
#canalNoFiltro[canalNoFiltro < 0] = 0

#grafica(timeArray, canalNoFiltro, "| Diodo (no filtrado)")

print("> Diodo aplicado a señal no-filtrada")
'''
# Hallado de picos sin filtraje
peaksNoFiltro, valuesNoFiltro = find_peaks(canalNoFiltro, height=0, distance = distancia)
print("\t> Picos de señal no-procesada hallados")
'''
plot(timeArray, canal1)
plot(peaksNoFiltro/fs, canalNoFiltro[peaksNoFiltro])
plt.show()
'''

picosFiltradoEnOriginal = canal1Filtrado[peaksFiltrado]

tenthFloored = ceil(len(picosFiltradoEnOriginal)*0.1)

# La ventana es 10% de la longitud del arreglo, debe ser impar

if (tenthFloored % 2 == 1):
    windowSavGolFilter = tenthFloored
else:
    windowSavGolFilter = tenthFloored + 1

picosProcesado_suavizado = savgol_filter(canal1Filtrado[peaksFiltrado], int(windowSavGolFilter), 5)

# Gráfica resumen
print("> Gráfica resumen")
subplot(2,1,1)
plot(timeArray, canal1Filtrado)
plot(peaksFiltrado/fs, canal1Filtrado[peaksFiltrado])
plot(peaksFiltrado/fs, picosProcesado_suavizado, color='k')
ylabel('Amplitude')
xlabel("Time (s)  |  Señal Procesada")

subplot(2,1,2)
plot(timeArray, canal1)
plot(peaksNoFiltro/fs, canalNoFiltro[peaksNoFiltro])
ylabel('Amplitude')
xlabel("Time (s)  |  Señal No-Procesada")

plt.show()

plot(peaksFiltrado/fs, picosProcesado_suavizado, color='k') #,linewidth=3.5)
plot(peaksFiltrado/fs, picosFiltradoEnOriginal)

plt.show()

print(corrcoef(picosFiltradoEnOriginal, picosProcesado_suavizado))

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