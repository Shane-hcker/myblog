# -*- encoding: utf-8 -*-
from typing import *
import asyncio
import time
from functools import partial
import flask

# Plugins
from flask_login import (login_user, current_user, logout_user, login_required)

from . import app
from . import forms
from .models import *

from typing import Dict

render_template = partial(flask.render_template, curr_time=time.strftime('%Y-%m-%d %H:%M'))


def getPosts() -> List[Dict[str, Any]]:
    return [
        {
            'author': post.poster.username_,
            'content': post.content_,
            'date': post.post_time
        } for post in Posts.query.all()
    ]


@app.route('/')
@app.route('/home')
@login_required
def home():
    # the chosen path name for templates: templates
    return render_template('home.html', route='Home', posts=getPosts())


@app.route('/login', methods=['GET', 'POST'])
async def login() -> Any:
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('home'))

    # True |> POST + (validators -> true)
    if not (login_form := forms.UserLoginForm()).validate_on_submit():
        return render_template('login.html', loginform=login_form, route='Sign In')

    get_login_user = BlogUser.query.filter_by(email=login_form.email.data).first()
    if not BlogUser.isUserValid(login_form, get_login_user):
        flask.flash('Invalid username or password')
        return flask.redirect(flask.url_for('login'))

    # login
    login_user(get_login_user, remember=login_form.remember.data)

    # display info
    username, do_remember = login_form.username.data, login_form.remember.data
    login_time = time.strftime("%Y-%m-%d %H:%M")
    msg = f'{username} logged in at {login_time}\tRemember: {do_remember}'
    flask.flash(msg)

    # flask.url_for() -> prevent future route change
    # url_for refers to the func that covers the template
    return flask.redirect(flask.url_for('home'))  # redirect


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html', route='Sign Up')


@app.route('/logout')
def logout():
    logout_user()  # no args required.
    return flask.redirect(flask.url_for('home'))

