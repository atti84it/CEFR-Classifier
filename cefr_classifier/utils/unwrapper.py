import re
import os
from cefr_classifier.helpers.correttore_ortografico import CorrettoreOrtografico

PERCORSO_PWL = os.path.join(os.path.dirname(__file__), "..", "helpers", "correttore_pwl.txt")
PERCORSO_ELISIONI = os.path.join(os.path.dirname(__file__), "..", "helpers", "correttore_elisioni.txt")
co = CorrettoreOrtografico("it_IT", modo=1, percorso_pwl=PERCORSO_PWL, percorso_elisioni=PERCORSO_ELISIONI)


def _linea_finita(linea):
    punteggio = 5  # 0 se non è finita; 10 se finisce con .?!
    if linea[-1:] in ".!?":
        punteggio = 10
    # r"[^a-zA-Z#:\ \dàÈèéìòù<>/,\.'_=\"\n\(\)\[\]\?!’“”…\-\+\;«»–]" usata in Taggatore
    if re.search(r'[\d\w,;:#<>/"\'\(\)\[\]’“”…\-\+«»–°%*]', linea[-1:]):
        punteggio = 0
    if punteggio == 5:
        print("ho un dubbio con:", linea[-10:], "serve un ritorno a capo?")
    return punteggio


def unwrap_testo_punto(testo):
    """
    Unwraps the text by removing the returns if the line does not end with a punctuation mark (.?!)
    Input: text
    """
    linee = testo.split("\n")
    return unwrap_linee_punto(linee)


def unwrap_linee_punto(lista_linee):
    """
    Reconstructs the text by removing the returns if the line does not end with a punctuation mark (.?!)
    Input: array of lines
    """
    finale = ""
    for linea in lista_linee:
        linea = linea.rstrip()
        if _linea_finita(linea) == 0:  # la linea non finisce con un punto
            finale = finale + linea + " "
        else:
            finale = finale + linea + "\n"
    return finale


def unwrap_testo_sillaba_a_capo(testo):
    """
    Unwraps the text by removing the hyphen and the return after it if the next word is a valid word according to the spellchecker.
    """
    pattern = r"([\w]*)-\n([\w]*)"  # individua (frammento1)-\n(frammento2)
    risultati = re.findall(pattern, testo)
    for risultato in risultati:
        parola_riunita = risultato[0] + risultato[1]
        riconosciuta = co.controlla_parola(parola_riunita)
        if risultato[0] != "" and risultato[1] != "" and riconosciuta:
            testo = re.sub(risultato[0] + r'-\n' + risultato[1], parola_riunita, testo)
    return testo


def unwrap_testo(testo):
    """
    Fa entrambi gli unwrap: prima sillaba a capo e poi punto.
    """
    testo = unwrap_testo_sillaba_a_capo(testo)
    testo = unwrap_testo_punto(testo)
    return testo
