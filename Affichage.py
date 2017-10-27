# -*- coding: utf-8 -*-
# Fichier Affichage.py (fichier supplémentaire)
# Permet de générer un aperçu du découpage de la page pdf


import matplotlib.pyplot as plt

def Affichage_page_quadrillee(Tchar, Vlin, Hlin, Vline = [], Hline = []):
    '''Affiche une page et son quadrillage
        *args : Tchar = liste de caractères sous le format de liste de [(float, float, float, float), char]
                Vlin , Hlin = Lignes définies sous le format d'extraction des lignes du pdf
                Vline, Hline = lignes supplémentaires qui sont crées manuellement sous la forme [float, float, float]
        *out : None                                                            
    '''
    fig, ax = plt.subplots()
    for ch in Tchar:
        x = (ch[0][0] + ch[0][2]) / 2.
        y = (ch[0][1] + ch[0][3]) / 2.
        plt.scatter(x, y, s = 1, c= "blue", marker = ".")
    for l in Vlin:
        plt.plot([l[0], l[0]], [l[1], l[2]], linewidth= 1) #  color = "black"
    for l in Hlin:
        plt.plot([l[1], l[2]], [l[0], l[0]], linewidth= 1)    
    for v in Vline:
        plt.axvline(v)
    for h in Hline:
        plt.axhline(h)
    fig.savefig('image2.png', format='png', dpi=2400)
    return 
    

def Affichage_frequence_projection(V, S):
    '''Affiche le graphique de l'effectif en fonction de la valeur considérée
        *args : V = liste des valeurs
                S = liste des effectifs
        *out : None                                                            
    '''
    plt.plot(V, S)
    plt.show()