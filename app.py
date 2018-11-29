# armRESTs - Robin Han, Aleksandra Koroza, Johnny Wong
# SoftDev1 pd8
# P01: ArRESTed Development

import os
from flask import Flask, redirect, url_for, render_template, session, request, flash, get_flashed_messages
from utils import database as arms
from utils import api


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
    pops= api.getPopular()
    genres = api.getGenres()
    if user in session:
        return render_template('index.html', errors = True, logged_in = True, trend=pops, sidebar= genres)
    return render_template('index.html', errors = True, logged_in = False, trend=pops, sidebar= genres)

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
            flash('Successfully logged in!')
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
                setOut()
                flash('Successfully registered account for user  "{}"'.format(username))
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
    flash('Successfully logged out!')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    pass

@app.route('/search',methods=['POST'])
def search():
    #following code can be shortened
    if request.form["Submit"] == "Search1":
        entry = request.form['entry']
        if len(entry.strip()) != 0:
            if user in session:
                return render_template('searchResults.html', movie= entry, logged_in=True)
            else:
                return render_template('searchResults.html', movie= entry, logged_in=False)
        flash("Please input a movie name!")
        return redirect(url_for('index'))

    elif request.form["Submit"] == "Search2":
        entry = request.form['entry']
        if len(entry.strip()) != 0:
            if user in session:
                return render_template('mood.html', movie= entry, logged_in=True)
            else:
                return render_template('mood.html', movie= entry, logged_in=False)
        flash("Please input a movie name!")
        return redirect(url_for('index'))

    elif request.form["Submit"] == "Search3":
        entry = request.form['entry']
        if len(entry.strip()) != 0:
            if user in session:
                return render_template('searchResults.html', movie= entry, logged_in=True)
            else:
                return render_template('searchResults.html', movie= entry, logged_in=False)
        flash("Please input a movie name!")
        return redirect(url_for('index'))

@app.route('/mood',methods=['POST'])
def mood():
    if request.form["submit"] == "Happy":
        #fill in some API shenanigans
        #possible problem: passing in entry from searching into mood
        return render_template('searchResults.html')
    if request.form["submit"] == "Sad":
        return render_template('searchResults.html')
    if request.form["submit"] == "Stressed":
        return render_template('searchResults.html')
    if request.form["submit"] == "Bored":
        return render_template('searchResults.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
