from scipy.io import wavfile
import matplotlib.pyplot as plt
from pylab import arange, plot, mean, subplot

# Este script crea un arreglo donde los valores son los valores medios del
# archivo de sonido, en donde la muestra depende del parámetro 'dist'

carpeta = "../audioFiles/"
nombre = 'Sentado_30cm_interfaz_1'
ext = '.wav'
arch = carpeta + nombre + ext

fs, data = wavfile.read(arch)

print('> Archivo leído: fs, data')

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
for x in range(0, len(channel1), dist):
    med = mean(channel1[x:x+dist])
    ch1av.append(med)   

print('> Cálculo de valores medios finalizado')

# Creación de arreglo de tiempo para valores promedio, 
# correción según parámetro 'dist'
tch1av = arange(0, len(ch1av), 1)
tch1av = tch1av/(fs/dist)

print('> Creación de arreglo de tiempo para valores promedio')

# Gráfica de señal original y la promediada
subplot(2,1,1)
plot(tch1av, ch1av, label='signal', color='k')

subplot(2,1,2)
plot(t, channel1)

plt.show()

print('> Gráfica de valores medios y señal original realizada')