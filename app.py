# -*- coding: utf-8 -*-
"""ORRM Schedule application."""

from flask import Flask, jsonify, render_template, session, request, redirect, \
    url_for
from database import get_this_week_for_site, get_schedule_for_mobile
from util import Util

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_page():
    """Default page."""
    if request.method == 'POST':
        if request.form['password'] == 'Mtbank_1':
            print(request.form['password'])
            return jsonify({'status': 'OK'})
        else:
            return jsonify({'status': '404'})
    return render_template('index.html', dates_this_week=Util.get_this_week(),
                           this_week=get_this_week_for_site())


@app.route('/mobile')
def get_test():
    """Return json for mobile app."""
    return jsonify(get_schedule_for_mobile())


if __name__ == "__main__":
    app.run()
