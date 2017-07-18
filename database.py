# -*- coding: utf-8 -*-
import os
import sqlite3

from models import Employee
from util import Util
from werkzeug.security import generate_password_hash

database_url = '{}{}'.format(os.path.dirname(os.path.realpath(__file__)),
                             '/database.db')


def init_db():
    """Initiate db and set admin password"""
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
                 employee_shift VARCHAR(3) DEFAULT 'X',
                 UNIQUE (date, shortname));''')

    conn.execute('''CREATE TABLE keys (
                     shortname VARCHAR NOT NULL,
                     password VARCHAR NOT NULL);''')

    password = generate_password_hash(input("Enter password: "))
    conn.execute('''INSERT INTO keys VALUES (?, ?);''', ['admin', password])
    conn.commit()
    conn.close()


def get_admin_pwhash():
    """Get password hash to compare with password hash from login modal"""
    shortname = 'admin'
    conn = sqlite3.connect(database_url)
    cur = conn.execute \
        ("SELECT password FROM keys WHERE shortname = ?", [shortname])
    pwhash = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return pwhash


def add_employee(name_rus, surname_rus):
    """Adding employee to database"""
    employee = Employee(name_rus, surname_rus)
    conn = sqlite3.connect(database_url)
    conn.execute('INSERT INTO employees VALUES (NULL, ?, ?, ?, ?, ?)',
                 employee.get_values())
    conn.commit()
    conn.close()


def delete_employee(name_rus, surname_rus):
    """Deleting employee from database"""
    conn = sqlite3.connect(database_url)
    conn.execute("DELETE FROM employees WHERE name_rus=? AND surname_rus=?",
                 [name_rus, surname_rus])
    conn.commit()
    conn.close()


def get_employees_shortnames():
    """Return list of employees nicknames"""
    conn = sqlite3.connect(database_url)
    cursor = conn.execute('SELECT shortname FROM employees')
    employees = []
    for row in cursor:
        employees.append(row[0])
    conn.commit()
    conn.close()
    return tuple(employees)


def get_employees():
    """Return list of employees shortnames"""
    conn = sqlite3.connect(database_url)
    cursor = conn.execute \
        ('SELECT name_rus, surname_rus FROM employees')
    employees = []
    for row in cursor:
        employees.append({'name_rus': row[0], 'surname_rus': row[1]})
    conn.commit()
    conn.close()
    return employees


def get_schedule(iso_week):
    conn = sqlite3.connect(database_url)
    cur = conn.cursor()

    schedule = []
    dates_to_insert = []  # List of dates to insert in db if they not exist
    shortnames = get_employees_shortnames()
    week = Util.get_ordinary_week(iso_week)

    # Loop through list with shortnames and fill list with schedule
    for shortname in shortnames:

        # Fill list with dates to insert in db
        for day in week:  # Week has format: {'tuesday': '2017-07-18', ...}
            date = [week[day], shortname]
            dates_to_insert.append(tuple(date))

        conn.executemany('''INSERT OR IGNORE INTO schedule(date, shortname) 
                            VALUES(?, ?)''', dates_to_insert)

        # Create and fill dict with employee name, shortname and schedule
        employee_schedule = {}
        select = cur.execute('''SELECT name_rus, surname_rus, shortname 
                                FROM employees WHERE shortname = ?''',
                             [shortname])

        for employee in select:
            name_rus = employee[0]
            surname_rus = employee[1]
            shortname = employee[2]
            employee_schedule['name'] = "%s %s" % (name_rus, surname_rus)
            employee_schedule['shortname'] = shortname

        query = cur.execute('''SELECT date,employee_shift 
                               FROM schedule WHERE shortname=? 
                               AND date BETWEEN ? AND ?''',
                            [shortname, week['monday'], week['friday']])

        # Add days with shifts to dict with employee schedule
        for day in query:
            date = day[0]
            shift = day[1]
            day = Util.get_day_by_date(date)
            employee_schedule[day] = shift

        schedule.append(employee_schedule)

    conn.commit()
    conn.close()
    return schedule


def update_schedule(shortname, iso_week, shift):
    """Update schedule"""
    conn = sqlite3.connect(database_url)
    cur = conn.cursor()

    date = Util.iso_week_to_date(iso_week)
    cur.execute('''UPDATE schedule SET employee_shift=? 
                   WHERE date=? AND shortname=?''', [shift, date, shortname])

    conn.commit()
    conn.close()
