#from .strings import some_string_function
#from .lists import some_list_function

def ordina_dizionario_per_chiavi(dizionario):
    lista = sorted(dizionario.items(), key=lambda x: x[0])
    sortdict = dict(lista)
    return sortdict


def ordina_dizionario_per_frequenza(dizionario):
    lista = sorted(dizionario.items(), key=lambda x: x[1], reverse=True)
    sortdict = dict(lista)
    return sortdict


def ordina_dizionario_per_lunghezza_delle_chiavi(dizionario):
    lista = sorted(dizionario.items(), key=lambda x: len(x[0]), reverse=True)
    sortdict = dict(lista)
    return sortdict


def aggrega_dizionari(diz1, diz2):
    # riceve due dizionari
    # restituisce un terzo dizionario in cui le chiavi sono l'unione dei due dizionari, e i valori sono la somma delle frequenze di entrambi
    for chiave in diz2.keys():
        if chiave in diz1.keys():
            diz1[chiave] += diz2[chiave]
        else:
            diz1[chiave] = diz2[chiave]
    return diz1


def aggiunge_diz_a_diz(dizionario, chiave, elemento):
    # inserisce k, v in un dizionario
    # chiave = "are" (= rima)
    # elemento = {"A1" : 0.0003}
    if chiave in dizionario:  # se l'elemento esiste lo aggiorna
        dizionario[chiave].update(elemento)
    else:  # altrimenti lo aggiunge
        dizionario[chiave] = elemento
    return dizionario


def porzione_diz(diz, quante):
    """
    In: dizionario di frequenze
    Out: dizionario di frequenze: le top n ("quante") del dizionario originale

    # equivalente a diz[:quante] che dà l'errore "unhashable type: 'slice'"
    """
    quante = int(quante)
    diz = ordina_dizionario_per_frequenza(diz)
    chiavi = list(diz)[:quante]
    nuovo_diz = {}
    for chiave in chiavi:
        nuovo_diz[chiave] = diz[chiave]
    return nuovo_diz


def moltiplica_diz(dizionario, moltiplicatore):
    """
    Restituisce lo stesso dizionario moltiplicando i valori per "moltiplicatore"
    in: diz {k: numeric}
    out: diz {k: num * mult}
    """
    nuovo_diz = {}
    for chiave in dizionario.keys():
        nuovo_diz[chiave] = dizionario[chiave] * moltiplicatore
    return nuovo_diz
