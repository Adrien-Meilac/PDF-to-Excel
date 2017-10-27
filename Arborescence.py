# -*- coding: utf-8 -*-
# Fichier Arborescence.py
# contient les fonctions qui facilitent l'accès à l'arborescence


import os 
import shutil # Pour déplacer des fichiers
import VarGlobale as vg

def liste_sous_chemin(chemin_parent):
    '''Renvoit l'arborescence (au premier niveau uniquement)
        *args = chemin_parent : chemin dont on veut écrire l'aborescence
        *out = (fichier, repertoire) avec des liens sous forme de noms (chemin relatifs et non absolus)
    '''
    L = os.listdir(chemin_parent)
    F = [] # Stocke les liens des fichiers
    R = [] # Stocke les liens des repertoires
    for lien in L:
        if os.path.isfile(chemin_parent + "/" + lien): #teste si le lien est un fichier ou un répertoire
            F.append(lien)
        else :
            R.append(lien)
    return (F, R)    

    
def liste_pdf(chemin):
    '''Renvoit la liste des noms des fichiers pdf (avec extension)
        *ags = chemin : répertoire qui contient les pdfs
        *out = F : liste de string
        '''
    (F, _) = liste_sous_chemin(chemin)
    for i in reversed(range(len(F))):
        (fname, ext) = os.path.splitext(F[i]) # coupe le nom du fichier de l'extension
        if ext != ".pdf":
            del(F[i])
    return F
    
    
def creation_repertoire_compte_par_copie(chemin, lien = "S:/CAM/POLE_DONNEES/Adrien/ScriptSellementComptes/Comptes_selles", noprint = False):
    '''Déplacement et réorganisation des fichiers en dossiers par identifiant EPN
        *args : id_EPN : identifiant du compte
                chemin : lien vers le répertoire dans lequel on veut créer un fichier par id
                lien : lien vers le répertoire qui contient les fichiers non triés
        *out : None
        
    Attention, effectuer le tri depuis un répertoire qui n'est pas sur l'ordinateur prend plus de temps
    '''
    if not os.path.exists(chemin): # Création du dossier pour le compte d'identifiant id_EPN
            os.mkdir(chemin)
    (_, R) = liste_sous_chemin(lien)
    for r in R:
        (F, _) = liste_sous_chemin(lien + '/' + r)
        if not os.path.exists(chemin + '/' + r): # Création du dossier pour le compte d'identifiant id_EPN
            os.mkdir(chemin + '/' + r)
        for f in F:
            (fname, ext) = os.path.splitext(f)
            L = fname.split("_")
            if len(L) >= 2 and L[1] in vg.type_recherches:
                if not noprint:
                    print(chemin + '/' + r + '/' + f)
                shutil.copyfile(lien + '/' + r + '/' + f, chemin + '/' + r + '/' + f)
    return
