#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os

import requests

def valBVN(bvnNumber):
    bvnNumber= str(bvnNumber)
    tokenKey= 'FLWSECK-af1ff421c70907112ba55815f89710ea-X'
    api= 'https://ravesandboxapi.flutterwave.com/v2/kyc/bvn/'+ bvnNumber+'?seckey='+ tokenKey

    r= requests.get(api)

    return r.json
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
        bvnNo = request.form['bvnNumber']
        if not bvnNo.isdigit():
            return render_template('pages/placeholder.home.html', digit_check=True)
        if len(bvnNo) != 11:
            return render_template('pages/placeholder.home.html', length_check= True)
        print(bvnNo)
        checkBVN= valBVN(bvnNo)
        if checkBVN()['status']== 'error':
            return render_template('pages/placeholder.home.html', error_message= checkBVN()['message'] )
        if checkBVN()['status']== 'success':
            return render_template('pages/placeholder.home.html', name= checkBVN()['data']['first_name'] +" "+ checkBVN()['data']['middle_name'] +" "+ checkBVN()['data']['last_name'], date= checkBVN()['data']['date_of_birth'], phonenumber= checkBVN()['data']['phone_number'] )
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
