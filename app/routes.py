# -*- encoding: utf-8 -*-
from typing import *
import time
from functools import partial
from urllib.parse import urlsplit
import flask

# Plugins
from flask_login import (login_user, current_user, logout_user, login_required)

from app import app, forms, db, success, fail, forEach
from app.models import *
from app.security.saltypassword import *
from app.security.check import check_valid_username
from app.utils.gravatar import *


render_template = partial(flask.render_template)
current_time = lambda: time.strftime('%Y-%m-%d %H:%M')


def getAllPosts() -> List[Dict[str, Any]]:
    return [
        {
            'poster': post.poster.username,
            'content': post.content,
            'post_time': post.post_time,
        } for post in Posts().all()
    ]


def flash_parse(flash_messages) -> Optional[List[str]]:
    parse = lambda msg: [
        'success' if (msg_ := msg.split(';'))[0] == 'success'
        else 'error', msg_[-1]
    ]
    return forEach(flash_messages, parse, ret_val=True) if flash_messages else []


@app.route('/')
@app.route('/home')
@login_required
def home():
    # the chosen path name for templates: templates
    return render_template('home.html', route='Home', posts=current_user.get_visible_posts(),
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
    return render_template('user/profile.html', flash_parse=flash_parse, username=username,
                           current_time=current_time(), user=BlogUser.get_uuser(username=username))


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

    if changed:
        BlogUser().flush().commit()
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
    if not (reg_form := forms.UserRegForm()).validate_on_submit():
        return render_template('signup.html', reg_form=reg_form, route='Sign Up', flash_parse=flash_parse,
                               current_time=current_time())

    new_user = BlogUser()
    new_user.email = reg_form.email.data
    new_user.username = reg_form.username.data
    new_user.password = SaltyPassword.saltify(reg_form.password.data)

    with GravatarFetcher(email=new_user.email) as fetcher:
        new_user.avatar = fetcher.fetch(size=100).url

    BlogUser(False).add(new_user).flush().commit()

    flask.flash(success('you successfully registered your account, please login...'))
    return flask.redirect(flask.url_for('login'))
