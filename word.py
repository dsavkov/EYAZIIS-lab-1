import pymorphy2

from dict_constants import ANIMACY
from dict_constants import ASPECT
from dict_constants import CASE
from dict_constants import GENDER
from dict_constants import NUMBER
from dict_constants import PART_OF_SPEECH
from dict_constants import PERSON
from dict_constants import TENSE

morph = pymorphy2.MorphAnalyzer()


def build_characteristic_string(key: str, value: str) -> str:
    if value:
        return f'{key}: {value}\n'
    else:
        return ""


class Word:
    def __init__(self, word: str) -> None:
        super().__init__()
        self.word_analyze = morph.parse(word)[0]

    def get_lexeme(self) -> str:
        """
        :return: начальная форму слова
        """
        return self.word_analyze.normal_form

    def get_tense(self) -> str:
        """
        :return: время глагола
        """
        if self.word_analyze.tag.tense is None:
            return ""
        else:
            return TENSE.get(self.word_analyze.tag.tense)

    def get_person(self) -> str:
        """
        :return: лицо глагола
        """
        if self.word_analyze.tag.person is None:
            return ""
        else:
            return PERSON.get(self.word_analyze.tag.person)

    def get_aspect(self) -> str:
        """
        :return: совершенность глагола
        """
        if self.word_analyze.tag.aspect is None:
            return ""
        else:
            return ASPECT.get(self.word_analyze.tag.aspect)

    def get_number(self) -> str:
        """
        :return: число слова
        """
        if self.word_analyze.tag.number is None:
            return ""
        else:
            return NUMBER.get(self.word_analyze.tag.number)

    def get_gender(self) -> str:
        """
        :return: род слова
        """
        if self.word_analyze.tag.gender is None:
            return ""
        else:
            return GENDER.get(self.word_analyze.tag.gender)

    def get_case(self) -> str:
        """
        :return: падеж слова
        """
        if self.word_analyze.tag.case is None:
            return ""
        else:
            return CASE.get(self.word_analyze.tag.case)

    def get_animacy(self) -> str:
        """
        :return: одушевлённость слова
        """
        if self.word_analyze.tag.animacy is None:
            return ""
        else:
            return ANIMACY.get(self.word_analyze.tag.animacy)

    def get_part_of_speech(self) -> str:
        """
        :return: часть речи слова
        """
        return PART_OF_SPEECH.get(self.word_analyze.tag.POS)

    def get_full_characteristics(self) -> str:
        result = ""
        result += build_characteristic_string("Часть речи", self.get_part_of_speech())
        result += build_characteristic_string("Падеж", self.get_case())
        result += build_characteristic_string("Род", self.get_gender())
        result += build_characteristic_string("Число", self.get_number())
        result += build_characteristic_string("Одушевленность", self.get_animacy())
        result += build_characteristic_string("Время", self.get_tense())
        result += build_characteristic_string("Лицо", self.get_person())
        result += build_characteristic_string("Совершенность", self.get_aspect())
        return result
