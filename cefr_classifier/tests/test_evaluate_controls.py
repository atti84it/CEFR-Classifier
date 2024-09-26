import unittest
from cefr_classifier.evaluate_controls import _guess_level_from_file_name, _distance_between_levels

class TestGuessLevelFromFileName(unittest.TestCase):
    def test_guess_level_from_file_name(self):
        
        # Test case 1: A2 level
        self.assertEqual(_guess_level_from_file_name("lorem ipsum a2 ciao miao"), "A2")

        # Test case 2: B1 level
        self.assertEqual(_guess_level_from_file_name("B1 miao ciao"), "B1")

        # Test case 3: No level found, should raise an exception
        with self.assertRaises(Exception) as context:
            _guess_level_from_file_name("ciao miao lorem")
        self.assertEqual(str(context.exception), "Level not found")


class TestDistanceBetweenLevels(unittest.TestCase):
    def test_distance_between_levels(self):
        # Test cases with expected results
        test_cases = [
            ('A1', 'A2', 1),
            ('A1', 'B1', 2),
            ('A1', 'C2', 5),
            ('B2', 'C1', 1), #
            ('C1', 'B2', 1), #
            ('C1', 'A2', 3),
            ('C2', 'C2', 0),
        ]

        for lev1, lev2, expected in test_cases:
            with self.subTest(f"{lev1} to {lev2}"):
                result = _distance_between_levels(lev1, lev2)
                self.assertEqual(result, expected)

    def test_invalid_input(self):
        # Test with invalid input
        with self.assertRaises(KeyError):
            _distance_between_levels('A0', 'B1')
        
        with self.assertRaises(KeyError):
            _distance_between_levels('A1', 'D1')

if __name__ == '__main__':
    unittest.main()