# armRESTs - Robin Han, Aleksandra Koroza, Johnny Wong
# SoftDev1 pd8
# P01: ArRESTed Development

import os
from flask import Flask, redirect, url_for, render_template, session, request, flash, get_flashed_messages
from utils import database as arms


# instantiate Flask object
app = Flask(__name__)
app.secret_key = os.urandom(32)

# manage cookies and user data here
DB_FILE = "data/armRESTs.db"
user = None
def setUser(userName):
    global user
    user = userName

@app.route('/')
def index():
    if user in session:
        return render_template('index.html', logged_in = True)
    return render_template('index.html', errors = True, logged_in = False)

@app.route('/register')
def register():
    if user in session:
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    if user in session:
        return redirect(url_for('index'))
    # instantiates DB_Manager with path to DB_FILE
    data = arms.DB_Manager(DB_FILE)
    username, password = request.form['username'], request.form['password']
    # LOGGING IN
    if request.form["submit"] == "Login":
        if username != "" and password != "" and data.verifyUser(username, password):
            session[username] = password
            setUser(username)
            data.save()
            return redirect(url_for('index'))
        # user was found in DB but password did not match
        elif data.findUser(username):
            flash('Incorrect password!')
        # user not found in DB at all
        else:
            flash('Incorrect username!')
        data.save()
        return redirect(url_for('index'))
    # REGISTERING
    else:
        if len(username.strip()) != 0 and not data.findUser(username):
            if len(password.strip()) != 0:
                # add account to DB
                data.registerUser(username, password)
                data.save()
                return redirect(url_for('index'))
            else:
                flash('Password length insufficient')
        elif len(username) == 0:
            flash('Username length insufficient')
        else:
            flash('Username already taken!')
        # Try to register again
        return render_template('register.html', errors = True)

@app.route('/logout')
def logout():
    session.pop(user, None)
    setUser(None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run()
