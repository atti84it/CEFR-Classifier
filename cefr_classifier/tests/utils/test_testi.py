import unittest
from cefr_classifier.utils.testi import *

class TestTestiFunctions(unittest.TestCase):
    #def setUp(self):
    #    pass

    def test_evidenzia_espressione(self):

        risultato = evidenzia_espressione("inizio passato prossimo fine", "passato prossimo", "strong")
        atteso = "inizio <strong>passato prossimo</strong> fine"
        self.assertEqual(atteso, risultato)

        risultato = evidenzia_espressione("inizio questa parola seguente questa parola ancora questa parola fine",
                                             "questa parola", "b")
        atteso = "inizio <b>questa parola</b> seguente <b>questa parola</b> ancora <b>questa parola</b> fine"
        self.assertEqual(atteso, risultato)

    def test_evidenzia_lista_espressioni(self):

        risultato = evidenzia_lista_espressioni("inizio qui e anche qua e infine qui fine", ["qui", "qua"], "b")
        atteso = "inizio <b>qui</b> e anche <b>qua</b> e infine <b>qui</b> fine"
        self.assertEqual(atteso, risultato)

        testo_base = """per stimolare la produzione e la comprensione scritta e orale fino a  <strong>produzione scritta</strong> e orale per gennaio corrente mese"""
        risultato = evidenzia_lista_espressioni(testo_base,
                                                   ["produzione scritta", "produzione orale", "comprensione scritta",
                                                    "comprensione orale"], "b")
        atteso = "per stimolare la <b>produzione e la <b><b>comprensione scritta</b></b> e orale</b> fino a  <strong><b>produzione scritta</strong> e orale</b> per gennaio corrente mese"
        self.assertEqual(atteso, risultato)

    def test_dividi_testo_in_frasi(self):
        risultato = dividi_testo_in_frasi("Prima frase. Seconda frase. Terza frase? Quarta! Quinta.")
        atteso = ['Prima frase.', 'Seconda frase.', 'Terza frase?', 'Quarta!', 'Quinta.']
        self.assertEqual(atteso, risultato)

        risultato = dividi_testo_in_frasi("Prima frase. Seconda frase? Terza frase…")
        atteso = ['Prima frase.', 'Seconda frase?', 'Terza frase…']
        self.assertEqual(atteso, risultato)

        risultato = dividi_testo_in_frasi("Frase normale. Frase che non finisce con un punto")
        atteso = ['Frase normale.', 'Frase che non finisce con un punto']
        self.assertEqual(atteso, risultato)

        risultato = dividi_testo_in_frasi("Prima frase… Seconda frase. Terza frase? Quarta! Quinta…")
        atteso = ['Prima frase…', 'Seconda frase.', 'Terza frase?', 'Quarta!', 'Quinta…']
        self.assertEqual(atteso, risultato)

        risultato = dividi_testo_in_frasi("""Prima frase
Seconda frase. Terza frase?
Quarta! Quinta…""")
        atteso = ['Prima frase\n', 'Seconda frase.', 'Terza frase?', 'Quarta!', 'Quinta…']
        self.assertEqual(atteso, risultato)

    def test_url_a_nome_file_da_salvare(self):
        risultato = url_a_nome_file_da_salvare("https://www.example.com/pagina.html")
        atteso = "pagina.html"
        self.assertEqual(atteso, risultato)

        risultato = url_a_nome_file_da_salvare("https://www.example.com/pagina.htm")
        atteso = "pagina.htm"
        self.assertEqual(atteso, risultato)

        risultato = url_a_nome_file_da_salvare("https://www.example.com/pagina")
        atteso = "pagina.html"
        self.assertEqual(atteso, risultato)

        risultato = url_a_nome_file_da_salvare("https://www.example.com/pagina/")
        atteso = "pagina.html"
        self.assertEqual(atteso, risultato)

        risultato = url_a_nome_file_da_salvare("https://www.example.com/documento.pdf", ".pdf", ".pdf")
        atteso = "documento.pdf"
        self.assertEqual(atteso, risultato)