# -*- coding: utf-8 -*-
"""ORRM Schedule application."""

from flask import Flask, jsonify, render_template, request

from database import get_this_week_for_site, get_schedule_for_mobile, \
    get_employee_data, add_employee, delete_employee
from util import Util

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_page():
    """Default page."""
    if request.method == 'POST':
        if request.form['password'] == '123':
            return jsonify({'status': 'OK'})
        else:
            return jsonify({'status': '404'})
    return render_template('index.html', dates_this_week=Util.get_this_week(),
                           this_week=get_this_week_for_site())


@app.route('/add_employee', methods=['POST'])
def add_employee_to_db():
    """Add employee to database."""
    if request.method == 'POST':
        add_employee(request.form['name'], request.form['surname'])
        return jsonify({'status': 'OK'})


@app.route('/delete_employee', methods=['POST'])
def delete_employee_from_db():
    """Add employee to database."""
    if request.method == 'POST':
        delete_employee(request.form['id'])
        return jsonify({'status': 'OK'})


@app.route('/mobile')
def get_mobile_data():
    """Return json for mobile app."""
    return jsonify(get_schedule_for_mobile())


@app.route('/employees')
def get_employees():
    """Return employees data from database."""
    return jsonify(get_employee_data())


if __name__ == "__main__":
    app.run()
