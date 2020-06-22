import unittest
from flash_cards.flash_cards import FlashCards
from unittest.mock import patch
from parameterized import parameterized


class FlashCardsTestPlay(unittest.TestCase):

    def setUp(self):
        self.fc = FlashCards('flash_cards/dict.json')

    def test_play_0correct(self):
        with patch('builtins.input', return_value='wrong'):
            self.assertEqual(self.fc.play(), 'Done! 0 of 2 correct')

    @parameterized.expand([
        'apple',
        'AppLe'
    ])
    def test_play_1correct(self, answer):
        with patch('builtins.input', return_value=answer):
            self.assertEqual(self.fc.play(), 'Done! 1 of 2 correct')

    @parameterized.expand([
        (['apple', 'persimmon'],),
        (['aPPle', 'persiMMon'],),
    ])
    def test_play_2correct(self, answer):
        with patch('random.choice', side_effect=['яблоко', 'хурма']):
            with patch('builtins.input', side_effect=answer):
                self.assertEqual(self.fc.play(), 'Done! 2 of 2 correct')

    def test_play_same_question_does_not_work(self):
        with patch('random.choice', return_value='яблоко'):
            with patch('builtins.input', side_effect=['apple', 'persimmon']):
                with self.assertRaises(ValueError):
                    self.fc.play()


if __name__ == '__main__':
    unittest.main()
