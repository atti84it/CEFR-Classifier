
#from .. import numeri as un
from cefr_classifier.utils import numeri as un


def conta_frequenze_di_una_lista(lista):
    from collections import Counter
    return Counter(lista)


def elementi_unici_della_lista(lista):
    return list(set(lista))


def pulisci_lista_parole(lista):
    """
    Data una lista di parole, elimina le parole vuote e le parole con numeri.
    """

    lista_pulita = []
    for parola in lista:
        if parola == "":
            continue
        if any(map(str.isdigit, parola)):
            continue
        lista_pulita += [parola]
    # print(lista_pulita)
    return lista_pulita


def scala_lista(lista, o_min=0, o_max=1):
    """
    Data una lista di valori, li riscala su una scala 0-1, o definita dall'utente.
    """
    nuova = []
    i_min = min(lista)
    i_max = max(lista)
    for x in lista:
        nuova.append(un.scala_numero(x, i_min, i_max, o_min, o_max))
    return nuova


def somma_liste(l1, l2):
    """
    Date due liste di valori, restituisce una terza con la somma dei valori: x0 + y0, x1 + y1, ecc.
    """
    if len(l1) != len(l2):
        raise Exception("Le due liste devono avere numero uguale di elementi")

    l3 = []
    for i in range(len(l1)):
        l3.append(l1[i] + l2[i])
    return l3


def disposizioni_uniche(lista):
    # input [a, b, c, d]
    # output [(a,b), (a,c), (a,d), (b,c), (b,d), (c,d)]
    # dati n elementi, restituisce len = (n * (n-1)) / 2
    finale = []
    while len(lista) > 1:
        base = lista[0]
        resto = lista[1:]
        for elemento in resto:
            finale.append((base, elemento))
        lista = resto
    return finale


def disposizioni_uniche_iter(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            yield lista[i], lista[j]


def disposizioni_uniche_con_distanza_iter(lista, includi_identici=False):
    """
    includi_identici : abilita o no le disposizioni di un elemento con se stesso, cioè distanza = 0
    """
    if includi_identici:
        offset = 0
    else:
        offset = 1

    for i in range(len(lista)):
        for j in range(i + offset, len(lista)):
            yield lista[i], lista[j], j - i


def parola_piu_lunga_di_una_lista(lista):
    parola_maggiore = ""
    for parola in lista:
        if len(parola) > len(parola_maggiore):
            parola_maggiore = parola
    return parola_maggiore


def similitudine_liste(l1, l2):
    d1 = conta_frequenze_di_una_lista(l1)
    d2 = conta_frequenze_di_una_lista(l2)

    punteggio = 0
    for k in d1:
        if k in d2:
            punteggio += min(d1[k], d2[k])

    return (punteggio * 2) / (len(l1) + len(l2))
