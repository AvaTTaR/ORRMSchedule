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
        shortname = self.name_eng[0] + self.surname_eng
        self.shortname = shortname.lower()

    def get_shortname(self):
        """Get employee nickname (John Dorian -> jdorian)."""
        return self.shortname

    def get_values(self):
        """Return employee fields."""
        return (self.name_rus, self.surname_rus, self.name_eng,
                self.surname_eng, self.shortname)
