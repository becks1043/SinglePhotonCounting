import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit 

def gaussian(x, A, mu, sigma):
    return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

def linear(x, m, q):
    fit = m*np.array(x) + q
    return fit
    
def MGF(x, *params):
    result = np.zeros_like(x, dtype=np.float64)
    for i in range(0, len(params), 3):
        a = params[i]
        mu = params[i +1]
        sigma = params[i+2]
        result += a * np.exp(-((x-mu)**2)/(2*(sigma**2)))
    return result

def MGF2(x, *params): #versione vettorializzata
    if len(params) % 3 != 0:
        raise ValueError(f"Il numero di parametri deve essere un multiplo di 3 (A, $\mu$, $\sigma$ per ogni gaussiana).")
    params = np.array(params).reshape(-1, 3)  # Reshape in (N, 3)
    a, mu, sigma = params[:, 0], params[:, 1], params[:, 2]  # Estrai colonne
    gaussians = a[:, None] * np.exp(-((x[None, :] - mu[:, None])**2) / (2 * sigma[:, None]**2))
    return np.sum(gaussians, axis=0)

path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno2\test_35dB_2.7mV_alimentato12V.Spe"
with open(path, "r") as file:
    lines = file.readlines()
data = lines[13:2060]
rumore = [int(line.strip()) for line in data] # abbiamo il rumore del task03
# è uno strumentopolo misterioso che ci servirà più tardi

#%%________________________GIORNO 2 parte 3__________________________________________________________________
# guardiamo sorgenteAm_12V_150s.Spe

path = r"C:\Users\user\Desktop\Programming\es3_Single-photon-counting\giorno2\sorgenteAm_12V_150s.Spe"
data = []

with open(path, "r") as file:
    lines = file.readlines()

data_raw = lines[13:2060]
data = [int(line.strip()) for line in data_raw]

for jj in range(len(data)):
    data[jj] -= rumore[jj]
    if data[jj]<0:
        data[jj] = 0

#noise = np.array(data_corrected[:30]) # i primi 30 canali sono rumorosi
spectra = np.array(data[30:]) # osserviamo qui lo spettro
channels = list( range(1, len(data)+1 ) ) # definiamo l'array dei canali da 1 a 2048

#noise_region = np.array(channels[:30]) # da 1 a 30
spectra_region = np.array(channels[30:]) # da 31 a 2047

# guess Am241 peaks
guess = [9610, 50, 20,
    540, 100, 20,
    6600, 345, 17]

bound = (0, np.inf)
popt, pcov = curve_fit(MGF2, spectra_region, spectra, p0=guess, sigma=None, maxfev=100000, bounds=bound)

print('popt:\n', popt)
print('pcov:\n', np.sqrt( np.diag(pcov) ) )

# PLOT
plt.figure(figsize=(10, 6))
#plt.errorbar(noise_region, noise, zorder=2, color='green', label=r'rumore')
plt.errorbar(spectra_region, spectra, zorder=2, fmt='.', color='blue', label=r'sorgente di $^{241}Am$')
plt.plot(spectra_region, MGF2(spectra_region, *popt), color='red', zorder=1, label='fit gaussiano')
plt.xlabel("Canali", size=15)
plt.ylabel("Conteggi [adim.]", size=15)
plt.xlim(0, 800)
plt.ylim(0, 20000)
# Create empty plot with blank marker containing the extra label
plt.plot([], [], ' ', label="picco in:") # bad trick, I know
plt.plot([], [], ' ', label="$345\pm5$")
plt.plot([], [], ' ', label="$46\pm2$")
plt.legend(loc='best', fontsize=15)
#plt.show()
#plt.savefig("spettro-Am241.pdf", format="pdf", bbox_inches="tight")
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


# FIT MULTIGAUSSIANO MOLIBDENO
# Molibdeno emissione ka a 17.5keV e 17.4keV ed una meno visibile kb a 19.6keV
with open(Mo_path, "r") as file:
    lines = file.readlines()
data1 = lines[13:2060]
Mo = [int(line.strip()) for line in data1]

for jj in range(len(Mo)):
    Mo[jj] -= rumore[jj]
    if Mo[jj]<0:
        Mo[jj] = 0

#channels = np.linspace(1, len(data1)+1, len(data1))
ii = np.arange(314, 375) # nei prox fit rimane uguale
guess_Mo = [2770, 41, 40,
           1000, 100, 25,
           235, 137, 20,
           1000, 345, 20] # nei prox fit viene ridefinito

popt1, pcov1 = curve_fit(MGF, channels[29:], Mo[29:], p0=guess_Mo, sigma=None, maxfev=1000000)


# FIT MULTIGAUSSIANO ZIRCONIO
# Zirconio emissione ka a 15.77keV e 15.79 keV ed una kb a 17.7keV
with open(Zr_path, "r") as file:
    lines = file.readlines()
data2 = lines[13:2060]
Zr = [int(line.strip()) for line in data2] 

for jj in range(len(Zr)):
    Zr[jj] -= rumore[jj]
    if Zr[jj]<0:
        Zr[jj] = 0

