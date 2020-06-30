import os
import sys
from flask import Flask, render_template, redirect, request
from flask_mail import Mail, Message

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(FILE_PATH, 'src'))

from estimator import Analysis, Input
from render_utils import *


def create_app():
    flask_app = Flask(__name__)
    return flask_app


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

app = create_app()
app.config.update(mail_settings)
mail = Mail(app)


@app.route("/")
def index():
    return redirect('/calculator')


@app.route("/calculator")
def calculator():
    return render_template('calculator.html', house_details=None)


@app.route("/calculator", methods=['POST'])
def calculator_post():
    loan = get_loan(request.form)
    params = get_user_parameters(request.form)
    listing = get_listing(request.form)
    inp = Input(loan, params, listing)
    analysis = Analysis(inp)
    expenses = Analysis.calculate_monthly_expenses(inp)
    return render_template('calculator.html', analysis=analysis, expenses=expenses, request=request)


@app.route('/about')
def render_about():
    return render_template('about.html')


@app.route('/contact')
def render_contacts():
    return render_template('contacts.html')


@app.route('/contact', methods=['POST'])
def contacts_post():
    form = request.form
    subject = 'Feedback from %s' % form['Name']
    text = 'Subject: ' + form['Subject'] + '\n'
    text = text + 'Email: ' + form['Email'] + '\n'
    text = text + form['Comment']
    msg = Message(subject,
                  body=text,
                  sender=app.config.get("MAIL_USERNAME"),
                  recipients=["rippx009@gmail.com"])
    mail.send(msg)
    return render_template('feedback.html', message='Thank you for your feedback.')


def render_error(error='Ops. Error occurred.'):
    return render_template('error.html', error=error)


#@app.errorhandler(Exception)
#def special_exception_handler(error):
#    return render_error(error=error)
