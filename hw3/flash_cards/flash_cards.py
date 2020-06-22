import json
import random


class FlashCards:
    def __init__(self, path_to_file: str):
        """
        Прочитает пары слов из указанного файла в формате json.
        Создаст все требующиеся атрибуты.
        """
        with open(path_to_file, encoding='utf-8') as f:
            self._dict = json.load(f)
        self._update_words()

    @property
    def words(self):
        """
        Возвращает read-only список слов.
        """
        return self._words

    def _update_words(self):
        """
        Обновляет атрибут со списком слов.
        """
        self._words = tuple(self._dict.keys())

    def play(self) -> str:
        """
        Выдает русские слова из словаря в рандомном порядке,
        сверяет введенный пользователем перевод с правильным
        (регистр введенного слова при этом не важен),
        пока слова в словаре не закончатся.
        Возвращает строку с количеством правильных ответов/общим количеством
        слов в словаре.
        """
        words_to_play = list(self.words)
        if not words_to_play:
            return 'dictionary is empty'
        else:
            score = 0
            while words_to_play:
                question = random.choice(words_to_play)
                print(question)
                if input().lower() == self._dict[question]:
                    score += 1
                words_to_play.remove(question)
            return f'Done! {score} of {len(self._dict)} correct'

    def add_word(self, russian: str, english: str) -> str:
        """
        Добавляет в словарь новую пару слов,
        если русского слова еще нет в словаре.
        Возвращает строку в зависимоти от результата.
        """
        if not isinstance(russian, str) or not isinstance(english, str):
            return 'wrong type of input'
        elif not russian or not english:
            return 'empty input'
        else:
            russian = russian.lower()
            if russian not in self._dict:
                self._dict[russian] = english.lower()
                self._update_words()
                return f'{russian} successfully added'
            else:
                return f'{russian} already in dictionary'

    def delete_word(self, russian: str) -> str:
        """
        Удаляет из словаря введенное русское слово
        и соответсвующее ему английское.
        Возвращает строку в зависимоти от результата.
        """
        if not isinstance(russian, str):
            return 'wrong type of input'
        else:
            russian = russian.lower()
            if russian in self._dict:
                self._dict.pop(russian)
                self._update_words()
                return f'{russian} successfully deleted'
            else:
                return f'{russian} not in dictionary'
