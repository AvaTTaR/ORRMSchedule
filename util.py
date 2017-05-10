# -*- coding: utf-8 -*-
"""Util module."""
from datetime import timedelta, datetime
from isoweek import Week


class Util:
    """Util class."""

    @staticmethod
    def get_dates_tuple():
        """Return a tuple with tuples of dates."""
        dates = []

        this_week = Week.thisweek()
        # next_week = this_week + 1
        monday = this_week.monday()

        for i in [0, 1, 2, 3, 4, 7, 8, 9, 10, 11]:
            day = monday + timedelta(days=i)
            # dates.append(day.strftime('%Y-%m-%d'))
            dates.append((str(day),))  # adding tuple with date

        return tuple(dates)

    @staticmethod
    def get_dates(param):
        """Return tuple with dates."""
        dates = []

        this_week = Week.thisweek()
        # next_week = this_week + 1
        monday = this_week.monday()

        if param == "this":
            days = [0, 1, 2, 3, 4]
        elif param == "next":
            days = [7, 8, 9, 10, 11]
        elif param == "two":
            days = [0, 1, 2, 3, 4, 7, 8, 9, 10, 11]
        else:
            return "Wrong parameter"

        for i in days:
            day = monday + timedelta(days=i)
            # dates.append(day.strftime('%Y-%m-%d'))
            dates.append(str(day))

        return dates

    @staticmethod
    def get_formatted_dates(param):
        formatted_dates = []
        for date in Util.get_dates(param):
            date_object = datetime.strptime(date, "%Y-%m-%d")
            formatted_dates.append(date_object.strftime("%d.%m"))
        return formatted_dates

    @staticmethod
    def get_this_week():
        """Return list of dates for this week."""
        dates = []

        this_week = Week.thisweek()
        monday = this_week.monday()

        for i in range(5):
            day = monday + timedelta(days=i)
            dates.append(str(day))

        return dates

    @staticmethod
    def format_date(date):
        date_object = datetime.strptime(date, "%Y-%m-%d")
        return date_object.strftime("%d.%m")

    @staticmethod
    def get_dates_for_site(param):
        dates = []
        for day in Util.get_dates(param):
            dates.append({'data': day, 'value': Util.format_date(day)})
        return dates

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
