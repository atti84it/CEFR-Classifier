import os, csv

from .utils import testi as ht
from .utils import liste as hl
from .utils import dizionari as hd

class CEFRClassifier:
    def __init__(self):
        
        LIVELLI = ("A1", "A2", "B1", "B2", "C1", "C2")
        PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
        PERCORSO_POPOLARITA_RIME_U6 = os.path.join(PACKAGE_DIR, "assets", "CEFR_weights", "rime.csv")
        separatore = ","
        self.popolarita_rime_U6 = {}

        with open(PERCORSO_POPOLARITA_RIME_U6) as file:
            csvReader = csv.reader(file, delimiter=separatore)

            for row in csvReader:
                rima = row[0]
                popolarita_rima = {}
                for i in range(0, 6):
                    livello = LIVELLI[i]
                    if row[i + 1] != "":
                        valore = float(row[i + 1])
                    else:
                        valore = float(0)
                    popolarita_rima[livello] = valore
                self.popolarita_rime_U6[rima] = popolarita_rima


    def _moltiplica_delta(self, dizionario, moltiplicatore):
        nuovo_diz = {}
        for chiave in dizionario.keys():
            nuovo_diz[chiave] = dizionario[chiave] * moltiplicatore
        return nuovo_diz


    def _normalizza_delta(self, dizionario):
        # moltiplica i delta in modo che la somma sia = 1
        somma = 0
        for chiave in dizionario.keys():
            somma += dizionario[chiave]
        moltiplicatore = 1 / somma
        return self._moltiplica_delta(dizionario, moltiplicatore)
    
    def classify_dict(self, contenuto):
        probabilita_parole = {}

        parole_file = ht.dividi_testo_in_parole(contenuto)
        parole_file = hl.pulisci_lista_parole(parole_file)

        frequenze_parole_file = hl.conta_frequenze_di_una_lista(parole_file)
        #print("Nel file ci sono", len(parole_file), "parole totali, di cui", len(frequenze_parole_file), "uniche")


        # per ogni parola in dizionario di frequenza:
        for parola in frequenze_parole_file:
            rime_con_cui_rima_questa_parola = []
            # per ogni rima in lista rime:
            for rima in self.popolarita_rime_U6.keys():
                # se la parola fa rima:
                if ht.stringa_finisce_con(parola, rima):
                    rime_con_cui_rima_questa_parola += [rima]
                    # print("associazione parola-rima",parola,rima)

            # tra le rime con cui rima questa parola scegli la più lunga
            rima_piu_lunga = hl.parola_piu_lunga_di_una_lista(rime_con_cui_rima_questa_parola)
            # print("rima piu lunga", parola, rima_piu_lunga)

            deltas = self.popolarita_rime_U6[rima_piu_lunga]  # le popolarità della rima in ogni livello
            deltas = self._normalizza_delta(deltas)
            moltiplicatore = frequenze_parole_file[parola]  # se la parola appare n volte, le popolarità vanno moltiplicate
            deltas_moltiplicati = self._moltiplica_delta(deltas, moltiplicatore)

            probabilita_parole[parola] = deltas_moltiplicati

        # print(probabilita_parole)
        probabilita_livelli = {}

        for parola in probabilita_parole.keys():
            for livello in probabilita_parole[parola].keys():
                if livello in probabilita_livelli:
                    probabilita_livelli[livello] += probabilita_parole[parola][livello]
                else:
                    probabilita_livelli[livello] = probabilita_parole[parola][livello]

        return hd.ordina_dizionario_per_frequenza(probabilita_livelli)
    
    def classify(self, contenuto):
        #return hd.porzione_diz(self.classify_dict(contenuto), 1).keys()
        return next(iter(self.classify_dict(contenuto)))