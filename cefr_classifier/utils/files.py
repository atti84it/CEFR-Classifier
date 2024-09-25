def carica_testo(percorso_file):
    with open(percorso_file, "r", encoding='utf-8') as file:
        contenuto = file.read()
    return contenuto


def parti_di_file_iter(percorso_completo):
    """
    per leggere un file QCER che all'interno è diviso in parti separate da 4 ritorni a capo
    """
    contenuto = carica_testo(percorso_completo)

    if "\n\n\n" in contenuto:
        if "\n\n\n\n" not in contenuto:
            print("SUS: solo 3returns in", percorso_completo)
    parti = contenuto.split("\n\n\n\n")

    for i in range(len(parti)):
        parte = parti[i].strip()
        if parte == "":
            print('Salto parte vuota')
            continue
        yield parte, i


def leggi_linee_da_file(percorso_file):
    # input: un file che contiene una lista di files, o di parole
    # output: una lista del contenuto delle linee, eliminando \n finale
    with open(percorso_file, 'r', encoding='utf-8') as file:
        lista_linee = []
        linea = file.readline()
        while linea:
            linea = linea.strip()
            lista_linee += [linea]
            linea = file.readline()
        return lista_linee


def leggi_linee_da_file_iter(percorso_file):
    """
    Legge un file una linea alla volta. Poiché usa yield bisogna usare for linea in leggi...
    """
    with open(percorso_file, 'r', encoding='utf-8') as file:
        for linea in file:
            yield linea.strip()


def leggi_linee_da_file_iter_old(percorso_file):
    """
    Legge un file una linea alla volta. Poiché usa yield bisogna usare for linea in leggi...
    """
    with open(percorso_file, 'r', encoding='utf-8') as file:
        linea = file.readline().strip()
        while linea:
            yield linea
            linea = file.readline().strip()


def carica_e_unwrap_testo(percorso_completo):
    """
    In: percorso file di testo
    Out: testo ricostruito (word wrap)
    """
    import os
    from cefr_classifier.utils import unwrapper as uw

    if os.path.isfile(percorso_completo):
        with open(percorso_completo, "r", encoding='utf-8') as file:
            contenuto = file.read()
        contenuto = uw.unwrap_testo(contenuto)
        return contenuto


def diz_freq_a_csv(diz, separatore=","):
    # in: dizionario di frequenze
    # out: stringa pronta da scrivere in un file .csv
    stringa = ""
    for parola in diz.keys():
        stringa = stringa + str(parola) + separatore + str(diz[parola]) + "\n"
    return stringa


def diz_freq_a_file_csv(percorso_file, diz, separatore=","):
    with open(percorso_file, 'w', encoding='utf-8') as file:
        file.write(diz_freq_a_csv(diz, separatore=separatore))


def diz_freq_a_csv_iter(diz, separatore=","):
    # in: dizionario di frequenze
    # out: stringa pronta da scrivere in un file .csv
    for parola in diz.keys():
        yield str(parola) + separatore + str(diz[parola]) + "\n"


def file_csv_a_dizionario(percorso, separatore=","):
    contenuto = carica_testo(percorso)
    return csv_a_dizionario(contenuto, separatore)


def csv_a_dizionario(testo, separatore=","):
    # in: stringa che viene da un file .csv
    # out: dizionario di frequenze !!!INT!!!!
    diz_frequenze = {}
    linee = testo.split("\n")

    for linea in linee:
        if linea != "":
            chiave, valore = linea.split(separatore)
            if valore.strip().isdigit():
                diz_frequenze[chiave] = int(valore)
    return diz_frequenze


def file_jsonl_a_lista(percorso_file):
    import json
    lista = []
    with open(percorso_file, 'r', encoding='utf-8') as file:
        for linea in file:
            lista.append(json.loads(linea))
    return lista


def lista_a_file_jsonl(percorso_file, lista):
    import json
    with open(percorso_file, 'w', encoding='utf-8') as file:
        for elem in lista:
            file.write(json.dumps(elem) + "\n")


def appendi_elem_in_file_jsonl(percorso_file, elem):
    import json
    with open(percorso_file, 'a', encoding='utf-8') as file:
        file.write(json.dumps(elem) + "\n")


def lista_di_tuple_a_csv(lista, separatore=','):
    # TODO da scrivere bene, adesso non funziona, ma ho preparato almeno la funzione map
    for elem in lista:
        separatore.join(map(str, dato)) + '\n'
