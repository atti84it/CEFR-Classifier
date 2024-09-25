import unittest
from cefr_classifier.utils.liste import disposizioni_uniche_iter, disposizioni_uniche_con_distanza_iter, similitudine_liste

class TestListeFunctions(unittest.TestCase):

    def test_disposizioni_uniche_iter(self):
        # Create da me:
        lista = [1, 2, 3, 4]
        atteso = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        risultato = []
        for una_disp in disposizioni_uniche_iter(lista):
            risultato.append(una_disp)
        self.assertEqual(atteso, risultato)

        n = 400
        atteso = (n * (n - 1)) / 2
        conteggio = 0
        for _ in disposizioni_uniche_iter(range(n)):
            conteggio += 1
        self.assertEqual(atteso, conteggio)        

        # Creata da Claude:
        lista = ['a', 'b', 'c']
        expected = [('a', 'b'), ('a', 'c'), ('b', 'c')]
        result = list(disposizioni_uniche_iter(lista))
        self.assertEqual(result, expected)

    def test_disposizioni_uniche_con_distanza_iter(self):
        # Create da me:
        lista = [1, 2, 3, 4]
        atteso = [(1, 2, 1), (1, 3, 2), (1, 4, 3), (2, 3, 1), (2, 4, 2), (3, 4, 1)]
        risultato = []
        for una_disp in disposizioni_uniche_con_distanza_iter(lista):
            risultato.append(una_disp)
        self.assertEqual(atteso, risultato)

        atteso = [(1, 1, 0),  # identici con distanza 0
                  (1, 2, 1),
                  (1, 3, 2),
                  (1, 4, 3),
                  (2, 2, 0),  # identici con distanza 0
                  (2, 3, 1),
                  (2, 4, 2),
                  (3, 3, 0),  # identici con distanza 0
                  (3, 4, 1),
                  (4, 4, 0)]  # identici con distanza 0
        risultato = []
        for una_disp in disposizioni_uniche_con_distanza_iter(lista, includi_identici=True):
            risultato.append(una_disp)
        self.assertEqual(atteso, risultato)        

        # Creata da Claude:
        lista = ['a', 'b', 'c']
        expected = [('a', 'b', 1), ('a', 'c', 2), ('b', 'c', 1)]
        result = list(disposizioni_uniche_con_distanza_iter(lista))
        self.assertEqual(result, expected)

        expected_with_identical = [('a', 'a', 0), ('a', 'b', 1), ('a', 'c', 2), ('b', 'b', 0), ('b', 'c', 1), ('c', 'c', 0)]
        result_with_identical = list(disposizioni_uniche_con_distanza_iter(lista, includi_identici=True))
        self.assertEqual(result_with_identical, expected_with_identical)

    def test_similitudine_liste(self):
        # Creata da me:
        l1 = 'a b c d'.split(' ')
        l2 = l1
        atteso = 1.0
        risultato = similitudine_liste(l1, l2)
        self.assertEqual(atteso, risultato)

        l1 = 'a b c d'.split(' ')
        l2 = 'a b x y'.split(' ')
        atteso = 0.5
        risultato = similitudine_liste(l1, l2)
        self.assertEqual(atteso, risultato)

        l1 = 'a b b'.split(' ')
        l2 = 'a b c'.split(' ')
        atteso = 0.666
        risultato = similitudine_liste(l1, l2)
        self.assertAlmostEqual(atteso, risultato, delta=0.001)

        l1 = 'a b c d a b c a b a'.split(' ')
        l2 = 'a a b c x x x x x x'.split(' ')
        atteso = 0.4
        risultato = similitudine_liste(l1, l2)
        self.assertAlmostEqual(atteso, risultato, delta=0.001)

        l1 = 'a b c d a b c a b a'.split(' ')
        l2 = 'x y z x y x'.split(' ')
        atteso = 0
        risultato = similitudine_liste(l1, l2)
        self.assertAlmostEqual(atteso, risultato, delta=0.001)

        # Creata da Claude:
        l1 = ['a', 'b', 'a', 'c']
        l2 = ['a', 'a', 'b', 'd']
        expected = 0.75
        result = similitudine_liste(l1, l2)
        self.assertAlmostEqual(result, expected)

if __name__ == '__main__':
    unittest.main()