# -*- coding: utf-8 -*-
from copy import deepcopy, copy
import operator
import  xlsxwriter
import PDFcomprehension as comp
import Quadrillage as qu
import os


def reconnaissance_case(Tchar, Vlin, Hlin):
    Case = {}
    Hlength = len(Hlin)
    for ch in Tchar:
        ch = deepcopy(ch)
        (v1, h1, v2, h2) = ch[0]
        h = (h1 + h2) / 2.
        v = (v1 + v2) / 2.
        if v <= Vlin[0]:
            ipos = 0
        elif v > Vlin[-1]:
            ipos = len(Vlin)
        else:
            for i in range(len(Vlin)-1):
                if v >= Vlin[i] and v < Vlin[i+1]:
                    ipos = i
                    break
        if h <= Hlin[0]:
            jpos = Hlength + 1
        elif h > Hlin[-1]:
            jpos = 0
        else:
            for j in range(len(Hlin)-1):
                if h >= Hlin[j] and h < Hlin[j+1]:
                    jpos = Hlength - j
                    break
        if (ipos, jpos) in Case:
            Case[(ipos, jpos)].append(ch)
        else:
            Case[(ipos, jpos)] = [ch]
    return Case
    
def reconstitution_mot(Case):
    for (i,j) in Case.keys():
        L = []
        for ligne in Case[i,j]:
            L.append([ligne[0][p] for p in range(3)] + [ligne[1]])
        L = sorted(L, key=operator.itemgetter(0))
        mot = "".join([L[p][-1] for p in range(len(L))])
        Case[(i,j)] = mot
    return Case

def ecriture_excel(Cases, repDoc, nomDoc):
    workbook = xlsxwriter.Workbook(repDoc + "/" + nomDoc +".xlsx") #Création d'un fichier excel
    for k in range(len(Cases)):
        Case = Cases[k]
        worksheet = workbook.add_worksheet("Page {}".format(str(k+1))) # Création de la feuille de statistique
        for (i, j) in Case.keys():
            worksheet.write(j, i, Case[(i,j)])
    workbook.close()    
    return 
    
def conversion(cheminDoc, nomDoc, cheminSauv, niveau_de_souplesse = 0):
    (TC, TL, TR) = comp.lecture_explosee_fichier(cheminDoc, nomDoc)
    n_page = len(TC)
    produit_une_erreur = False
    Cases = []
    for k in range(n_page):
        Tpos = TC[k]
        Tlin =  TL[k]
        Trect = TR[k]
        (Vlin, Hlin) = comp.simplification_ligne(Tlin, Trect)
        if niveau_de_souplesse == 0:
            ip = comp.axes_principaux(Vlin)
            VlinP = []
            for i in ip:
                VlinP.append(Vlin[i][0])
            VlinP = sorted(list(set(VlinP)))
            (V, S) = qu.frequence_echantillonage(qu.liste_position_projete(1, Tpos), 300) # seuils à bouger si ça ne marche pas
            Hline = qu.valeurs_frequence_minimum(V, S, 0) # seuils à bouger si ça ne marche pas
            Hline = sorted(list(set(Hline)))
            CaseA = reconstitution_mot(reconnaissance_case(Tpos, VlinP, Hline))
            LX = []
            LY = []
            L = CaseA.keys()
            for (p, q) in L:
                LX.append(p)
                LY.append(q)
            LX = sorted(list(set(LX)))
            LY = sorted(list(set(LY)))
            def transformation(x, y, LX, LY):
                for pp in range(len(LX)):
                    if LX[pp] == x:
                        x_pos = pp
                        break
                for qq in range(len(LY)):
                    if LY[qq] == y:
                        y_pos = qq
                        break
                return (x_pos, y_pos)
            Case = {}
            for (p, q) in L:
                Case[transformation(p, q, LX, LY)] = CaseA[(p, q)]
            Cases.append(Case)
        elif niveau_de_souplesse == 1:
            try :
                ip = comp.axes_principaux(Vlin)
                VlinP = []
                for i in ip:
                    VlinP.append(Vlin[i][0])
                VlinP = sorted(list(set(VlinP)))
                (V, S) = qu.frequence_echantillonage(qu.liste_position_projete(1, Tpos), 300) # seuils à bouger si ça ne marche pas
                Hline = qu.valeurs_frequence_minimum(V, S, 0) # seuils à bouger si ça ne marche pas
                Hline = sorted(list(set(Hline)))
                CaseA = reconstitution_mot(reconnaissance_case(Tpos, VlinP, Hline))
                LX = []
                LY = []
                L = CaseA.keys()
                for (p, q) in L:
                    LX.append(p)
                    LY.append(q)
                LX = sorted(list(set(LX)))
                LY = sorted(list(set(LY)))
                def transformation(x, y, LX, LY):
                    for pp in range(len(LX)):
                        if LX[pp] == x:
                            x_pos = pp
                            break
                    for qq in range(len(LY)):
                        if LY[qq] == y:
                            y_pos = qq
                            break
                    return (x_pos, y_pos)
                Case = {}
                for (p, q) in L:
                    Case[transformation(p, q, LX, LY)] = CaseA[(p, q)]
                Cases.append(Case)
            except :
                if len(Vlin) == 0:
                    Cases.append({})
                else:
                    try:
                        (V, S) = qu.frequence_echantillonage(qu.liste_position_projete(0, Tpos), 200) # seuils à bouger si ça ne marche pas
                        Vline = qu.valeurs_frequence_minimum(V, S, 0) # seuils à bouger si ça ne marche pas
                        Vline = sorted(list(set(Vline)))
                        (V, S) = qu.frequence_echantillonage(qu.liste_position_projete(1, Tpos), 300) # seuils à bouger si ça ne marche pas
                        Hline = qu.valeurs_frequence_minimum(V, S, 0) # seuils à bouger si ça ne marche pas
                        Hline = sorted(list(set(Hline)))
                        CaseA = reconstitution_mot(reconnaissance_case(Tpos, Vline, Hline))
                        LX = []
                        LY = []
                        L = CaseA.keys()
                        for (p, q) in L:
                            LX.append(p)
                            LY.append(q)
                        LX = sorted(list(set(LX)))
                        LY = sorted(list(set(LY)))
                        def transformation(x, y, LX, LY):
                            for pp in range(len(LX)):
                                if LX[pp] == x:
                                    x_pos = pp
                                    break
                            for qq in range(len(LY)):
                                if LY[qq] == y:
                                    y_pos = qq
                                    break
                            return (x_pos, y_pos)
                        Case = {}
                        for (p, q) in L:
                            Case[transformation(p, q, LX, LY)] = CaseA[(p, q)]
                        Cases.append(Case)
                    except :
                        Cases.append({})
                produit_une_erreur = True
    (fname, ext) = os.path.splitext(nomDoc)
    if niveau_de_souplesse == 0:
        ecriture_excel(Cases, cheminSauv, fname)
    elif niveau_de_souplesse == 1: 
        ecriture_excel(Cases, cheminSauv, fname + '#')
    return produit_une_erreur
    