from . import app
from flask import render_template
from .routes import current_time


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html', current_time=current_time())


@app.errorhandler(500)
def error_500(e):
    return render_template('errors/500.html', current_time=current_time())
