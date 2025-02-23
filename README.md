# SinglePhotonCounting
Esperienza tre del corso di LabMedicalPhysics

Giorno 1: 
primi task, come prima cosa si fa la calibrazione con il segnale di test (task01),  poi una misura di come cambia FWHM del picco osservato al variare delle capacità collegate alla catena di acquisizione.

Giorno 2:
Riprese le misure test del signale simulato dell'Americio, prima senza detector e senza alimentazione (test_35dB_2.7mV) e dopo con il detector per diverse alimentazioni (regione_svuotamento).
Abbiamo poi preso una misura del segnale test con alimentazione a 12V (test_35dB_2.7mV_alimentato12V). 
Osservata discrepanza sui canali di ben 70 chan, test 414.6+-16.7(FWHM) mentre sorgente 344.6+-16.9, l'errore è sensato ma il canale non corrisponde, perché? Perché per calcolare la tensione da somministrare (2.7mV) abbiamo utilizzato una capacità nominale da 1pF che risulta essere in realtà più grande (sembra) dunque il segnale test dovrebbe avere una ddp inferiore per trovarsi nel canale 344 come il segnale da 60keV.

Osservati gli spettri dell'americio e delle fluorescenze del nettunio, anche la risoluzione spettrale dei picchi a bassa energia non permette di realizzare una calibrazione in energia. inseriamo dunque dei fogli di materiale puro (Mo, Sn, Gd, Zn) con diverso spessore in modo tale da evidenziare vari picchi di fluorescenza. Su questi FARE FIT DI CALIBRAZIONE.

Giorno 3:
Misure di attenuazione inserendo man mano lastrine il cui spessore è stato preso con un calibro ventesimale.
