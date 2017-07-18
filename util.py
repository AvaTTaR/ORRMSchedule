# -*- coding: utf-8 -*-
from datetime import datetime

import re
from isoweek import Week


class Util:
    @staticmethod
    def get_day_by_date(date):
        return datetime.strptime(date, "%Y-%m-%d").strftime('%A').lower()

    @staticmethod
    def get_ordinary_week(iso_week):
        week = {
            'monday': Week.fromstring(iso_week).monday().isoformat(),
            'tuesday': Week.fromstring(iso_week).tuesday().isoformat(),
            'wednesday': Week.fromstring(iso_week).wednesday().isoformat(),
            'thursday': Week.fromstring(iso_week).thursday().isoformat(),
            'friday': Week.fromstring(iso_week).friday().isoformat()
        }
        return week

    @staticmethod
    def iso_week_to_date(iso_week):  # iso_week in format 2017-W28-4
        year = iso_week[:4]
        week = iso_week[6: 8]
        day = iso_week[9]
        #  Week.day(0-6)
        return Week(int(year), int(week)).day(int(day)-1)

    @staticmethod
    def is_valid_employee(name_rus, surname_rus):
        name = re.search(r'^[А-ЯЁ][а-яё]+$', name_rus)
        surname = re.search(r'^[А-ЯЁ][а-яё]+$', surname_rus)
        if name is None or surname is None:
            return False
        return True

    @staticmethod
    def translit(string):
        """Return the name and surname in translit."""
        capital_letters = {
            u'А': u'A',
            u'Б': u'B',
            u'В': u'V',
            u'Г': u'G',
            u'Д': u'D',
            u'Е': u'E',
            u'Ё': u'Yo',
            u'Ж': u'Zh',
            u'З': u'Z',
            u'И': u'I',
            u'Й': u'Y',
            u'К': u'K',
            u'Л': u'L',
            u'М': u'M',
            u'Н': u'N',
            u'О': u'O',
            u'П': u'P',
            u'Р': u'R',
            u'С': u'S',
            u'Т': u'T',
            u'У': u'U',
            u'Ф': u'F',
            u'Х': u'H',
            u'Ц': u'Ts',
            u'Ч': u'Ch',
            u'Ш': u'Sh',
            u'Щ': u'Sch',
            u'Ъ': u'',
            u'Ы': u'Y',
            u'Ь': u'',
            u'Э': u'E',
            u'Ю': u'Yu',
            u'Я': u'Ya'
        }

        lower_case_letters = {
            u'а': u'a',
            u'б': u'b',
            u'в': u'v',
            u'г': u'g',
            u'д': u'd',
            u'е': u'e',
            u'ё': u'yo',
            u'ж': u'zh',
            u'з': u'z',
            u'и': u'i',
            u'й': u'y',
            u'к': u'k',
            u'л': u'l',
            u'м': u'm',
            u'н': u'n',
            u'о': u'o',
            u'п': u'p',
            u'р': u'r',
            u'с': u's',
            u'т': u't',
            u'у': u'u',
            u'ф': u'f',
            u'х': u'h',
            u'ц': u'ts',
            u'ч': u'ch',
            u'ш': u'sh',
            u'щ': u'sch',
            u'ъ': u'',
            u'ы': u'y',
            u'ь': u'',
            u'э': u'e',
            u'ю': u'yu',
            u'я': u'ya'
        }

        translit_string = ""

        for index, char in enumerate(string):
            if char in lower_case_letters.keys():
                char = lower_case_letters[char]
            elif char in capital_letters.keys():
                char = capital_letters[char]
                if len(string) > index + 1:
                    if string[index + 1] not in lower_case_letters.keys():
                        char = char.upper()
                else:
                    char = char.upper()
            translit_string += char

        return translit_string

Util.iso_week_to_date("2017-W28-4")
