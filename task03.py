import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit 

# GIORNO 2 parte 1
# abbiamo ripreso la misura di test per verificare la calibrazione 24h dopo

path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno2\test_35dB_2.7mV.Spe"

with open(path, "r") as file:
    lines = file.readlines()
    data = lines[12:2060]

# dati senza alimentazione: A-No
y_Ano = [int(line.strip()) for line in data]
xx = np.linspace(0, len(y_Ano), len(y_Ano))

# GIORNO2 parte 2
# Abbiamo preso una misura del segnale test con alimentazione a 12V
# si osserva uno shift di 70 canali !

path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno2\test_35dB_2.7mV_alimentato12V.Spe"

with open(path, "r") as file:
    lines = file.readlines()

data = lines[12:2060]

# dati con alimentazione: A-Si
y_Asi = [int(line.strip()) for line in data]

# PLOT DI ENTRAMBI
fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=True, gridspec_kw={'height_ratios': [1, 1]})

axes[0].plot(xx, y_Ano, label='senza alimentazione')
axes[0].set_ylabel("Ampiezza [adim.]", size=15)
axes[0].legend(loc='best')
axes[0].set_ylim(-1, 13000)
axes[0].set_xlim(0, 800)

axes[1].plot(xx, y_Asi, label='con alimentazione 12 V')
axes[1].set_ylim(-1, 13000)
axes[1].set_xlim(0, 800)
axes[1].set_xlabel("Canali", size=15)
axes[1].set_ylabel("Ampiezza [adim.]", size=15)
axes[1].legend(loc='best')
plt.savefig("calibrazione-giorno2.pdf", format="pdf", bbox_inches="tight")
plt.show()
plt.close()