guess_Zr = [2100, 40, 20,
        700, 92, 15,
        180, 137, 25,
        5000, 345, 15]

popt2, pcov2 = curve_fit(MGF, channels[29:], Zr[29:], p0=guess_Zr, sigma=None, maxfev=1000000)


# FIT MULTIGAUSSIANO GADOLINIO
# Gadolinio emissione kb a 48.69keV e ka a 43keV e 42.3keV
with open(Gd_path, "r") as file:
    lines = file.readlines()
data3 = lines[13:2060]
Gd = [int(line.strip()) for line in data3]

for jj in range(len(Gd)):
    Gd[jj] -= rumore[jj]
    if Gd[jj]<0:
        Gd[jj] = 0
        
guess_Gd = [380, 50, 30, 
         1000, 100, 15, 
         200, 247, 20,
         76, 283, 10,
         1000, 345, 10]

popt3, pcov3 = curve_fit(MGF, channels[29:], Gd[29:], p0=guess_Gd, sigma=None, maxfev=1000000)

print(f'Avendo dato un guess\n (Ampiezza / Canale picco / FHWM)\n {guess_Mo}\n il fit molibdeno è:\n {popt1}\n')
print(f'Avendo dato un guess\n {guess_Zr}\n il fit Zirconio è:\n {popt2}\n')
print(f'Avendo dato un guess\n {guess_Gd}\n il fit Gadolinio è:\n {popt3}\n')

plt.figure()
plt.errorbar(channels, Mo, fmt='.', label='Molibdeno $100 \mu m$', zorder=2)
plt.errorbar(channels, Zr, fmt='.', label='Zirconio $250 \mu m$', zorder=2)
plt.errorbar(channels, Gd, fmt='.', label='Gadolinio $240 \mu m$', zorder=2)
plt.plot(channels[29:], MGF(channels[29:], *popt1), color='grey', zorder=1)
plt.plot(channels[29:], MGF(channels[29:], *popt2), color='grey', zorder=1)
plt.plot(channels[29:], MGF(channels[29:], *popt3), color='grey', zorder=1)
plt.ylabel("Conteggi [adim.]", size=15)
plt.xlabel("Canale", size=15)
plt.ylim(0, 7000)
plt.xlim(20, 450)
plt.legend(loc='best', fontsize=15)
#plt.savefig("lastrine-Mo_Zr_Gd.pdf", format="pdf", bbox_inches="tight")
#plt.show()
plt.close()

#%%__________________GIORNO 2 parte 5_____________________________________________________________________
# fortunatamente ho trovato almeno che abbiamo visto in aula un picco di stagno a 144 corrispondente a 25 keV
# allora usiamo quello e le emissioni caratteristiche del Molibdeno (17.3, 17.5, 19.5 keV in canale 101)
# quelle dello Zirconio (15.7 e 15.8 keV in canale 91 & 18 keV in canale 99) ed infine
# le emissioni del Gadolinio (49 keV a canale 282 & 42.3, 43 keV a canale 247)

CC = [91., 99., 101., 144., 247., 271., 344.]
dC = [9, 39, 8, 8, 7, 50, 8]
En = [15.8, 18., 17.5, 25., 43., 49., 60.]

ENERGIES = np.linspace(0, 100, 10000)

popt, pcov = curve_fit(linear, En, CC, sigma=dC)
print(f'la conversione canali->energia è:\n (canale-{popt[1]}) / {popt[0]}')
print(f'perché: \n m={popt[0]}+-{np.sqrt(np.diag(pcov))[0]} \n q={popt[1]}+-{np.sqrt(np.diag(pcov))[1]}')

# definisco i punti separati in base all'appartenenza di materiale
mol, dmol, Emol = 101, 8, 18 # canale picco / sigma / energia corrispondente in keV
zin, dzin, Ezin = [91, 99], [9, 39], [15.8, 18]
sta, dsta, Esta = 144, 8, 25
gad, dgad, Egad = [247, 271], [7, 50], [43, 47]
com, dcom, Ecom = 344, 8, 60

# PLOT CALIBRAZIONE
plt.figure(figsize=(10, 6))
plt.errorbar(Emol, mol, dmol, zorder=2, fmt='o', color='blue', label=r'emissioni Mo')
plt.errorbar(Ezin, zin, dzin, zorder=2, fmt='o', color='orange', label=r'emissioni Zr')
plt.errorbar(Egad, gad, dgad, zorder=2, fmt='o', color='green', label=r'emissioni Gd')
plt.errorbar(Ecom, com, dcom, zorder=2, fmt='o', color='black')
plt.plot(ENERGIES, linear(ENERGIES, *popt), color='red', zorder=1, label='fit lineare')
plt.xlabel("Energia [keV]", size=15)
plt.ylabel("Canali picco [adim.]", size=15)
plt.legend(loc='best', fontsize=15)
#plt.show()
plt.savefig("calibrazione-materiali.pdf", format="pdf", bbox_inches="tight")
plt.close()