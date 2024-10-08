import os

from .utils import unwrapper as uw
from .utils import print_colors as upc

from . import CEFRClassifier

def _guess_level_from_file_name(file_name: str) -> str:
    """
    Input: any string
    Output: CEFR level uppercas (e.g. "A1"), or exeption if not found. 
    """
    LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
    file_name = file_name.lower()
    for level in LEVELS:
        if file_name.find(level.lower()) != -1:
            return level
    raise Exception("Level not found")

def _distance_between_levels(lev1: str, lev2: str) -> int:
    equivalence_dict = {
        'A1': 1,
        'A2': 2,
        'B1': 3,
        'B2': 4,
        'C1': 5,
        'C2': 6
    }

    num1 = equivalence_dict[lev1]
    num2 = equivalence_dict[lev2]

    return abs(num1-num2)


def evaluate_controls():

    classifier = CEFRClassifier()

    PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

    count_evaluated = 0
    count_right = 0
    count_dist_1_or_less = 0

    cartella_livello = os.path.join(PACKAGE_DIR, "assets", "CEFR_controls")
    nomi_files = os.listdir(
        cartella_livello)  # [:1] ### includere o commentare [:2] per limitare il numero dei files esaminati

    if len(nomi_files) <= 1:
        print(f"Put your texts to be evaluated in the directory {cartella_livello}\nThey have to include the level in the file name, e.g. 'lorem a1 ipsum.txt' will be recognized as A1. It's case insensitive.")
        exit()
    else:
        print(f"Evaluating {len(nomi_files)} files:")

    for nome_file in nomi_files:
        percorso_completo = os.path.join(cartella_livello, nome_file)
        if os.path.isfile(percorso_completo):
            #print("processando:", percorso_completo)
            with open(percorso_completo, "r", encoding='utf-8') as file:
                contenuto = file.read()
                contenuto = uw.unwrap_testo_sillaba_a_capo(contenuto)
                contenuto = uw.unwrap_testo_punto(contenuto)
                contenuto = contenuto.lower()

                level_from_classifier = classifier.classify(contenuto)
                level_from_file_name = _guess_level_from_file_name(nome_file)

                count_evaluated += 1
                if level_from_classifier == level_from_file_name:
                    upc.print_color(level_from_classifier + " " + nome_file, "green")
                    count_right += 1
                else:
                    upc.print_color(level_from_classifier + " " + nome_file, "red")

                if _distance_between_levels(level_from_classifier, level_from_file_name) <= 1:
                    count_dist_1_or_less += 1

                #print(f"il livello è: {result}")

    percent_right = (count_right / count_evaluated) * 100
    print("Exact match rate: ", round(percent_right,2), "%")
    percent_right = (count_dist_1_or_less / count_evaluated) * 100
    print("Rate of guess within a distance of 1 (e.g. file was B1, but detected as B2): ", round(percent_right,2), "%")


if __name__ == "__main__":
    evaluate_controls()