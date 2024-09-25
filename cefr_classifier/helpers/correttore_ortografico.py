r"""
Fa il controllo ortografico usando pyenchant come base, più alcune migliorie:
- Personal Word List di parole che esistono (tipo custom dictionary)
- lista di Elisioni (espressioni da ignorare tipo: melting pot, content producer, ecc.)
- cache di parole conosciute
- esclude URL tipo www.dominio.it, mentre l'originale esclude solo http://ecc..

Esempio di uso "una parola alla volta con cache": (modo 1, CON CACHE!)
    PERCORSO_PWL = os.path.join("include", "correttore_pwl.txt")
    PERCORSO_ELISIONI = os.path.join("include", "correttore_elisioni.txt")
    co = CorrettoreOrtografico("it_IT", modo=1, percorso_pwl=PERCORSO_PWL, percorso_elisioni=PERCORSO_ELISIONI)

    co.controlla_testo(testo_della_parte, tag=nome_file, ignora_se_inizia_con_maiuscola=True,
                                                 ignora_se_inizia_con_numero=True, filtri="tutti")

Esempio di uso "tutto il testo insieme usando la classe SpellChecker": (modo 2, questo metodo NON usa la cache)
    # tutto uguale, cambia solo modo=2

==== Installazione su Ubuntu Linux ====
sudo apt-get install python3-enchant

==== Per installare altre lingue ====
scaricare da:
    https://github.com/LibreOffice/dictionaries
e copiare in:
    C:\Users\utente\AppData\Local\Programs\Python\Python310\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell

==== Alternative ====
textblob: tante funzioni fichissime, ma solo in inglese
jamspell: fin troppo avanzato, e poi serve quel programma c++, overkill
pyspellchecker: bisognerebbe compilare il dizionario d'italiano
pyenchant: ++ a quanto pare sembra già integrato con i dizionari hunspell/aspell,ecc.
pyhunspell (pip install hunspell  https://github.com/pyhunspell/pyhunspell ): sembra un progetto poco mantenuto
"""

import re
import enchant

from cefr_classifier.utils import files as hf
from cefr_classifier.utils import testi as ht

# TODO
"""
per correggere la maiuscola iniziale (andrea, roma, torino) posso chiedere a Enchant se esiste la variante maiuscola?
cosa succede se do a Enchant una serie di parole dentro .check? qual è lo strumento per testare un testo completo? 
"""


def filtra_testo_regex(testo, filtri=[]):
    """
    Applica i filtri eliminando URLs e indirizzi email dal testo
    """
    nuovo_testo = testo
    for filtro in filtri:
        nuovo_testo = re.sub(filtro, ' ', nuovo_testo, flags=re.IGNORECASE)
    return nuovo_testo


