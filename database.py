# -*- coding: utf-8 -*-
"""Database module."""

import os
import sqlite3

from models import Employee
from util import Util
from werkzeug.security import generate_password_hash

database_url = '{}{}'.format(os.path.dirname(os.path.realpath(__file__)),
                             '/database.db')


def init_db():
    """Initiate db and set admin password."""
    if os.path.exists(database_url):
        os.remove(database_url)
    conn = sqlite3.connect(database_url)
    conn.execute('''CREATE TABLE employees (
                 id INTEGER NOT NULL,
                 name_rus VARCHAR(15),
                 surname_rus VARCHAR(15),
                 name_eng VARCHAR(15),
                 surname_eng VARCHAR(15),
                 shortname VARCHAR(15),
                 PRIMARY KEY(id),
                 UNIQUE (id, name_rus, name_eng));''')
    conn.execute('''CREATE TABLE schedule (
                 date VARCHAR(10),
                 shortname VARCHAR(10),
                 employee_shift VARCHAR(3) DEFAULT '',
                 UNIQUE (date, shortname));''')
    conn.execute('''CREATE TABLE keys (
                     shortname VARCHAR NOT NULL,
                     password VARCHAR NOT NULL);''')
    password = generate_password_hash(input("Введите пароль: "))
    conn.execute('''INSERT INTO keys VALUES (?, ?);''', ['admin', password])
    conn.commit()
    conn.close()


def get_admin_pwhash():
    shortname = 'admin'
    conn = sqlite3.connect(database_url)
    cur = conn.execute\
        ("SELECT password FROM keys WHERE shortname = ?", [shortname])
    pwhash = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return pwhash


def add_employee(name_rus, surname_rus):
    """Adding employee to database."""
    employee = Employee(name_rus, surname_rus)
    conn = sqlite3.connect(database_url)
    conn.execute('INSERT INTO employees VALUES (NULL, ?, ?, ?, ?, ?)',
                 employee.get_values())
    conn.commit()
    conn.close()


def delete_employee(name_rus, surname_rus):
    """Deleting employee from database."""
    conn = sqlite3.connect(database_url)
    conn.execute("DELETE FROM employees WHERE name_rus=? AND surname_rus=?",
                 [name_rus, surname_rus])
    conn.commit()
    conn.close()


def get_employees_shortname():
    """Return list of employees nicknames."""
    conn = sqlite3.connect(database_url)
    cursor = conn.execute('SELECT shortname FROM employees')
    employees = []
    for row in cursor:
        employees.append(row[0])
    conn.commit()
    conn.close()
    return tuple(employees)


def get_employees():
    """Return list of employees nicknames."""
    conn = sqlite3.connect(database_url)
    cursor = conn.execute \
        ('SELECT name_rus, surname_rus FROM employees')
    employees = []
    for row in cursor:
        employees.append({'name_rus': row[0], 'surname_rus': row[1]})
    conn.commit()
    conn.close()
    return employees


def get_schedule(week_param):
    """Return from db this week with employees shifts."""
    conn = sqlite3.connect(database_url)
    cur = conn.cursor()
    data = []
    first_day = Util.get_dates(week_param)[0]
    last_day = Util.get_dates(week_param)[-1]
    data_to_insert = []
    for shortname in get_employees_shortname():
        for i in Util.get_dates(week_param):
            date = [i, shortname]
            data_to_insert.append(tuple(date))
        employee_data = {}
        conn.executemany('''INSERT OR IGNORE INTO schedule(date, shortname) 
                            VALUES(?, ?)''', data_to_insert)
        c = cur.execute('''SELECT name_rus, surname_rus, shortname 
                           FROM employees where shortname = ?''', [shortname])
        for i in c:
            employee_data['name'] = "%s %s" % (i[0], i[1])
            employee_data['shortname'] = i[2]
        query = cur.execute('''SELECT date,employee_shift 
                               FROM schedule WHERE shortname=? 
                               AND date BETWEEN ? AND ?''',
                            [shortname, first_day, last_day])
        for day in query:
            # date = day[0] and shift = day[1]
            employee_data[Util.format_date(day[0])] = day[1]
        data.append(employee_data)
    conn.commit()
    conn.close()
    return data

#def get_schedule(week_param):
#    """Return from db this week with employees shifts."""
#    conn = sqlite3.connect(database_url)
#    cur = conn.cursor()
#    data = {'schedule': []}
#    first_day = Util.get_dates(week_param)[0][0]
#    last_day = Util.get_dates(week_param)[-1][0]
#    data_to_insert = []
#    for shortname in get_employees_shortname():
#        for i in Util.get_dates(week_param):
#            i.append(shortname)
#            data_to_insert.append(tuple(i))
#        employee_shifts = []
#        employee = {}
#        conn.executemany('''INSERT OR IGNORE INTO schedule(date, shortname)
#                            VALUES(?, ?)''', data_to_insert)
#        c = cur.execute('''SELECT name_rus, surname_rus
#                           FROM employees where shortname = ?''', [shortname])
#        for i in c:
#            employee['name'] = "%s %s" % (i[0], i[1])
#        query = cur.execute('''SELECT date,employee_shift
#                               FROM schedule WHERE shortname=?
#                               AND date BETWEEN ? AND ?''',
#                            [shortname, first_day, last_day])
#        for day in query:
#            employee_shifts.append({'date': day[0], 'shift': day[1]})
#        employee['shifts'] = employee_shifts
#        data['schedule'].append(employee)
#    conn.commit()
#    conn.close()
#    return data