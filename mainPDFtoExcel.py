# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 14:15:54 2017

@author: ameilac
"""
#import pdftables_api
#
#c = pdftables_api.Client('my-api-key',)
#c.xlsx('PDF_CR_0000245567_2016.pdf', 'output.xlsx')

import PDFcomprehension as comp
import Quadrillage as qu
import Affichage as aff
import EcritureExcel as ex
import IOfichier as io
from copy import deepcopy
import Arborescence as arb

chemin = "./Comptes_selles"
arb.creation_repertoire_compte_par_copie(chemin) # (lien = endroit ou sont stockés les EPN)


(_, R) = arb.liste_sous_chemin(chemin)
Erreur = []
for r in R:
    F = arb.liste_pdf(chemin + '/' + r)
    for f in F:
        (Bouverture, Btexte) = io.pdf_non_vide(chemin + '/' + r + '/' + f)
        if Bouverture == True and Btexte == True:
            try :
                ex.conversion(chemin + '/' + r, f, chemin + '/' + r, niveau_de_souplesse = 0)
                statut = "Done"
            except :
                Erreur.append([chemin + '/' + r + '/' + f])
                statut = "Error"
            print(statut + '\t' + chemin + '/' + r + '/' + f)
                               
io.ecrire_csv(".", "erreurs", Erreur)

T = io.lire_csv(".", "erreurs")

Erreur = []
for t in T:
    L = t[0].split("/")
    (lien, f) = ("/".join(L[:len(L)-1]), L[-1])
    Berreur = ex.conversion(lien, f, lien, niveau_de_souplesse = 1)
    print(lien + '/' + f)