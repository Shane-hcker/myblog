# -*- encoding: utf-8 -*-
from typing import *
from functools import partial
import time
import flask

from . import app
from . import forms


render_template = partial(flask.render_template, curr_time=time.strftime('%Y-%m-%d %H:%M'))


@app.route('/')
@app.route('/home')
def home() -> str:
    posts = [
        {
            'author': 'admin',
            'content': 'add',
            'date': '2020-11-04'
        },
        {
            'author': 'guest',
            'content': 'fuckfuck',
            'date': '...'
        }
    ]

    # the chosen path name for templates: templates
    return render_template('home.html', route='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login() -> Any:
    # True |> POST + validators -> true
    login_form = forms.UserLoginForm()
    if login_form.validate_on_submit():
        # display info
        flask.flash(f'{login_form.username.data} logged in at {time.strftime("%Y-%m-%d %H:%M")}\t'
                    f'Remember: {login_form.remember.data}')
        # flask.url_for() -> 防止如果未来路由发生改变全部东西都要改
        # url_for refers to the func that covers the template
        return flask.redirect(flask.url_for('home'))  # redirect

    return render_template('login.html', loginform=login_form, route='Sign In')
