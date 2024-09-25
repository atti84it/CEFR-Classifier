import unittest
from cefr_classifier.evaluate_controls import _guess_level_from_file_name

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

if __name__ == '__main__':
    unittest.main()