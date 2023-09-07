# -*- encoding: utf-8 -*-
from typing import *
import os
import time
from functools import partial
from urllib.parse import urlsplit
import flask

from PIL import Image
from werkzeug.utils import secure_filename, send_file, send_from_directory
from werkzeug.security import safe_join

# Plugins
from flask_login import current_user, login_user, logout_user, login_required

from app import forms, app, success, fail
from app.models import *

from app.config import AppConfig
from app.utils.check import check_valid_username
from app.utils.saltypassword import *
from app.utils.avatar import *
from app.utils.misc import *


render_template = partial(flask.render_template)
current_time = lambda: time.strftime('%Y-%m-%d %H:%M')


@app.route('/')
@app.route('/home')
@login_required
def home():
    # the chosen path name for templates: templates
    return render_template('home.html', route='Home', posts=current_user.visible_posts(),
                           current_time=current_time(), flash_parse=flash_parse)


@app.route('/login', methods=['GET', 'POST'])
def login() -> Any:
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('home'))

    # True |> POST + (validators -> true)
    if not (login_form := forms.UserLoginForm()).validate_on_submit():
        return render_template('login.html', login_form=login_form, route='Sign In',
                               current_time=current_time(), flash_parse=flash_parse, is_debug=app.debug)

    logged_in_user = BlogUser.get_uuser(email=login_form.email.data, username=login_form.username.data)
    if not BlogUser.is_user_valid(login_form, logged_in_user):
        flask.flash(fail('Invalid username or password'))
        return flask.redirect(flask.url_for('login'))

    # getting `next` from URL
    next_page = flask.request.args.get('next')
    if not next_page or urlsplit(next_page).netloc != '':
        next_page = flask.url_for('home')

    # login
    login_user(logged_in_user, remember=login_form.remember.data)

    logged_in_user.reset_recent_login()

    # display info
    username, do_remember = login_form.username.data, login_form.remember.data
    login_time = time.strftime("%Y-%m-%d %H:%M")
    msg = f'{username} logged in at {login_time}\tRemember: {do_remember}'

    flask.flash(success(msg))

    # flask.url_for() -> prevent future route change
    # url_for refers to the func that covers the template
    return flask.redirect(next_page)  # redirect


@app.route('/user/<username>/profile')
@login_required
@check_valid_username
def profile(username):
    if not (form := forms.BasicForm()).validate_on_submit():
        return render_template('user/profile.html', flash_parse=flash_parse, username=username,
                               current_time=current_time(), user=BlogUser.get_uuser(username=username),
                               form=form)


@app.route('/user/<username>/profile/edit', methods=['GET', "POST"])
@login_required
@check_valid_username
def profile_edit(username):
    if username != current_user.username:
        return render_template('errors/404.html')

    if not (edit_form := forms.ProfileEditForm(username, email := current_user.email)).validate_on_submit():
        return render_template('user/pedit.html', edit_form=edit_form, flash_parse=flash_parse,
                               current_time=current_time(), username=username)

    changed = False

    if edit_form.username.data != username:
        changed = True
        current_user.username = edit_form.username.data

    if edit_form.email.data != email:
        changed = True
        current_user.email = edit_form.email.data

    if raw_avatar := flask.request.files['avatar']:
        filename = secure_filename(raw_avatar.filename)
        changed = True
        with Avatar(raw_avatar.stream) as avatar:
            save_path = os.path.join(AppConfig.AVATAR_DIR, filename)
            avatar.resize(100).save(save_path)
            current_user.avatar = avatar.src

    if not changed:
        BlogUser(False).commit()
        flask.flash(success('successfully changed your profile!'))

    return flask.redirect(flask.url_for('profile_edit', username=current_user.username))


@app.route('/user/<username>/posts')
@login_required
@check_valid_username
def user_posts(username):
    posts = BlogUser.get_uuser(username=username).get_user_posts()
    return render_template('user/user_posts.html', posts=posts, username=username,
                           current_time=current_time())


@app.route('/logout')
def logout():
    logout_user()  # no args required.
    return flask.redirect(flask.url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('home'))

    if not (reg_form := forms.UserRegForm()).validate_on_submit():
        return render_template('signup.html', reg_form=reg_form, route='Sign Up', flash_parse=flash_parse,
                               current_time=current_time())

    new_user = BlogUser(
        email=reg_form.email.data, 
        username=reg_form.username.data,
        password=SaltyPassword.saltify(reg_form.password.data)
    )

    with Avatar(AppConfig.DEFAULT_AVATAR) as avatar:
        avatar.resize(70)
        new_user.avatar = avatar.src

    BlogUser(False).add(new_user).commit()

    flask.flash(success('you successfully registered your account, please login...'))
    return flask.redirect(flask.url_for('login'))
