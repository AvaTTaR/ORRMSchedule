# -*- coding: utf-8 -*-
"""Models for flask."""

from util import Util


class Employee:
    """Employee model."""

    def __init__(self, name_rus, surname_rus):
        """Constructor."""
        self.name_rus = str(name_rus)
        self.surname_rus = str(surname_rus)
        self.name_eng = Util.translit(name_rus)
        self.surname_eng = Util.translit(surname_rus)
        nickname = self.name_eng[0] + self.surname_eng
        self.nickname = nickname.lower()

    def get_nickname(self):
        """Get employee nickname (Jogn Dorian -> jdorian)."""
        return self.nickname

    def get_values(self):
        """Return employee fields."""
        return (self.name_rus, self.surname_rus, self.name_eng,
                self.surname_eng, self.nickname)
