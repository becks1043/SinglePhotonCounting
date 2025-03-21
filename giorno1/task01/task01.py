import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit 
import pandas as pd

y_data = []
x_data = []
all_data = []

path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno1\task01\A"
txt = ".Spe"

# Questi sono i dati ottenuti usando MAESTRO, li definiamo qui li usiamo prima per dare label al primo plot
# e poi per fare il secondo plot sulla calibrazione

V = [4.0, 2.7, 2.3, 2.1, 1.8, 1.4, 1.3]
Ver = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
Vbis = [4.0, 2.7]
Vbiserr = [0.4, 0.4]
Chan = [623.6, 416.7, 350.0, 312.2, 278.9, 208.7, 196.6]
Chaner = [14.7, 14.5, 14.6, 14.3, 14.6, 14.1, 14.1]
Chanbis = [624.1, 417.6]
Chanbiser = [14.4, 14.3]

xx = V + Vbis
yy = Chan + Chanbis
ERR = Chaner + Chanbiser


# vogliamo leggere i file A1...A7 e plottarli ignorando le prime 12 e ultime 16 righe
for i in range(1, 10):
    filename = path + str(i) + txt # nome del file in questa iterazione
    with open(filename, "r") as file:
        lines = file.readlines()
        data = lines[12:2060]
    # Converte i dati in una lista di numeri interi
    y_data = [int(line.strip()) for line in data]
    all_data.append(y_data)

bins = np.linspace(0, len(y_data), len(y_data))

# PLOT
# Fai il plot
plt.figure(figsize=(10, 6))
for i in range(9):
    plt.plot(bins, all_data[i][:], label=f"A{i+1}.Spe, d.d.p.= {xx[i]}, Xm={yy[i]}+\-{ERR[i]}")
plt.xlabel("Canali", size=15)
plt.ylabel("Ampiezza [u.a.]", size=15)
plt.title(f"Dati task01 dei file A1-A7")
plt.legend()
plt.show()
plt.close()


# Con MAESTRO abbiamo preso al variare della d.d.p. da 4mV a 1.3mV la posizione del canale centrale Xm
# ed il suo errore FWHM, selezionando una ROI attorno al picco che vedevamo
# le misure bis sono la prova di riprodurre le prime due misurazioni, due ore dopo l'inizio dell'esperienza

def linear(x, a, b):
    z = np.array(x)
    return a*z + b

# faccio il fit solo sulle misure prese a poca distanza di tempo A1/A7, 
# tengo le misure bis (A8, A9) fuori dal fit ma le plotterò in colore diverso
popt, pcov= curve_fit(linear, V, Chan, p0=None, sigma=Chaner, absolute_sigma=True)
m, q = popt[0], popt[1]
#m = int(popt[0])
#q = int(popt[1])

for i in range(len(Chan)):
    chi_square = np.sum( (linear(V, m, q)[i]- Chan[i])**2 / Chaner[i] ) #va diviso per gli errori 

dof = len(Chan) - len(popt)
chi_norm = chi_square / dof

print("---------")
print(f"Parametri del fit m={m} e q={q}")
print(f"il chi2 è {chi_square} \n il chi2 normalizzato è {chi_norm}")
print("---------")

plt.figure()
plt.scatter(V, Chan, Chaner, Ver, label='acquisizioni', zorder=2)
plt.scatter(Vbis, Chanbis, Chanbiser, Vbiserr, label='acquisizioni bis', zorder=2)
plt.plot(xx, linear(xx, m, q), zorder=1, label='fit lineare')
plt.xlabel("Tensione $\Delta$V [mV]", size=15)
plt.ylabel("Canale del picco $X_m$ [channels]", size=15)
#plt.title("")
plt.legend()
plt.grid(which="both", linestyle="--")
plt.show()
plt.close()














