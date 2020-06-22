import unittest
from flash_cards.flash_cards import FlashCards
from parameterized import parameterized


class FlashCardsTestAddword(unittest.TestCase):

    def setUp(self):
        self.fc = FlashCards('flash_cards/dict.json')

    @parameterized.expand([
        ('wrong type of input', 123, 'english'),
        ('wrong type of input', 'russian', 123),
        ('wrong type of input', 123, 123),
        ('wrong type of input', None, 'english'),
        ('wrong type of input', 'russian', ['english'])
    ])
    def test_add_word_wrong_input(self, output, russian, english):
        self.assertEqual(output,
                         self.fc.add_word(russian, english))

    @parameterized.expand([
        ('empty input', '', 'english'),
        ('empty input', 'russian', ''),
        ('empty input', '', '')
    ])
    def test_add_word_empty_input(self, output, russian, english):
        self.assertEqual(output,
                         self.fc.add_word(russian, english))

    @parameterized.expand([
        ('хурма already in dictionary', 'хурма', 'english'),
        ('яблоко already in dictionary', 'ЯблОко', 'english'),
    ])
    def test_add_word_already_exist(self, output, russian, english):
        self.assertEqual(output,
                         self.fc.add_word(russian, english))

    @parameterized.expand([
        ('russian successfully added', 'russian', 'english'),
        ('russian successfully added', 'RussIan', 'apple'),
    ])
    def test_add_word_everything_fine(self, output, russian, english):
        self.assertEqual(output,
                         self.fc.add_word(russian, english))

    @parameterized.expand([
        (('хурма', 'яблоко', 'russian'), 'russian', 'english'),
        (('хурма', 'яблоко', 'russian'), 'ruSSian', 'english')
    ])
    def test_add_word_added_to_words(self, words, russian, english):
        self.fc.add_word(russian, english)
        self.assertEqual(sorted(words),
                         sorted(self.fc.words))

    @parameterized.expand([
        ({'хурма': 'persimmon', 'яблоко': 'apple', 'russian': 'english'},
         'russian', 'english'),
        ({'хурма': 'persimmon', 'яблоко': 'apple', 'russian': 'english'},
         'russian', 'english')
    ])
    def test_add_word_added_to_dict(self, dictionary, russian, english):
        self.fc.add_word(russian, english)
        self.assertEqual(sorted(dictionary),
                         sorted(self.fc._dict))


if __name__ == '__main__':
    unittest.main()
