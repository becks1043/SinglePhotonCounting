import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit 

def linear(x, m, q):
    fit = m*np.array(x) + q
    return fit

dV = 2.7 # mV
Ver = 0.4 # mV
G = 35 # dB
time = 90 # s
C = [0, 4.4, 6.5, 11.2, 17.7] # pF
Xm = np.round([418.0, 417.5, 417.5, 417.3, 417.2]) # chan
fwhm = np.round([13.3, 13.8, 16.5, 15.1, 15.9]) # chan

# FIT Xm contro C
popt, pcov= curve_fit(linear, C, Xm, sigma=np.array(fwhm)/2.35 , p0=(0, 417.5), absolute_sigma=False)
m, q = popt[0], popt[1]
merr, qerr = np.sqrt( np.diag(pcov) )

# CHI QUADRO E RESIDUI Xm contro C
fit_X = m* np.array(C) + q
chi_square = np.sum(((fit_X- Xm)/ fwhm)**2)  
dof = len(Xm) - len(popt)
chi_norm = chi_square / dof
residui = [Xm[i] - (m*C[i]+q) for i in range(len(Xm))]

print(f"\n Parametri del fit:\n m={m}+/-{merr}\n q={q}+/-{qerr}\n")
print(f"il chi2 è: {chi_square}\nil chi2 normalizzato è: {chi_norm}\n \n")

# PLOT Xm in funzione di C
fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
xx = np.linspace(min(C), max(C), 1000)
axes[0].errorbar(C, Xm, np.array(fwhm)/2.35, fmt='ro', label='picchi calcolati\n da maestro')
axes[0].plot(xx, linear(xx, m, q), label='fit')
axes[0].set_ylabel("posizione picco Xm [canali]", size=15)
axes[0].set_xlim(min(C)-1, max(C)+1)
axes[0].legend(loc='lower right', fontsize=15)
axes[1].set_xlim(min(C)-1, max(C)+1)
axes[1].set_ylim(-1, 1)
axes[1].errorbar(C, residui, np.array(fwhm)/2.35, fmt='bo')
axes[1].axhline(0, color='black', linestyle='--', linewidth=1)
axes[1].set_xlabel("Capacità collegata [pF]", size=15)
axes[1].set_ylabel("Residui [canali]", size=15)
#plt.show()
#plt.savefig("CvsXm.pdf", format="pdf", bbox_inches="tight")
plt.close()


# FIT FWHM contro C
popt2, pcov2= curve_fit(linear, C, fwhm, p0=(0.1, 13.3), sigma=0.1*np.ones(len(C)), absolute_sigma=False)
m2, q2 = popt2[0], popt2[1]
m2err, q2err = np.sqrt( np.diag(pcov2) )
err = np.ones(len(fwhm)) # errore artificiale, array di uno

# CHI QUADRO E RESIDUI FWHM vs C
fit_fwhm = m2* np.array(C) + q2
chi_square2 = np.sum(((fit_fwhm- fwhm)/ err)**2)  
dof2 = len(fwhm) - len(popt2)
chi_norm2 = chi_square2 / dof2
residui2 = [fwhm[i] - fit_fwhm[i] for i in range(len(fwhm))]

print(f"Parametri del fit:\n m={m2}+/-{m2err}\n q={q2}+/-{q2err}\n ")
print(f"il chi2 è: {chi_square2}\nil chi2 normalizzato è: {chi_norm2}")

print('------------')
print('il cavo di capacità incognita ha fwhm di 14.4 canali\n')
Cx = (14.4- q2) / m2 # pF
print(f'secondo il nostro fit questo vuol dire che ha una capacità C={Cx} pF')

# PLOT FWHM vs. C
fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
axes[0].errorbar(C, fwhm, 0.1*np.ones(len(fwhm)), fmt='ro', label='FWHM calcolati\n da maestro')
axes[0].plot(xx, linear(xx, m2, q2), label='fit')
np.delete(C, 2)
np.delete(fwhm, 2)
popt3, pcov3= curve_fit(linear, C, fwhm, p0=(0.2, 13.3), sigma=0.1*np.ones(len(C)), absolute_sigma=False)
axes[0].plot(xx, linear(xx, *popt3), label='fit escludendo 6.5pF')
axes[0].set_ylabel("Larghezza a metà altezza [canali]", size=15)
axes[0].set_xlim(min(C)-1, max(C)+1)
axes[0].legend(loc='lower right', fontsize=15)
axes[1].set_xlim(min(C)-1, max(C)+1)
axes[1].errorbar(C, residui, fmt='bo')
axes[1].axhline(0, color='black', linestyle='--', linewidth=1)
axes[1].set_xlabel("Capacità collegata [pF]", size=15)
axes[1].set_ylabel("Residui [canali]", size=15)
plt.show()
plt.savefig("CvsFWHM.pdf", format="pdf", bbox_inches="tight")
plt.close()