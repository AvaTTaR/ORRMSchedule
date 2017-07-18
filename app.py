# -*- coding: utf-8 -*-
"""ORRM Schedule application."""

from flask import Flask, jsonify, render_template, request, Response
from werkzeug.security import check_password_hash

from database import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_page():
    if request.method == 'POST':
        if check_password_hash(get_admin_pwhash(), request.form['password']):
            return Response(status=200)
        else:
            return Response(status=403)
    return render_template('index.html')


@app.route('/api/v1/employees', methods=['GET', 'POST', 'DELETE'])
def employees():
    if request.method == 'GET':
        return jsonify(get_employees())
    if request.method == 'POST':
        if Util.is_valid_employee(request.form['name_rus'],
                                  request.form['surname_rus']):
            add_employee(request.form['name_rus'], request.form['surname_rus'])
            return Response(status=201)
        return Response(status=400)
    if request.method == 'DELETE':
        if Util.is_valid_employee(request.form['name_rus'],
                                  request.form['surname_rus']):

            delete_employee(request.form['name_rus'],
                            request.form['surname_rus'])
            return Response(status=200)
        return Response(status=400)


@app.route('/api/v1/schedule', methods=['PUT'])
@app.route('/api/v1/schedule/<string:iso_week>', methods=['GET'])
def schedule(iso_week=None):
    if request.method == 'GET':
        return jsonify(get_schedule(iso_week))
    if request.method == 'PUT':
        update_schedule(request.form['shortname'], request.form['iso_week'],
                        request.form['shift'])
        return Response(status=200)


if __name__ == "__main__":
    app.run()
