from flask import Flask, request, render_template, make_response, redirect, url_for, abort
import random

app = Flask(__name__)


@app.route('/')
def lucky():
    try:
        cookie_val = request.cookies.get('lucky_number')
        if cookie_val == None:
            prev_lucky_number = "(No previous value. Seems you cleared your cookie or it's the first time you run this app.)"
        else:
            prev_lucky_number = int(cookie_val)
    except ValueError:
        # Probably the value in the cookie was not an integer number
        abort(400)        
    lucky_number = random.randint(0,99)
    resp = make_response(
        render_template('lucky_number.html', 
            prev_lucky_number=prev_lucky_number, 
            lucky_number=lucky_number))
    resp.set_cookie('lucky_number', str(lucky_number))
    return resp


@app.route('/clear')
def clear():
    resp = make_response(redirect(url_for('lucky')))
    resp.set_cookie('lucky_number', '', expires=0)
    return resp


@app.route('/badcookie')
def bad_cookie():
    resp = make_response(redirect(url_for('lucky')))
    resp.set_cookie('lucky_number', 'bad_cookie_is_not_an_integer_number')
    return resp


# run with
# on Linux:
#   export FLASK_APP="main.py"
#   export FLASK_ENV="development"
#   flask run -h 127.0.0.2 -p 5001
# in Powershell:
#   $env:FLASK_APP="main.py"
#   $env:FLASK_ENV="development"
#   flask run -h 127.0.0.2 -p 5001
