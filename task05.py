import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit 
import pandas as pd

def espo(s, N0, mu):
    # mu_att = 1.593 cm^2/g
    # densità = 8.96 g/cm^3
    # N_0 = 298313
    return N0 * np.exp(mu*s)
    

lastrine = [0, 1, 2, 3, 4, 5, 6, 7, 9, 11]
y_data = []
all_data = []
data = []

path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno3\Atten"
txt = ".Spe"


# vogliamo leggere i file Atten1...Atten9 e plottarli ignorando le prime 12 e ultime 16 righe
for i in range(0, 10):
    filename = path + str(lastrine[i]) + txt # nome del file in questa iterazione
    with open(filename, "r") as file:
        lines = file.readlines()
        data = lines[12:2060]
    # Converte i dati in una lista di numeri interi
    y_data = [int(line.strip()) for line in data]
    all_data.append(y_data)

bins = np.linspace(0, len(y_data), len(y_data))

# PLOT
plt.figure(figsize=(10, 6))
for i in range(9):
    plt.plot(bins, all_data[i][:], label=f"Attenuazione di {550*lastrine[i]} um di rame")
plt.xlabel("Canali", size=15)
plt.ylabel("Ampiezza [u.a.]", size=15)
plt.xlim(315, 375) 
#plt.title(f"Dati task01 dei file A1-A7")
plt.legend()
plt.savefig("task5.pdf", format="pdf", bbox_inches="tight")
plt.show()
plt.close()

#%% VOGLIO PRENDERE I PICCHI DI DATI ATTENUAZIONE 

# area sottesa ai picchi, presa grazie a roi di maestro
Agross = [313640, 150743, 72151, 35269, 17127, 8266, 4125, 1969, 467, 152]
Anet = [298313, 145160, 69860, 34341, 16576, 7990, 3994, 1911, 380, 50]

mu = 1.593 * 8.96 * 0.0001 # cm^2/g * g/cm^3 * cm/um
spessore = 550 * np.array(lastrine) # micrometri

# fit esponenziale attenuazione area
popt1, pcov1 = curve_fit(espo, spessore, Agross, p0=(313640, mu) )
popt2, pcov2 = curve_fit(espo, spessore, Anet, p0=(298313, mu) )

print(popt1, '\n', np.sqrt(np.diag(pcov1)), '\n')
print(popt2, '\n', np.sqrt(np.diag(pcov2)), '\n')

xx = np.linspace(0, max(spessore), len(spessore)*100)

# verifico su questo l'attenuazione o facendo i fit dei picchi?
print(espo(xx, *popt1))
plt.figure()
plt.errorbar(spessore, Agross, fmt='o', label='gross area', zorder=2)
plt.errorbar(spessore, Anet, fmt='o', label='net area', zorder=2)
plt.plot(xx, espo(xx, *popt1), color='#A9A9A9', zorder=1)
plt.plot(xx, espo(xx, *popt2), color='#A9A9A9', zorder=1)
plt.savefig("attenuazione.pdf", format="pdf", bbox_inches="tight")
plt.show()
plt.close()