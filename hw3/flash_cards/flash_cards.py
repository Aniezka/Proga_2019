import json
from random import shuffle


class FlashCards(object):
    def __init__(self, path_to_file: str):
        '''
        Прочитает пары слов из указанного файла в формате json.
        Создаст все требующиеся атрибуты.
        '''

        self._r2e = dict()
        self._e2r = dict()
        self._words_set = set()
        self.words = []

        with open(path_to_file, encoding='utf-8') as data_file:
            data_json = json.load(data_file)

        for k in data_json:
            self._r2e[k] = data_json[k]
            self._e2r[data_json[k]] = k
            self._words_set.add(k)

        self._update_words()

    def _update_words(self):
        self.words = [i for i in self._words_set]

    def play(self) -> str:
        '''
        Выдает русские слова из словаря в рандомном порядке,
        сверяет введенный пользователем перевод с правильным
        (регистр введенного слова при этом не важен),
        пока слова в словаре не закончатся.
        Возвращает строку с количеством правильных ответов/общим количеством
        слов в словаре (см пример работы).
        '''

        count = 0
        arr = [i for i in self._words_set]
        shuffle(arr)
        for elem in arr:
            print(elem)
            answer = input()
            count += self._r2e[elem] == answer
        return "Done! {0} of {1} words correct.".format(count, len(arr))

    def add_word(self, russian: str, english: str) -> str:
        '''
        Добавляет в словарь новую пару слов,
        если русского слова еще нет в словаре.
        Возвращает строку в зависимоти от результата (см пример работы).
        '''
        if not (type(russian) is str) or not (type(english) is str):
            return

        if self._r2e.get(russian) is None:
            self._e2r[english] = russian
            self._r2e[russian] = english
            self._words_set.add(russian)
            self._update_words()
            return "Succesfully added word '{0}''.".format(russian)
        return "'{0}' already in dictionary.".format(russian)

    def delete_word(self, russian: str) -> str:
        '''
        Удаляет из словаря введенное русское слово
        и соответсвующее ему английское.
        Возвращает строку в зависимоти от результата (см пример работы).
        '''

        if not (type(russian) is str):
            return

        if russian in self._words_set:
            self._e2r.pop(self._r2e[russian])
            self._r2e.pop(russian)
            self._words_set.remove(russian)
            self._update_words()
            return "Succesfully deleted word '{0}''.".format(russian)
        return "'{0}' not in dictionary.".format(russian)

fc = FlashCards("test_json.json")