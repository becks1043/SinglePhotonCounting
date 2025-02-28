import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit 

def MGF(x, *params):
    result = np.zeros_like(x, dtype=float)
    for i in range(0, len(params), 3):
        a = params[i]
        mu = params[i +1]
        sigma = params[i+2]
        result += a * np.exp(-((x-mu)**2)/(2*(sigma**2)))
    return result

#%%________________________GIORNO 2 parte 3__________________________________________________________________
# guardiamo sorgenteAm_12V_150s.Spe

path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno2\sorgenteAm_12V_150s.Spe"
data = []

with open(path, "r") as file:
    lines = file.readlines()

data = lines[13:2060]
data_corrected = [int(line.strip()) for line in data]

noise = data_corrected[:30] # i primi 30 canali sono rumorosi
spectra = data_corrected[30:] # osserviamo qui lo spettro

channels = list( range(1, len(data)+1 ) ) # definiamo l'array dei canali da 1 a 2048

noise_region = channels[:30]
spectra_region = channels[30:]

# guess Am241 peaks
n_peak = 2
guess = [45, 50, 1,
         345, 17, 1,
         ]

bound = (0, np.inf)
popt, pcov = curve_fit(MGF, spectra_region, spectra, p0=guess, sigma=None, maxfev=100000, bounds=bound)

print('popt:\n', popt)
print('pcov:\n', pcov)

# PLOT
plt.figure(figsize=(10, 6))
plt.errorbar(noise_region, noise, zorder=2, color='green', label=r'rumore')
plt.errorbar(spectra_region, spectra, zorder=2, fmt='.', color='blue', label=r'sorgente di $^{241}Am$')
plt.plot(spectra_region, MGF(spectra_region, *popt), color='red', zorder=1, label='fit multigaussiano')
plt.xlabel("Canali", size=15)
plt.ylabel("Conteggi [adim.]", size=15)
plt.xlim(0, 800)
plt.ylim(0, 20000)
# Create empty plot with blank marker containing the extra label
plt.plot([], [], ' ', label=r"Posizione del picco: $345\pm17$") # bad trick, I know
plt.legend(fontsize=15)
plt.show()
plt.savefig("spettro-Am241.pdf", format="pdf", bbox_inches="tight")
plt.close()


#%%__________________GIORNO 2 parte 4_____________________________________________________________________
# guardiamo la sorgente attraverso i picchi di fluorescenza id 4 lastrine
# Molibdeno 100 um, Stagno 250 um, Zirconio 250 um, Gadolinio 240 um
# manca il file .Spe dello stagno :(

Mo_path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno2\Molibdeno100um.Spe"
data1 = []
Zr_path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno2\Zirconio250um.Spe"
data2 = []
Gd_path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno2\gadolinio240um.Spe"
data3 = []


# Molibdeno emissione ka a 17.5keV e 17.4keV ed una meno visibile kb a 19.6keV
with open(Mo_path, "r") as file:
    lines = file.readlines()
Mo_data = lines[13:2060]
Mo = [int(line.strip()) for line in Mo_data]

x = np.linspace(1, len(Mo_data)+1, len(Mo_data))

# Zirconio emissione ka a 15.77keV e 15.79 keV ed una kb a 17.7keV
with open(Zr_path, "r") as file:
    lines = file.readlines()
Zr_data = lines[13:2060]
Zr = [int(line.strip()) for line in Zr_data]

# Gadolinio emissione kb a 48.69keV e ka a 43keV e 42.3keV
with open(Gd_path, "r") as file:
    lines = file.readlines()
Gd_data = lines[13:2060]
Gd = [int(line.strip()) for line in Gd_data]

plt.figure()
plt.plot(x, Mo, label='Molibdeno $100 \mu m$')
plt.plot(x, Zr, label='Zirconio $250 \mu m$')
plt.plot(x, Gd, label='Gadolinio $240 \mu m$')
plt.ylabel("Conteggi [adim.]", size=15)
plt.xlabel("Canale", size=15)
plt.ylim(0, 7000)
plt.xlim(0, 500)
plt.legend(loc='best', fontsize=15)
plt.savefig("lastrine-Mo_Zr_Gd.pdf", format="pdf", bbox_inches="tight")
plt.show()
plt.close()


