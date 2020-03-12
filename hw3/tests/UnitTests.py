import unittest
from flash_cards import FlashCards

class FlashCardsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = FlashCards('test_json.json')

    def test_add_new_word(self):
        words = set(['яблоко', 'хурма', 'телефон', 'машина'])
        self.app.add_word('машина','car')
        self.assertEqual(words, set(self.app.words))

    def test_add_old_word(self):
        words = set(['яблоко', 'хурма', 'телефон'])
        self.app.add_word('яблоко','apple')
        self.assertEqual(words, set(self.app.words))

    def test_delete_new_word(self):
        words = set(['яблоко', 'хурма', 'телефон'])
        self.app.delete_word('корабль')
        self.assertEqual(words, set(self.app.words))

    def test_delete_old_word(self):
        words = set(['яблоко', 'телефон'])
        self.app.delete_word('хурма')
        self.assertEqual(words, set(self.app.words))

if __name__ == '__main__':
    unittest.main()