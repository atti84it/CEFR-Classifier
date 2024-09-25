import os, csv
from .utils import liste as hl
from .utils import testi as ht
from .utils import files as hf
from .utils import dizionari as hd
from .utils import unwrapper as uw

def crea_lista_rime():
    LIVELLI = ("A1", "A2", "B1", "B2", "C1", "C2")
    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
    PERCORSO_GRAFICO_RIME = os.path.join(PACKAGE_DIR, "assets", "CEFR_weights", "grafico_rime.csv")
    PERCORSO_RIME_MINI = os.path.join(PACKAGE_DIR, "assets", "CEFR_weights", "rime_mini.txt")

    parole_U6 = []

    for livello in LIVELLI:
        parole_uniche_livello = []
        cartella_livello = os.path.join(PACKAGE_DIR, "assets", "CEFR_corpus_files", livello)
        nomi_files = os.listdir(cartella_livello)#[:1] ### includere o commentare [:2] per limitare il numero dei files esaminati
        for nome_file in nomi_files:
            percorso_completo = os.path.join(cartella_livello, nome_file)
            if os.path.isfile(percorso_completo):
                # print("processando:", percorso_completo)
                with open(percorso_completo, "r", encoding='utf-8') as file:
                    contenuto = file.read()
                    contenuto = uw.unwrap_testo_sillaba_a_capo(contenuto)
                    contenuto = uw.unwrap_testo_punto(contenuto)
                    contenuto = contenuto.lower()
                    parole = ht.dividi_testo_in_parole(contenuto)
                    parole = hl.pulisci_lista_parole(parole)
                    # print("trovate n parole:", len(parole))
                    parole_uniche_file = hl.elementi_unici_della_lista(parole)
                    # print("di cui uniche:", len(parole_uniche_file))
                    parole_uniche_livello += parole_uniche_file
        parole_uniche_livello = hl.elementi_unici_della_lista(parole_uniche_livello)
        print("il livello", livello, "ha", len(parole_uniche_livello), "parole uniche")
        parole_U6 += parole_uniche_livello

    parole_U6 = hl.elementi_unici_della_lista(parole_U6)
    n_uniche = len(parole_U6)
    print(f"*** in U6 ci sono {n_uniche} parole uniche ***")

    stima_disp_uniche = int((n_uniche * (n_uniche-1)) / 2)
    stima_disp_uniche_str = '{:,}'.format(stima_disp_uniche)
    print(f"mmm.. ci vorrà un po' per elaborare {stima_disp_uniche_str} disposizioni uniche...")

    frazione_percento = int(stima_disp_uniche / 100) # normalmente stampa l'aggiornamento ogni 1%, ma si può cambiare

    rime = []
    n_disposizioni_elaborate = 0
    grafico = []
    for disposizione in hl.disposizioni_uniche_iter(parole_U6):
        n_disposizioni_elaborate += 1
        if n_disposizioni_elaborate % frazione_percento == 0:
            percentuale_elaborata = int(n_disposizioni_elaborate * 100 / stima_disp_uniche)
            print(percentuale_elaborata, "% ; elaborate", '{:,}'.format(n_disposizioni_elaborate), "disposizioni, trovate", len(rime), "rime")
            grafico.append(str(n_disposizioni_elaborate) + ',' + str(len(rime)) + '\n')

        finali = ht.finali_in_comune(disposizione[0], disposizione[1])
        if finali == "":
            continue
        if finali not in rime:
            rime += [finali]

    print("q.tà rime", len(rime))

    with open(PERCORSO_GRAFICO_RIME, "w", encoding='utf-8') as file:
        file.write('disposizioni_elaborate,rime\n')
        file.writelines(grafico)

    with open(PERCORSO_RIME_MINI, "w", encoding='utf-8') as file:
        for rima in rime:
            file.write(rima + "\n")


