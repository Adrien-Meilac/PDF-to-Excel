# -*- coding: utf-8 -*-

def liste_position_projete(axeNum, Tpos):
    '''Renvoit la liste des positions en abscisses projetées
        *args = axeNum: 0 si abcisse
                        1 si ordonnee
                Tpos: tableau de la forme d'une page de lecture_explosee_fichier
        *out
    '''
    n = len(Tpos)
    M = []
    for k in range(n):
        a = (Tpos[k][0][axeNum] + Tpos[k][0][axeNum + 2]) / 2.
        M.append(a)
    M.sort()
    return M
    
def frequence_echantillonage(M, sensibilite):
    V = []
    S = []
    for k in range(sensibilite):
        a = M[0] + k * (M[-1] - M[0]) / sensibilite
        b = M[0] + (k + 1) * (M[-1] - M[0]) / sensibilite
        compteur = 0
        for i in range(len(M)):
            if M[i] >= a  and M[i] <= b:
                compteur += 1
        V.append((a + b) / 2)
        S.append(compteur)
    return (V, S)
    
def valeurs_frequence_minimum(V, S, seuil):
    Imin = []
    for i in range(len(S)):
        if S[i] <= seuil:
            Imin.append(i)
     
    val = []
    fait = lambda i: False
    for i in range(len(Imin)):
        if not fait(i):
            M = Imin[i]
            j = i
            while j < len(Imin) and M + j - i == Imin[j]:
                j += 1
            val.append(V[Imin[(i+j)//2]])
            fait = lambda i: i < j
    return val
        