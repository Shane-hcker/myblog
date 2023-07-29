from . import app, db
from flask import render_template
from .routes import current_time


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def error_500(e):
    db.session.rollback()
    return render_template('errors/500.html'), 500
