import sys
import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import os

from . import liste as hl
from . import dizionari as hd


def dividi_testo_in_frasi_old_deprecato(testo=""):
    # TODO al momento si perde il separatore (.?!)
    #  bisogna modificare la funzione in modo da rimetterlo alla fine del testo

    # tokens = re.split("[ :;'?=()!\\[\\]-]+|(?<=\\d)(?=\\D)", self.testo)
    tokens = re.split(r"[\n?!.…]", testo)
    tokens = [token.strip() for token in tokens if len(token) > 1]
    return tokens


def dividi_testo_in_frasi(testo=""):
    separatori = r"\. \? ! \n … : ;\n".split(" ")
    testo = testo.strip()
    frammenti = [testo]
    for separatore in separatori:

        parziali = []
        for frammento in frammenti:
            ris = re.split(separatore, frammento)

            # Se ha spezzato, si è perso il separatore, bisogna riaggiungerlo
            # ciclando su tutti i frammenti meno l'ultimo
            if len(ris) > 1:
                for i in range(len(ris) - 1):
                    if separatore == '\\n':
                        sep = "\n"
                    elif separatore == ';\\n':
                        sep = ';\n'
                    else:
                        sep = separatore.replace('\\', '')
                    ris[i] += sep

            # Giacché ogni separatore spezza il testo e la frase successiva inizia con "spazio", bisogna rimuoverlo
            for i in range(len(ris)):
                ris[i] = ris[i].lstrip()

                # se il frammento non è vuoto, lo aggiungo a quelli validi
                if len(ris[i]) > 1:
                    parziali.append(ris[i])

        frammenti = parziali
    return frammenti


def dividi_testo_in_parole(testo):
    # in: stringa con tutto il testo
    # out: lista contenente le parole

    # words = re.split('[^a-zA-Zàèéìòù]', testo)
    parole = re.split(r'[\W]', testo)
    parole = [ele for ele in parole if ele != ""]
    return parole


def conta_freq_asso_del_testo(testo):
    # in: stringa con tutto il testo
    # out: dizionario di frequenze
    parole_file = dividi_testo_in_parole(testo)
    parole_file = hl.pulisci_lista_parole(parole_file)
    freq_parole = hl.conta_frequenze_di_una_lista(parole_file)
    return hd.ordina_dizionario_per_frequenza(freq_parole)


def evidenzia_espressione(testo_base, da_evidenziare, tag, distanza_aggiuntiva=1):
    """
    Dato un testo_base, rinchiude "da_evidenziare" all'interno di un tag tipo HTML
    Se chiami la funzione con i parametri "per aprire il documento fai clic qui", "clic qui", "a href='...'"
    farà esattamente quello che pensi

    Esempio in grassetto: "inizio passato prossimo fine", "passato prossimo", "strong"

    Marca le parole solo quando parole intere, con \b prima e dopo
    """
    apertura = "<" + tag + ">"
    chiusura = "</" + tag.split(" ")[0] + ">"

    r"""
    vero_evidenziare = re.findall(r"\b" + da_evidenziare + r"\b", testo_base, re.IGNORECASE)

    risultato = testo_base
    for ve in vero_evidenziare:
        risultato = re.sub(f'({ve})', f'{apertura}\g<1>{chiusura}', risultato)
    """
    # print("distanza:", distanza_aggiuntiva, da_evidenziare)

    # sostituisce gli spazi con uno spazio di tolleranza equivalente a '.{1,50}'
    # dove il 50 cambia in base al parametro distanza_aggiuntiva
    # questo deve aumentare ogni volta che si evidenzia un'espressione per consentire di prendere parole sempre più lontane
    distanza = 20 + distanza_aggiuntiva
    rimpiazzo = '.{1,' + str(distanza) + '}'
    da_evidenziare = da_evidenziare.replace(' ', rimpiazzo)
    vero_evidenziare = re.search(r"\b" + da_evidenziare + r"\b", testo_base, re.IGNORECASE)

    if vero_evidenziare:
        ve = vero_evidenziare.group(0)
        # risultato = re.sub(f'({ve})', f'{apertura}\g<1>{chiusura}', testo_base)
        ve = ve.replace(r'(', r'\(')
        ve = ve.replace(r')', r'\)')
        risultato = re.sub(f'({ve})', apertura + r"\g<1>" + chiusura, testo_base)
        return risultato
    else:
        return testo_base


