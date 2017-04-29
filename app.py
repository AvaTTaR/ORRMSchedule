# -*- coding: utf-8 -*-
"""ORRM Schedule application."""

from flask import Flask, jsonify, render_template
from database import get_this_week_for_site, get_schedule_for_mobile
# from flask_bootstrap import Bootstrap
from util import Util

app = Flask(__name__)
# Bootstrap(app)


@app.route('/', methods=['GET'])
def get_page():
    """Return."""
    return render_template('index.html', dates_this_week=Util.get_this_week(),
                           this_week=get_this_week_for_site())


@app.route('/mobile')
def get_test():
    """Return json for mobile app."""
    return jsonify(get_schedule_for_mobile())


if __name__ == "__main__":
    app.run()