class CorrettoreOrtografico:
    FILTRO_URL = r"(?<=[\s\(])(?:http[s]?:\/\/)?[\w\d_\-]+\.[\w\d_\-.]+\.[\w\d_\-/.]+"
    FILTRO_EMAIL = r"[\w.]+@[^\.].*\.[a-z]{2,}"

    def __init__(self, tag_lingua, modo=1, percorso_pwl="", percorso_elisioni=""):
        """
        tag_lingua = "it_IT"
        """
        self.cache_parole = []
        self.trovate_nella_cache = 0

        if modo == 0:  # modo semplice, solo correttore senza PWL
            # non è stato ancora sperimentato
            self.modo = 0
            self.diz_con_pwl = enchant.Dict(tag_lingua)
            print("caricato in modo 0")

        elif modo == 1:  # una parola alla volta
            self.modo = 1
            self.diz_con_pwl = enchant.DictWithPWL(tag_lingua, percorso_pwl)

        elif modo == 2:  # tutto il testo insieme usando la classe SpellCheck
            self.modo = 2
            from enchant.checker import SpellChecker
            # Non uso più i filtri perché i miei sono migliori:
            #   from enchant.tokenize import EmailFilter, URLFilter
            #   self.checker = SpellChecker(tag_lingua, filters=[EmailFilter, URLFilter])
            self.checker = SpellChecker(tag_lingua)
            self.diz_pwl = enchant.request_pwl_dict(percorso_pwl)
        else:
            print("errore: modo invalido:", modo)

        if percorso_elisioni:
            self._carica_elisioni(percorso_elisioni)
        else:
            self.lista_elisioni = []

    def _carica_elisioni(self, percorso_elisioni):
        print("caricando file elisioni:", percorso_elisioni)
        self.lista_elisioni = hf.leggi_linee_da_file(percorso_elisioni)

    def filtra_testo_elisioni(self, testo):
        """
        Applica elimina tutte le occorrenze delle parole nel file "elisioni"
        """
        # TODO correggere: adesso elimina anche l'interno delle parole
        nuovo_testo = testo
        for espressione in self.lista_elisioni:
            nuovo_testo = nuovo_testo.replace(espressione, ' ')
            # nuovo_testo = re.sub(r"\b" + espressione + r"\b", ' ', testo)
        return nuovo_testo

    def _parola_nella_cache(self, parola):
        return parola in self.cache_parole

    def _aggiungi_parola_alla_cache(self, parola):
        self.cache_parole.append(parola)

    def controlla_parola(self, parola, ignora_se_inizia_con_maiuscola=True, ignora_se_inizia_con_numero=True):
        """
        Ritorna True se:
        - la parola è nella cache
        - la parola è ignorata per una delle ragioni ad esempio se inizia con maiuscola o un numero
        Ritorna False se:
        - la parola non è riconosciuta

        proposta:
        10 se esiste
        5 se è ignorata
        -5 se esiste con maiuscola iniziale (es: torino, roma..)
        -10 se non esiste
        """
        if self._parola_nella_cache(parola):
            self.trovate_nella_cache += 1
            return True

        if ignora_se_inizia_con_maiuscola and re.search(r'[A-Z]', parola[0]):
            return True

        if ignora_se_inizia_con_numero and re.search(r'\d', parola[0]):
            return True

        if self.diz_con_pwl.check(parola):
            self._aggiungi_parola_alla_cache(parola)
            return True
        else:
            return False

    def _controlla_testo_modo_1(self, testo, tag="", ignora_se_inizia_con_maiuscola=True,
                                ignora_se_inizia_con_numero=True, filtri=[]):
        """
        Fa il controllo ortografico UNA PAROLA ALLA VOLTA usando enchant.DictWithPWL,
        viene attivata la cache (!) in modo da non usare Enchant ogni volta
        input:
            tag: fornisci il path del file dove si trova il testo, così se c'è un errore indica qual è il file
        output:
            lista di parole ['tag parola1', 'tag parola2', ...]
        """

        lista_sconosciute = []
        if tag:
            aggiunta_tag = "'" + tag + "' - "
        else:
            aggiunta_tag = ""

        testo = filtra_testo_regex(testo, filtri)

        testo = self.filtra_testo_elisioni(testo)

        for parola in ht.dividi_testo_in_parole(testo):
            valida = self.controlla_parola(parola,
                                           ignora_se_inizia_con_maiuscola=ignora_se_inizia_con_maiuscola,
                                           ignora_se_inizia_con_numero=ignora_se_inizia_con_numero)
            if not valida:
                lista_sconosciute.append(aggiunta_tag + parola)

        return lista_sconosciute

    def _controlla_testo_modo_2(self, testo, tag="", ignora_se_inizia_con_maiuscola=True,
                                ignora_se_inizia_con_numero=True, filtri=[]):
        """
        Fa il controllo ortografico TUTTO IL TESTO INSIEME usando la classe SpellChecker()
        in:
            tag: fornisci il path del file dove si trova il testo, così se c'è un errore indica qual è il file
        out:
            lista di parole ['tag parola1', 'tag parola2', ...]
        """

        lista_sconosciute = []
        if tag:
            aggiunta_tag = "'" + tag + "' - "
        else:
            aggiunta_tag = ""

        testo = filtra_testo_regex(testo, filtri)

        testo = self.filtra_testo_elisioni(testo)

        self.checker.set_text(testo)

        for err in self.checker:
            err = err.word

            if ignora_se_inizia_con_maiuscola and re.search(r'[A-Z]', err[0]):
                continue

            if ignora_se_inizia_con_numero and re.search(r'\d', err[0]):
                continue

            if not self.diz_pwl.check(err):
                lista_sconosciute.append(aggiunta_tag + err)

        return lista_sconosciute

    def controlla_testo(self, testo, tag="", ignora_se_inizia_con_maiuscola=True,
                        ignora_se_inizia_con_numero=True, filtri=[]):
        if filtri == "tutti":
            filtri = [self.FILTRO_EMAIL, self.FILTRO_URL]

        if self.modo == 0 or self.modo == 1:
            return self._controlla_testo_modo_1(testo, tag=tag,
                                                ignora_se_inizia_con_maiuscola=ignora_se_inizia_con_maiuscola,
                                                ignora_se_inizia_con_numero=ignora_se_inizia_con_numero, filtri=filtri)
        elif self.modo == 2:
            return self._controlla_testo_modo_2(testo, tag=tag,
                                                ignora_se_inizia_con_maiuscola=ignora_se_inizia_con_maiuscola,
                                                ignora_se_inizia_con_numero=ignora_se_inizia_con_numero, filtri=filtri)
