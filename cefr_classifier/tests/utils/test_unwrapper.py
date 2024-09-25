import unittest
from cefr_classifier.utils.unwrapper import *


class TestUnwrapperFunctions(unittest.TestCase):
    def test_unwrap_sillaba_a_capo_testo(self):
        testo = """libro di avven-
tura che racconta"""
        atteso = "libro di avventura che racconta"
        risultato = unwrap_testo_sillaba_a_capo(testo)
        self.assertEqual(atteso, risultato)

        testo = """interessi, per-
mette di raggiungere una impresa agri-
cola. Dal"""
        atteso = "interessi, permette di raggiungere una impresa agricola. Dal"
        risultato = unwrap_testo_sillaba_a_capo(testo)
        self.assertEqual(atteso, risultato)

        # Non riunire se c'è uno spazio prima
        testo = """anni - ha continuato Tullio Bernabei -
con alcuni amici"""
        atteso = testo
        risultato = unwrap_testo_sillaba_a_capo(testo)
        self.assertEqual(atteso, risultato)

        # Non riunire se la parola non è nel dizionario
        testo = """interessi, perwwww-
kkkkmette di raggiungere una impresa agri-
cola. Dal"""
        atteso = """interessi, perwwww-
kkkkmette di raggiungere una impresa agricola. Dal"""
        risultato = unwrap_testo_sillaba_a_capo(testo)
        self.assertEqual(atteso, risultato)
