#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from movie import *
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        moviename = request.form['movie_name']
        getmovies()
        checkers = checkname()
        if checkers == False:
            return render_template('pages/placeholder.home.html', checker=True)
        moviename = "#" + moviename + " #movie"
        df = searching(moviename)
        if df.empty:
            return render_template('pages/placeholder.home.html', empt=True)
        return render_template('pages/placeholder.home.html', df=df, check=True)
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


# Default port:
if __name__ == '__main__':
    app.run()
