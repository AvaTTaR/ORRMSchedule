# -*- coding: utf-8 -*-
"""ORRM Schedule application."""

from flask import Flask, jsonify, render_template, request
from werkzeug.security import check_password_hash
from database import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_page():
    """Default page."""
    if request.method == 'POST':
        if check_password_hash(get_admin_pwhash(), request.form['password']):
            return jsonify({'status': 'OK'})
        else:
            return jsonify({'status': '404'})
    return render_template('index.html',
                           this_week=Util.get_dates_for_site("this"),
                           next_week=Util.get_dates_for_site("next"))


@app.route('/employees')
def get_employees_list():
    """Return employees data from database."""
    return jsonify(get_employees())


@app.route('/add_employee', methods=['POST'])
def add_employee_to_db():
    """Add employee to database."""
    if request.method == 'POST':
        add_employee(request.form['name_rus'], request.form['surname_rus'])
        return jsonify({'status': 'OK'})


@app.route('/delete_employee', methods=['POST'])
def delete_employee_from_db():
    """Delete employee from database."""
    if request.method == 'POST':
        delete_employee(request.form['name_rus'], request.form['surname_rus'])
        return jsonify({'status': 'OK'})


@app.route('/schedule=<string:param>')
def get_schedule_from_db(param):
    """Return schedule."""
    return jsonify(get_schedule(param))


@app.route('/schedule', methods=['POST'])
def update_schedule():
    if request.method == 'POST':
        update(request.form['shortname'], request.form['date'],
               request.form['shift'])
        return jsonify({'status': 'OK'})


if __name__ == "__main__":
    app.run()
