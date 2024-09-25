r"""
This script opens the files in assets/CEFR_corpus_dirty_files, extracts the texts from each file, and writes clean parts to assets/CEFR_corpus_files.
It also performs some basic unwrapping of the text (e.g. it removes the hyphen and the return after it if the next word is a valid word according to the spellchecker).
"Dirty files" means that one file is made of multiple parts, and each part is separated by 3 returns (i.e. "\n\n\n").
It also writes the unknown words (words that are not recognized by the spellchecker, e.g. foreign words) in the file "assets/CEFR_weights/parole_sconosciute.txt".
"""
import os
import shutil  # per cancellare una cartella non-vuota

from .utils import unwrapper as uw
from .utils import liste as hl
from .helpers.correttore_ortografico import CorrettoreOrtografico

def clean_corpus_files():
    print("Cleaning...")
    LIVELLI = ("A1", "A2", "B1", "B2", "C1", "C2")
    SCRIVI_FILES_PULITI = True # True: will write clean corpus files in the folder CEFR_corpus_files; False: will only elaborate "parole_sconosciute.txt" (= unknown words, e.g. foreign words)
    
    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
    PERCORSO_PWL = os.path.join(PACKAGE_DIR, "helpers", "correttore_pwl.txt")
    PERCORSO_ELISIONI = os.path.join(PACKAGE_DIR, "helpers", "correttore_elisioni.txt")
    PERCORSO_PAROLE_SCONOSCIUTE = os.path.join(PACKAGE_DIR, "assets", "CEFR_weights", "parole_sconosciute.txt")

    parole_sconosciute = []
    co = CorrettoreOrtografico("it_IT", modo=1, percorso_pwl=PERCORSO_PWL, percorso_elisioni=PERCORSO_ELISIONI)

    for livello in LIVELLI:
        cartella_livello = os.path.join(PACKAGE_DIR, "assets", "CEFR_corpus_dirty_files", livello)
        cartella_livello_pulito = os.path.join(PACKAGE_DIR, "assets", "CEFR_corpus_files", livello)

        if os.path.exists(cartella_livello_pulito):
            shutil.rmtree(cartella_livello_pulito)

        # includere o commentare [:2] per limitare il numero dei files esaminati
        nomi_files = os.listdir(cartella_livello)#[:2]
        for nome_file in nomi_files:
            percorso_completo = os.path.join(cartella_livello, nome_file)
            if os.path.isfile(percorso_completo):
                print("processando:", percorso_completo)
                with open(percorso_completo, "r", encoding='utf-8') as file:
                    contenuto = file.read()

                if "\n\n\n" in contenuto:
                    if "\n\n\n\n" not in contenuto:
                        print("SUS: solo 3returns")
                parti = contenuto.split("\n\n\n\n")

                for i in range(len(parti)):
                    testo_della_parte = parti[i].strip()

                    testo_della_parte = uw.unwrap_testo_sillaba_a_capo(testo_della_parte)
                    testo_della_parte = uw.unwrap_testo_punto(testo_della_parte)

                    sconosciute = co.controlla_testo(testo_della_parte, tag=nome_file, ignora_se_inizia_con_maiuscola=True,
                                                    ignora_se_inizia_con_numero=True, filtri="tutti")
                    parole_sconosciute.extend(sconosciute)

                    if SCRIVI_FILES_PULITI:
                        os.makedirs(cartella_livello_pulito, exist_ok=True)  # equivalente a mkdir

                        file_senza_estensione = os.path.splitext(nome_file)[0]
                        percorso_file_pulito = os.path.join(cartella_livello_pulito,
                                                            file_senza_estensione + "_part" + str(i + 1) + ".txt")
                        with open(percorso_file_pulito, "w", encoding="utf-8") as file:
                            file.write(testo_della_parte)

    parole_sconosciute = hl.elementi_unici_della_lista(parole_sconosciute)
    parole_sconosciute.sort()

    print("Scrivendo:", PERCORSO_PAROLE_SCONOSCIUTE)
    with open(PERCORSO_PAROLE_SCONOSCIUTE, "w", encoding="utf-8") as file:
        out = "\n".join(parole_sconosciute)
        file.write(out)

    print(co.trovate_nella_cache, "volte ho recuperato una parola dalla cache")    

if __name__ == "__main__":
    clean_corpus_files()