def evidenzia_lista_espressioni(testo_base, lista_espressioni, tag):
    """
    Dato un testo_base, inserisce tutte le espressioni della lista all'interno di un tag.
    Utile per evidenziare multiple keywords all'interno di un testo per mezzo del tag <strong>
    """
    testo_evidenziato = testo_base
    dimensione_prima = len(testo_evidenziato)
    differenza = 0
    for espressione in lista_espressioni:
        testo_evidenziato = evidenzia_espressione(testo_evidenziato, espressione, tag,
                                                  distanza_aggiuntiva=differenza + 1)
        dimensione_dopo = len(testo_evidenziato)
        differenza = dimensione_dopo - dimensione_prima
    return testo_evidenziato


def schema_e_dominio_da_url(url):
    import urllib.parse
    parse_result = urllib.parse.urlparse(url)
    return parse_result.scheme + "://" + parse_result.netloc


def url_a_nome_file_da_salvare(url, estensione_out='.html', controllo='.htm'):
    """
    Data una url restituisce un nome decente per salvare una pagina web
    Esempi url:
        .../nome_risorsa.htm
        .../nome_risorsa.html
        .../nome_risorsa
        .../nome_risorsa/
    Out:
        nome_risorsa.htm(l)
    """
    import urllib.parse
    parse_result = urllib.parse.urlparse(url)
    page_name = parse_result.path.split("/")[-1]  # url tipo .../nome_risorsa
    page_name = page_name.strip()
    if page_name == "":  # url tipo .../nome_risorsa/
        page_name = parse_result.path.split("/")[-2]
    if controllo not in page_name:
        page_name = page_name + estensione_out
    return page_name


def nome_file_senza_estensione(nome_completo):
    return os.path.splitext(nome_completo)[0]


def nome_file_da_percorso(file_path):
    return os.path.basename(file_path)


def similitudine_stringhe(s1, s2):
    """
    Restituisce la similitudine tra due stringhe contando quante parole hanno in comune.
    La similitudine è sempre tra 0 e 1. Similitudine = 1 potrebbe significare che le parole sono uguali ma in ordine diverso.
    """
    l1 = dividi_testo_in_parole(s1)
    l2 = dividi_testo_in_parole(s2)
    return hl.similitudine_liste(l1, l2)


def stringa_finisce_con(stringa, rima):
    # restituisce Boolean True/False se la parola finisce con "rima"
    return stringa[-len(rima):] == rima


def stringa_inizia_con(stringa, parte):
    # restituisce Boolean True/False se la stringa inizia con "parte"
    return stringa[:len(parte)] == parte


def stringa_contiene(stringa, caratteri):
    """
    Per determinare se stringa contiene uno dei caratteri ,;.“”"«»()
    """
    contiene = False
    for c in caratteri:
        if c in stringa:
            contiene = True
    return contiene


def finali_in_comune(parola1, parola2):
    if len(parola2) > len(parola1):
        return finali_in_comune(parola2, parola1)

    # print("comparando", parola1, parola2)
    parte_comune_inversa = ""
    for i in range(-1, -len(parola2) - 1, -1):
        # print("frazione ", i, " ", parola1[i], " ", parola2[i])
        if parola1[i] == parola2[i]:
            parte_comune_inversa += parola1[i]
        else:
            break
    # return "".join(reversed(parte_comune_inversa))
    return parte_comune_inversa[::-1]


def stringa_a_chiave_diz(stringa):
    """
    Trasforma una stringa per usarla come chiave di un dizionario
    """
    stringa = re.sub(r'\W+', '', stringa)
    return stringa


def stringa_a_nome_file(stringa):
    """
    Trasforma una stringa per usarla come chiave di un dizionario
    """
    stringa = stringa.replace(' ', '_')
    stringa = re.sub(r'\W+', '', stringa)
    return stringa


def riconosci_e_decodifica_testo(rawdata):
    import chardet
    diz_encoding_info = chardet.detect(rawdata)
    page_encoding = diz_encoding_info['encoding']
    if diz_encoding_info["confidence"] < 0.8:
        page_encoding = "utf-8"
    return rawdata.decode(page_encoding)
