# -*- encoding: utf-8 -*-
from datetime import datetime
import flask
from flask import render_template

from . import app


@app.route('/')
@app.route('/home')
def home():
    user = dict(username='Shane Xiang')
    # the chosen path name for templates: templates
    return render_template('home.html', title='Home', user=user, curr_time=datetime.now())
