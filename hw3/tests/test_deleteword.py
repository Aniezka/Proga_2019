import unittest
from flash_cards.flash_cards import FlashCards
from parameterized import parameterized


class FlashCardsTestDelword(unittest.TestCase):

    def setUp(self):
        self.fc = FlashCards('flash_cards/dict.json')

    @parameterized.expand([
        ('wrong type of input', 123),
        ('wrong type of input', None),
        ('wrong type of input', ['russian'])
    ])
    def test_del_word_wrong_input(self, output, russian):
        self.assertEqual(output,
                         self.fc.delete_word(russian))

    @parameterized.expand([
        ('russian not in dictionary', 'russian'),
        (' not in dictionary', ''),
        ('russian not in dictionary', 'RuSSian')
    ])
    def test_del_word_not_in_dict(self, output, russian):
        self.assertEqual(output,
                         self.fc.delete_word(russian))

    @parameterized.expand([
        ('хурма successfully deleted', 'хурма'),
        ('хурма successfully deleted', 'хУРма')
    ])
    def test_del_word_everything_fine(self, output, russian):
        self.assertEqual(output,
                         self.fc.delete_word(russian))

    @parameterized.expand([
        (('хурма',), 'яблоко'),
        (('хурма',), 'ябЛОко')
    ])
    def test_add_word_deleted_from_words(self, words, russian):
        self.fc.delete_word(russian)
        self.assertEqual(words,
                         self.fc.words)

    @parameterized.expand([
        ({'хурма': 'persimmon'}, 'яблоко'),
        ({'хурма': 'persimmon'}, 'ябЛОко')
    ])
    def test_add_word_deleted_from_dict(self, dictionary, russian):
        self.fc.delete_word(russian)
        self.assertEqual(dictionary,
                         self.fc._dict)


if __name__ == '__main__':
    unittest.main()