def valuta_probabilita_rime():
    LIVELLI = ("A1", "A2", "B1", "B2", "C1", "C2")
    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
    PERCORSO_RIME_MINI = os.path.join(PACKAGE_DIR, "assets", "CEFR_weights", "rime_mini.txt")
    PERCORSO_POPOLARITA_RIME_U6 = os.path.join(PACKAGE_DIR, "assets", "CEFR_weights", "rime.csv")

    popolarita_rime_U6 = {}

    lista_rime = hf.leggi_linee_da_file(PERCORSO_RIME_MINI)
    print("caricate n rime", len(lista_rime))

    for livello in LIVELLI:

        #crea lista di parole in questo livello
        parole_livello = []
        
        cartella_livello = os.path.join(PACKAGE_DIR, "assets", "CEFR_corpus_files", livello)
        nomi_files = os.listdir(cartella_livello)#[:1]  ### includere o commentare [:2] per limitare il numero dei files esaminati

        for nome_file in nomi_files:
            percorso_completo = os.path.join(cartella_livello, nome_file)
            print("processando:", percorso_completo)
            contenuto = hf.carica_e_unwrap_testo(percorso_completo)
            contenuto = contenuto.lower()
            parole_file = ht.dividi_testo_in_parole(contenuto)
            parole_file = hl.pulisci_lista_parole(parole_file)
            parole_livello += parole_file

        n_parole_livello = len(parole_livello)

        # crea frequenza_lista_parole_in_questo_livello
        frequenze_parole_livello = hl.conta_frequenze_di_una_lista(parole_livello)
        print("\nNel livello", livello, "ci sono", n_parole_livello, "parole totali, di cui", len(frequenze_parole_livello), "uniche\n")

        frequenze_rime_livello = {}

        # Scopre la rima migliore di ogni parola del livello.
        # per ogni parola in dizionario di frequenza:
        for parola in frequenze_parole_livello:
            rime_con_cui_rima_questa_parola = []
            # per ogni rima in lista rime:
            for rima in lista_rime:
                # se la parola fa rima:
                if ht.stringa_finisce_con(parola, rima):
                    # mette la rima nella lista delle rime, poi sceglierà la più lunga
                    rime_con_cui_rima_questa_parola += [rima]

            # Sceglie la più lunga tra le rime con cui rima questa parola
            rima_piu_lunga = hl.parola_piu_lunga_di_una_lista(rime_con_cui_rima_questa_parola)
            # print("rima piu lunga", parola, rima_piu_lunga)

            # Aggiorna la popolarità della rima in questo livello.
            # Per ogni parola si somma un po' alla rima corrispondente
            # frequenze_rime_livello = {'o': 10000, 'zione': 30, ...}
            if rima_piu_lunga in frequenze_rime_livello:
                frequenze_rime_livello[rima_piu_lunga] += frequenze_parole_livello[parola]
            else:
                frequenze_rime_livello[rima_piu_lunga] = frequenze_parole_livello[parola]

        # per ogni rima che appare nel livello:
        for rima in frequenze_rime_livello:
            freq_assoluta = frequenze_rime_livello[rima]
            freq_relativa = freq_assoluta / n_parole_livello

            # Inserisce all'interno del dizionario maggiore il valore della freq_relativa corrispondente al livello corrente
            # cioè: alla riga 'rima', alla colonna 'livello', inserisci freq_relativa
            # popolarita_rime_U6 = {'o': {'A1': 0.10, 'A2': 0.08}, 'zione': {...} }
            hd.aggiunge_diz_a_diz(popolarita_rime_U6, rima, {livello: freq_relativa})
        if "zione" in popolarita_rime_U6:
            print(popolarita_rime_U6["zione"])
            
    separatore = ","
    print("scrivendo:", PERCORSO_POPOLARITA_RIME_U6)
    with open(PERCORSO_POPOLARITA_RIME_U6, "w", newline='') as file:
        writer = csv.writer(file, delimiter=separatore)
        
        for rima in popolarita_rime_U6.keys():
            linea = [rima]
            for livello in LIVELLI:
                if livello in popolarita_rime_U6[rima]:
                    valore = popolarita_rime_U6[rima][livello]
                else:
                    valore = ""
                linea.append(valore)
            # print("linea:", linea)
            writer.writerow(linea)


def train():
    print("Training...")

    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

    # If you already have a pre-trained weights file, it will not run the training
    PERCORSO_POPOLARITA_RIME_U6 = os.path.join(PACKAGE_DIR, "assets", "CEFR_weights", "rime.csv")
    if os.path.exists(PERCORSO_POPOLARITA_RIME_U6):
        print(f"Weights file already existing!!! The training will be interrupted.\nIf you want to run the training, delete the file '{PERCORSO_POPOLARITA_RIME_U6}'")
        exit()

    # If you already have the intermediate file, it will skip the first phase -that creates it- and go straight to phase 2
    PERCORSO_RIME_MINI = os.path.join(PACKAGE_DIR, "assets", "CEFR_weights", "rime_mini.txt")
    if os.path.exists(PERCORSO_RIME_MINI):
        print(f"File {PERCORSO_RIME_MINI} found -> Skipping phase 1.\nIf you want to run phase 1, delete 'rime_mini.txt' file.")
        import time
        time.sleep(5)
    else:
        print("Starting phase 1...")
        crea_lista_rime()

    print("Starting phase 2...")
    valuta_probabilita_rime()


if __name__ == "__main__":
    train()