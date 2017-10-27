# -*- coding: utf-8 -*-
import sqlite3
import VarGlobale as vg
import IOfichier as io
import os 
import shutil
import Arborescence as arb

def copy_base_SQL(chemin = "S:/CAM/POLE_DONNEES/Adrien/ScriptSellementComptes/sellements.db", lien = './sellements.db'):
    shutil.copyfile(chemin, lien)

def complement_excel_SQL():
    '''Créer un inventaire des fichiers de l'arborescence des comptes sellés en SQL
    '''
    conn = sqlite3.connect('sellements.db')
    cursor = conn.cursor()
    Lcol = ["lien", "repertoire", "nom_fichier", "idEPN", "abreviation", "type_doc", "code_budgetaire", "compteur_unique", "annee", "extension", "etat"]
    (_, R) = arb.liste_sous_chemin(vg.adresseSauvegardeRep)
    for r in R:
        data = {"idEPN" : r}
        L = cursor.execute("""SELECT * FROM sellements_comptes WHERE idEPN = :idEPN AND ext = "pdf" """, data).fetchall()
        for f in L:
            (fname, ext) = os.path.splitext(f)
            if os.path.isfile(vg.adresseSauvegardeRep + '/' + r + '/' + fname + ".xlsx"):
                data["etat"] = 
        (F, _) = arb.liste_sous_chemin(vg.adresseSauvegardeRep + '/' + r)
        for f in F:
            
            L = fname.split("_")
            ext = ext[1:]
            if ext == "xlsx":
                print(vg.adresseSauvegardeRep + '/' + r + '/' + f)
                if Bouverture == False:
                    etat = "Corrompu"
                elif Bouverture == True and Btexte == True:
                    etat = "Lisible"
                else: 
                    etat = "Image"
            elif ext == "txt":
                etat = "Existant"
            if len(L) == 6:
                data = {"extension" : ext, "lien" : vg.adresseSauvegardeRep + '/' + r + '/' + f, "nom_fichier" : f, "repertoire": vg.adresseSauvegardeRep + '/' + r , "etat" : etat}
                for j in range(3, 9):
                    data[Lcol[j]] = L[j - 3]
                cursor.execute("""INSERT INTO sellements_comptes({0}) VALUES({1});""".format(", ".join(Lcol), ":" + ", :".join(Lcol)), data)
                conn.commit()
    conn.close()    
    
def tous_types_sont_dedans(id_EPN, anneeRef):
    '''Cherche à savoir si dans un répertoire, les types recherchés sont bien dedans (version 1 uniquement)
        *args : id_EPN : identifiant dans le site
                anneeRef : année dont on veut fournir l'analyse (Attention, stockée comme un entier)
        *out : F_est_dedans : liste de 14 variable qui indique le statut de chacun des documents recherchés (variable globale) en txt puis en pdf
    '''
    p = len(vg.type_recherches)
    F_est_dedans = ["Non existant"] * p
    (F, _) = arb.liste_sous_chemin(vg.adresseSauvegardeRep + '/' + id_EPN)
    for f in F:
        (fname, ext) = os.path.splitext(f)
        L = fname.split("_")
        if ext == ".xlsx" and len(L) == 3: # Si le fichier est un excel et que la nomenclature est lisible :
             [_, ftype, annee] = L
             if annee == str(anneeRef):
                for k in range(p):
                    if ftype == vg.type_recherches[k]:
                        F_est_dedans[k] = "Existant"
    return F_est_dedans

def base_SQL_conversion(anneeRef):
    '''Réalisation des calculs sur tout les comptables pour une année donnée (dans les dossiers de chargement, il peut y avoir plusieurs années)
        *args : anneeRef : entier
        * out : None
    '''
    xls = ["xls_" + vg.type_recherches[i] for i in range(len(vg.type_recherches))]
    Lcol = ["id_EPN"] + xls
    conn = sqlite3.connect('sellements.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversion_excel(
         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, {});""".format(" TEXT,".join(Lcol)))
    conn.commit()
    T_sell = io.lire_csv(".", "Liste_comptes_selles")
    n = len(T_sell)
    for i in range(n):
        if len(T_sell[i]) >= 2:
            id_EPN = T_sell[i][0]
            print(id_EPN)
            F = [id_EPN] +  tous_types_sont_dedans(id_EPN, anneeRef)
            data = {}
            for j in range(len(F)):
                data[Lcol[j]] = F[j]
            cursor.execute("""INSERT INTO conversion_excel({0}) VALUES({1});""".format(", ".join(Lcol), ":" + ", :".join(Lcol)), data)
    conn.commit()
    conn.close()
    return
    
#base_SQL_conversion(2016)

def SQL_requete():
    conn = sqlite3.connect('sellements.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT COUNT(*) FROM sellements WHERE (
    (txt_CR == "Non existant" AND  pdf_CR != "Texte") OR
    (txt_BILAN == "Non existant" AND pdf_BILAN != "Texte") OR
    (txt_SPE1 == "Non existant" AND pdf_SPE1 != "Texte") OR
    (pdf_BAL != "Texte") OR
    (txt_ABE == "Non existant" AND pdf_ABE != "Texte") OR
    (txt_TEF == "Non existant" AND pdf_TEF != "Texte")
    )
    """)
    rows = cursor.fetchone()
    print(rows[0])
    cursor.execute("""SELECT COUNT(*) FROM sellements WHERE (
    (txt_CR == "Non existant" AND  pdf_CR == "Image") OR
    (txt_BILAN == "Non existant" AND pdf_BILAN == "Image") OR
    (txt_SPE1 == "Non existant" AND pdf_SPE1 == "Image") OR
    (pdf_BAL == "Image") OR
    (txt_ABE == "Non existant" AND pdf_ABE == "Image") OR
    (txt_TEF == "Non existant" AND pdf_TEF == "Image")
    )
    """)
    rows = cursor.fetchone()
    print(rows[0])
    cursor.execute("""SELECT COUNT(*) FROM sellements WHERE (
    (txt_CR == "Non existant" AND  pdf_CR == "Corrompu") OR
    (txt_BILAN == "Non existant" AND pdf_BILAN == "Corrompu") OR
    (txt_SPE1 == "Non existant" AND pdf_SPE1 == "Corrompu") OR
    (pdf_BAL == "Corrompu") OR
    (txt_ABE == "Non existant" AND pdf_ABE == "Corrompu") OR
    (txt_TEF == "Non existant" AND pdf_TEF == "Corrompu")
    )
    """)
    rows = cursor.fetchone()
    print(rows[0])
    cursor.execute("""SELECT COUNT(*) FROM sellements WHERE (
    (txt_CR == "Non existant" AND  pdf_CR == "Non existant") OR
    (txt_BILAN == "Non existant" AND pdf_BILAN == "Non existant") OR
    (txt_SPE1 == "Non existant" AND pdf_SPE1 == "Non existant") OR
    (pdf_BAL == "Non existant") OR
    (txt_ABE == "Non existant" AND pdf_ABE == "Non existant") OR
    (txt_TEF == "Non existant" AND pdf_TEF == "Non existant")
    )
    """)
    rows = cursor.fetchone()
    print(rows[0])
    conn.close()
    return

    
    
    