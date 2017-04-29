# -*- coding: utf-8 -*-
"""Database module."""

import os
import sqlite3

from models import Employee
from util import Util

database_url = '{}{}'.format(os.path.dirname(os.path.realpath(__file__)),
                             '/database.db')


def init_db():
    """Database initialization."""
    if os.path.exists(database_url):
        os.remove(database_url)
    conn = sqlite3.connect(database_url)
    conn.execute('''CREATE TABLE employee (
                 id INTEGER NOT NULL,
                 name_rus VARCHAR(15),
                 surname_rus VARCHAR(15),
                 name_eng VARCHAR(15),
                 surname_eng VARCHAR(15),
                 nickname VARCHAR(15),
                 PRIMARY KEY(id));''')
    conn.execute('''CREATE TABLE schedule (
                 date VARCHAR(10) NOT NULL UNIQUE);''')
    conn.commit()
    conn.close()


def add_employee(name, surname):
    """Adding employee to database."""
    employee = Employee(name, surname)
    conn = sqlite3.connect(database_url)
    conn.execute('INSERT INTO employee VALUES (NULL, ?, ?, ?, ?, ?)',
                 employee.get_values())
    value = employee.get_nickname()
    conn.execute('''CREATE TABLE %s (
                 date VARCHAR(10) NOT NULL UNIQUE,
                 %s_shift VARCHAR(3));''' % (value, value))
    conn.commit()
    conn.close()


def delete_employee(nickname):
    """Deleting employee from database."""
    conn = sqlite3.connect(database_url)
    conn.execute("DELETE FROM employee WHERE nickname='%s'" % nickname)
    conn.execute('DROP TABLE IF EXISTS %s' % nickname)
    conn.commit()
    conn.close()


def get_employee_list():
    """Return list of employees nicknames."""
    conn = sqlite3.connect(database_url)
    cursor = conn.execute('SELECT nickname FROM employee')
    employee_list = []
    for row in cursor:
        employee_list.append(row[0])
    conn.commit()
    conn.close()
    return tuple(employee_list)


def get_week():
    """Return list of 14 dates from this monday."""
    conn = sqlite3.connect(database_url)
    conn.executemany('INSERT OR IGNORE INTO schedule VALUES(?)',
                     Util.get_dates_tuple())
    conn.commit()
    conn.close()
    return 'pass'


def get_schedule_for_mobile():
    """Return schedule for mobile app."""
    conn = sqlite3.connect(database_url)
    cur = conn.cursor()
    data = {}
    data['schedule'] = []
    first_day = Util.get_dates()[0]
    last_day = Util.get_dates()[-1]
    for nickname in get_employee_list():
        employee_shifts = []
        employee = {}
        conn.executemany('INSERT OR IGNORE INTO %s VALUES(?, "")' % nickname,
                         Util.get_dates_tuple())
        c = cur.execute('''SELECT name_rus, surname_rus
                    FROM employee where nickname = "%s"''' % nickname)
        for i in c:
            employee['name'] = "%s %s" % (i[0], i[1])
        query = cur.execute('SELECT * FROM %s WHERE DATE BETWEEN "%s" AND "%s"'
                            % (nickname, first_day, last_day))
        for day in query:
            employee_shifts.append({'date': day[0], 'shift': day[1]})
        employee['shifts'] = employee_shifts
        data['schedule'].append(employee)
    conn.commit()
    conn.close()
    return data


def get_this_week():
    """Return from db this week with employees shifts."""
    conn = sqlite3.connect(database_url)
    cur = conn.cursor()
    data = {}
    data['schedule'] = []
    first_day = Util.get_this_week()[0]
    last_day = Util.get_this_week()[-1]
    for nickname in get_employee_list():
        employee_shifts = []
        employee = {}
        conn.executemany('INSERT OR IGNORE INTO %s VALUES(?, "")' % nickname,
                         Util.get_dates_tuple())
        c = cur.execute('''SELECT name_rus, surname_rus
                    FROM employee where nickname = "%s"''' % nickname)
        for i in c:
            employee['name'] = "%s %s" % (i[0], i[1])
        query = cur.execute('SELECT * FROM %s WHERE DATE BETWEEN "%s" AND "%s"'
                            % (nickname, first_day, last_day))
        for day in query:
            employee_shifts.append({'date': day[0], 'shift': day[1]})
        employee['shifts'] = employee_shifts
        data['schedule'].append(employee)
    conn.commit()
    conn.close()
    return data


def get_this_week_for_site():
    """Return data for site from db ."""
    conn = sqlite3.connect(database_url)
    cur = conn.cursor()
    data = {}
    employee_list = []
    first_day = Util.get_this_week()[0]
    last_day = Util.get_this_week()[-1]
    data['dates'] = tuple(Util.get_this_week())
    for nickname in get_employee_list():
        row = []
        conn.executemany('INSERT OR IGNORE INTO %s VALUES(?, "")' % nickname,
                         Util.get_dates_tuple())
        c = cur.execute('''SELECT name_rus, surname_rus
                    FROM employee where nickname = "%s"''' % nickname)
        for i in c:
            # first item of a row is name (i[0]) and surname (i[1])
            row.append("%s %s" % (i[0], i[1]))
        query = cur.execute('SELECT * FROM %s WHERE DATE BETWEEN "%s" AND "%s"'
                            % (nickname, first_day, last_day))
        for day in query:
            row.append(day[1])  # fill row by fhifts
        employee_list.append(tuple(row))
    data['schedule'] = tuple(employee_list)
    conn.commit()
    conn.close()
    return data
