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
Xm = [418.0, 417.5, 417.5, 417.3, 417.2] # chan
fwhm = [13.3, 13.8, 16.5, 15.1, 15.9] # chan

# FIT Xm contro C
popt, pcov= curve_fit(linear, C, Xm, p0=(-0.0001, 418), absolute_sigma=False)
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
xx = np.linspace(min(C), max(C), 1000)
plt.figure()
plt.scatter(C, Xm, fwhm, zorder=2, label='picchi calcolati\n da maestro')
plt.plot(xx, linear(xx, m, q), zorder=1, label='fit')
plt.xlabel("Capacità collegata [pF]", size=15)
plt.ylabel("posizione picco Xm [canali]", size=15)
plt.ylim(415, 420)
plt.legend(loc='best')
plt.savefig("CvsXm.pdf", format="pdf", bbox_inches="tight")
plt.close()


# FIT FWHM contro C
popt2, pcov2= curve_fit(linear, C, fwhm, p0=(0.1, 13.3), absolute_sigma=False)
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
print(f"il chi2 è: {chi_square}\nil chi2 normalizzato è: {chi_norm}")

print('------------')
print('il cavo di capacità incognita ha fwhm di 14.4 canali\n')
Cx = (14.4- q2) / m2 # pF
print(f'secondo il nostro fit questo vuol dire che ha una capacità C={Cx} pF')

# PLOT FWHM vs. C
plt.figure()
plt.scatter(C, fwhm, zorder=2, label='FWHM calcolati\n da maestro')
plt.plot(xx, linear(xx, m2, q2), zorder=1, label='fit')
plt.xlabel("Capacità collegata [pF]", size=15)
plt.ylabel("Larghezza a metà altezza [canali]", size=15)
plt.ylim(10, 20)
plt.legend(loc='best')
plt.savefig("CvsFWHM.pdf", format="pdf", bbox_inches="tight")
plt.close()