# -*- encoding: utf-8 -*-
from typing import *
import time
from functools import partial
from urllib.parse import urlsplit
import flask

# Plugins
from flask_login import (login_user, current_user, logout_user, login_required)

from . import app
from . import forms
from .models import *
# from .utils.validators import loginRequired

render_template = partial(flask.render_template)


def getPosts() -> List[Dict[str, Any]]:
    return [
        {
            'author': post.poster.username_,
            'content': post.content_,
            'date': post.post_time,
        } for post in Posts.query.all()
    ]


@app.route('/')
@app.route('/home')
@login_required
def home():
    # the chosen path name for templates: templates
    return render_template('home.html', route='Home', posts=getPosts(),
                           current_time=time.strftime('%Y-%m-%d %H:%M'))


@app.route('/login', methods=['GET', 'POST'])
async def login() -> Any:
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('home'))

    # True |> POST + (validators -> true)
    if not (login_form := forms.UserLoginForm()).validate_on_submit():
        return render_template('login.html', loginform=login_form, route='Sign In',
                               current_time=time.strftime('%Y-%m-%d %H:%M'))

    get_login_user = BlogUser.get_uuser(email=login_form.email.data)
    if not BlogUser.isUserValid(login_form, get_login_user):
        flask.flash('Invalid username or password')
        return flask.redirect(flask.url_for('login'))

    # getting `next` from URL
    next_page = flask.request.args.get('next')
    if not next_page or urlsplit(next_page).netloc != '':
        next_page = flask.url_for('home')

    # login
    login_user(get_login_user, remember=login_form.remember.data)

    # display info
    username, do_remember = login_form.username.data, login_form.remember.data
    login_time = time.strftime("%Y-%m-%d %H:%M")
    msg = f'{username} logged in at {login_time}\tRemember: {do_remember}'

    flask.flash(msg)

    # flask.url_for() -> prevent future route change
    # url_for refers to the func that covers the template
    return flask.redirect(next_page)  # redirect


@app.route('/logout')
def logout():
    logout_user()  # no args required.
    return flask.redirect(flask.url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if not (regForm := forms.UserRegForm()).validate_on_submit():
        return render_template('signup.html', regForm=regForm, route='Sign Up',
                               current_time=time.strftime('%Y-%m-%d %H:%M'))
