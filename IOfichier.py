# -*- coding: utf-8 -*-
# Fichier Arborescence.py
# contient les fonctions qui permettent d'accéder à des fichiers externes

import PyPDF2 # Module de lecture des pdf rapide

def pdf_non_vide(adresse):
    '''Renvoit deux boléens pour savoir si le texte est non vide uniquement dans les 3 premières pages
        *args: adresse : lien complet vers le fichier pdf
        *out: (Bouverture, Btexte) :  Bouverture indique si le fichier est corrompu ou non (False = Corrompu)
                                      Btexte indique si le fichier contient du texte ou non (False = C'est une image)
    '''
    try : 
        flux = open(adresse, 'rb')
        DocPDF = PyPDF2.PdfFileReader(flux)
        n = min(DocPDF.numPages, 3)
        for i in range(n):
            if len(DocPDF.getPage(i).extractText()) > 0:
                flux.close()            
                return (True, True)
        flux.close()
        return (True, False)
    except:
        return (False, '')
        
        
def lire_csv(adresse, nom):
    '''lit un csv basique et renvoit le résultat sous forme de tableau
        *args: adresse : lien vers le répertoire contenant le fichier
               nom : nom du fichier sans extension
        *out : tableau contenant chaque case du csv
    '''
    flux = open(adresse + '/' + nom + '.csv', 'r')
    texte = flux.read()
    L = texte.split("\n")
    T = []
    for l in L:
        T.append(l.split(";"))
    return T
    
    
def ecrire_csv(adresse, nom, T):
    '''permet d'écrire un tableau dans un csv (nom sans extension) peu importe le format des colonnes
        *args: adresse : adresse du fichier
               nom : nom du fichier sans extension
               T : tableau à écrire
        *out : None
    '''
    flux = open(adresse + "/" + nom + ".csv", "w")
    for t in T:
        ligne = ''
        for element in t:
            ligne += str(element) + ';'
        ligne = ligne[:len(ligne)-1] + '\n'
        flux.write(ligne)
    flux.close()
    return