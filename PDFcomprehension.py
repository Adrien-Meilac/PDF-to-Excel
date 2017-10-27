# -*- coding: utf-8 -*-

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTFigure
from pdfminer.pdfpage import PDFPage
from copy import deepcopy
import operator # Pour trier les listes

def extraction_texte(layout):
    """Fonction qui trouve les caractères et leur position dans une page
        *args: layout: source de pdfminer
        *out: liste du type [(float, float, float, float), char]
        """
    T = []
    for lt_obj in layout:
        if lt_obj.__class__.__name__ == "LTChar":
            T.append([lt_obj.bbox, lt_obj.get_text()])
        if isinstance(lt_obj, LTFigure):
            T.extend(extraction_texte(lt_obj))  # Recursive
    return T

    
def extraction_ligne(layout):
    """Fonction qui trouve les lignes et leur position dans une page
        *args: layout: source de pdfminer
        *out: liste du type [(float, float, float, float), char]
        """
    T = []
    for lt_obj in layout:
        if lt_obj.__class__.__name__ == "LTLine":
            T.append(lt_obj.bbox)
        if isinstance(lt_obj, LTFigure):
            T.extend(extraction_ligne(lt_obj))  # Recursive
    return T
   
    
def extraction_rect(layout):
    """Fonction qui trouve les rectangles et les rectangles mal codés et leur position dans une page
        *args: layout: source de pdfminer
        *out: liste du type [(float, float, float, float), char]
        """
    T = []
    for lt_obj in layout:
        if lt_obj.__class__.__name__ == 'LTRect' or lt_obj.__class__.__name__ == 'LTCurve' :
            T.append(lt_obj.bbox)
        if isinstance(lt_obj, LTFigure):
            T.extend(extraction_rect(lt_obj))  # Recursive
    return T
    
    
def lecture_explosee_fichier(lien, f):
    '''Renvoit une arborescence des caractères (uniquement les char) dans un fichier pdf page par page
        *args = lien: lien vers le repertoire contenant le dossier
                f : nom du fichier (pdf uniquement)
        *out = T:  liste de tableau qui correspondent aux pages. Sur chaque page on a :
            [(xpos, ypos, xpos2, ypos2) qui encadrent la position d'un caractère
            char le caractère]
    '''
    fp = open(lien + "/" + f, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    Char = []
    Lin = []
    Rect = []
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        Char.append(extraction_texte(layout))
        Lin.append(extraction_ligne(layout))
        Rect.append(extraction_rect(layout))
    return (Char , Lin, Rect)

    
def separation_tlin(Tlin):
    '''Sépare les lignes verticales et les lignes horizontales.
        *args : Tlin : liste du genre [(float, float, float, float), char]
        *out :(Vlin, Hlin): Chacun des deux est une liste de la forme [float, float, float] qui représente :
            -> la position du trait verticale
            -> les positions horizontales du trait verticales (triées)
    '''
    Vlin = []
    Hlin = []
    for lin in Tlin:
        if lin[0] == lin[2]:
            if lin[1] <= lin[3]:
                Vlin.append(deepcopy([lin[0], lin[1], lin[3]]))
            else :
                Vlin.append(deepcopy([lin[0], lin[3], lin[1]]))
        if lin[1] == lin[3]:
            if lin[0] <= lin[2]:
                Hlin.append(deepcopy([lin[1], lin[0], lin[2]]))
            else :
                Hlin.append(deepcopy([lin[1], lin[2], lin[0]]))
    return (Vlin, Hlin)
    
    
def separation_trec(Trect):
    '''Divise les rectangles et les courbes qui ont été mal codés pour les transformer en lignes
        *args : Trect : liste du genre [(float, float, float, float), char]
        *out :(Vlin, Hlin): Chacun des deux est une liste de la forme [float, float, float] qui représente :
            -> la position du trait verticale
            -> les positions horizontales du trait verticales (triées)
    '''
    Vlin = []
    Hlin = []
    for rect in Trect:  
        if rect[0] <= rect[2]:
            hlin1 = deepcopy([rect[1], rect[0], rect[2]]) 
            hlin2 = deepcopy([rect[3], rect[0], rect[2]]) 
        else :
            hlin1 = deepcopy([rect[1], rect[2], rect[0]]) 
            hlin2 = deepcopy([rect[3], rect[2], rect[0]]) 
        if rect[1] <= rect[3]:
            vlin1 = deepcopy([rect[0], rect[1], rect[3]]) 
            vlin2 = deepcopy([rect[2], rect[1], rect[3]]) 
        else:
            vlin1 = deepcopy([rect[0], rect[3], rect[1]]) 
            vlin2 = deepcopy([rect[2], rect[3], rect[1]])             
        Vlin.append(vlin1)
        Vlin.append(vlin2)
        Hlin.append(hlin1)
        Hlin.append(hlin2)
    return (Vlin, Hlin)


        
def association_ligne(T):
    '''Agrège les lignes qui se touchent et vont dans la même direction, cela permettra de reconnaitre les axes principaux
        *args : T : liste du genre [float, float, float]
        *out :(Vlin, Hlin): Chacun des deux est une liste de la forme [float, float, float] qui représente :
            -> la position du trait verticale
            -> les positions horizontales du trait verticales (triées)
    '''
    n =len(T)
    # Trie de la liste selon les deux premiers indices pour améliorer la complexité de l'algorithme suivant
    T = sorted(T, key=operator.itemgetter(0))
    Ttrie = []
    est_dedans = lambda i: i < 0
    for i in range(n):
        if not est_dedans(i):
            j = 1
            while i + j < n and T[i][0] == T[i + j][0]:
                j += 1
            V = sorted(T[i : i + j], key=operator.itemgetter(1))
            Ttrie.extend(deepcopy(V))
            a = i + j
            est_dedans = lambda x: x < a
    # Fusion des lignes consécutives :
    for i in reversed(range(1,n)):
        if Ttrie[i-1][0] == T[i][0] and Ttrie[i][1] == Ttrie[i-1][2]:
            Ttrie[i-1][2] = Ttrie[i][2]
            del(Ttrie[i])
    for i in reversed(range(1,len(Ttrie))):
        if Ttrie[i] == Ttrie[i-1]:
            del(Ttrie[i])
    return Ttrie


def simplification_ligne(Tlin, Trect):
    ''' Effectue automatiquement toutes les étapes de simplification des lignes
        *args : Tlin, Trect : tous les tracés qu'il faut étudier
        *out : toutes les lignes présentes dans le document sous forme de couple de liste
    '''
    (Vlin, Hlin) = separation_tlin(Tlin)
    (Vlin2, Hlin2) = separation_trec(Trect)
    Vlin.extend(Vlin2)
    Hlin.extend(Hlin2)
    return (association_ligne(Vlin), association_ligne(Hlin))

    
def axes_principaux(T):
    ''' Regarde les axes majeurs du fichier, ils vont servir de découpage simplifié
        *args :  T, tableau de ligne du genre [float, float, float]
        *out : i_principaux : liste d'indice
    '''
    L = [T[i][2] - T[i][1] for i in range(len(T))]
    m = sum(L)/len(L)* 0.95 
    i_principaux = []
    for i in range(len(T)):
        if L[i] >= m:
            i_principaux.append(i)
    return i_principaux