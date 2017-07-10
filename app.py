# -*- coding: utf-8 -*-
"""ORRM Schedule application."""

from flask import Flask, jsonify, render_template, request
from werkzeug.security import check_password_hash
from database import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_page():
    if request.method == 'POST':
        if check_password_hash(get_admin_pwhash(), request.form['password']):
            return jsonify({'status': 'OK'})
        else:
            return jsonify({'status': '404'})
    return render_template('index.html')


@app.route('/employees')
def get_employees_list():
    """Return employees data from database"""
    return jsonify(get_employees())


@app.route('/add_employee', methods=['POST'])
def add_employee_to_db():
    if request.method == 'POST':
        add_employee(request.form['name_rus'], request.form['surname_rus'])
        return jsonify({'status': 'OK'})


@app.route('/delete_employee', methods=['POST'])
def delete_employee_from_db():
    if request.method == 'POST':
        delete_employee(request.form['name_rus'], request.form['surname_rus'])
        return jsonify({'status': 'OK'})


@app.route('/schedule', methods=['POST'])
def get_schedule_from_db():
    if request.method == 'POST':
        return jsonify(get_schedule(request.form.to_dict()))


@app.route('/update_schedule', methods=['POST'])
def update_schedule_in_db():
    if request.method == 'POST':
        print(request.form)
        update_schedule(request.form['shortname'], request.form['date'],
                        request.form['shift'])
        return jsonify({'status': 'OK'})


if __name__ == "__main__":
    app.run()
