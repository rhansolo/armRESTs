# armRESTs - Robin Han, Aleksandra Koroza, Johnny Wong
# SoftDev1 pd8
# P01: ArRESTed Development

import os
import random

from flask import Flask, redirect, url_for, render_template, session, request, flash, get_flashed_messages

from utils import database as arms, api


# instantiate Flask object
app = Flask(__name__)
app.secret_key = os.urandom(32)

# manage cookies and user data here
#instatiate users and votes table if does not already exist
DB_FILE = "data/armRESTs.db"
user = None
pageInterval = [1,2,3,4,5]
pageDict = {'1': [str(x) for x in pageInterval.copy()]}
genres = api.getGenres()
data = arms.DB_Manager(DB_FILE)
data.createVoteTable()
data.createUsers()

def setUser(userName):
    '''
    Sets the user global variable to userName
    Useful for many other methods
    '''
    global user
    user = userName

def getInterval(page = 1):
    '''
    Necessary for pagination
    Intervals viewable on bottom of results pages
    '''
    global pageDict
    # page is greater than 1
    if page > 1:
        # page is a multiple of 5
        if page % 5 == 0:
            # create an interval for each multiple of 5
            pageDict[str(page)] = pageDict[str(page)] = [str(x + page) for x in [int(x) for x in pageDict['1'].copy()]]
            return pageDict[str(page)]
        # page is in first interval
        if page < 5:
            return pageDict[str((page % 5) - page + 1)]
        # page is in intervals past the first
        else:
            multiple_of_five = page - (page % 5)
            # create an interval for multiple_of_five
            pageDict[str(multiple_of_five)] = [str(x + multiple_of_five) for x in [int(x) for x in pageDict['1'].copy()]]
            return pageDict[str(multiple_of_five)]
    else:
        return pageDict['1']


@app.route('/')
def index():
    '''
    Returns Home Page
    '''
    pops= api.getPopular()
    if user in session:
        return render_template('index.html', errors = True, logged_in = True, trend=pops, sidebar= genres, index=True)
    return render_template('index.html', errors = True, logged_in = False, trend=pops, sidebar= genres, index=True)

@app.route('/register')
def register():
    '''
    Returns Registration page if user is not logged in.
    '''
    if user in session:
        return redirect(url_for('index'))
    return render_template('register.html', sidebar=genres, logged_in=False)

@app.route('/login', methods=['POST'])
def login():
    '''
    Returns Login page if user is not logged in.
    '''
    if user in session:
        return redirect(url_for('index'))
    return render_template('login.html', sidebar=genres, address=request.form['address'], logged_in=False)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    '''
    References db and handles authentication and registration.
    '''
    if user in session:
        return redirect(url_for('index'))
    # instantiates DB_Manager with path to DB_FILE
    data = arms.DB_Manager(DB_FILE)
    username, password, curr_page = request.form['username'], request.form['password'], request.form['address']

    # LOGGING IN
    if request.form["submit"] == "Login":
        if username != "" and password != "" and data.verifyUser(username, password):
            session[username] = password
            setUser(username)
            data.save()
            flash('Successfully logged in!')
            return redirect(curr_page)
        # user was found in DB but password did not match
        elif data.findUser(username):
            flash('Incorrect password!')
        # user not found in DB at all
        else:
            flash('Incorrect username!')
        data.save()
        return redirect(curr_page)
    # REGISTERING
    else:
        if len(username.strip()) != 0 and not data.findUser(username):
            if len(password.strip()) != 0:
                # add account to DB
                data.registerUser(username, password)
                data.save()
                #data.setOut()
                flash('Successfully registered account for user  "{}"'.format(username))
                return redirect(url_for('index'))
            else:
                flash('Password length insufficient')
        elif len(username) == 0:
            flash('Username length insufficient')
        else:
            flash('Username already taken!')
        # Try to register again
        return render_template('register.html', errors = True, sidebar=genres)

@app.route('/logout')
def logout():
    '''
    Logs user out if they are logged in
    '''
    curr_page = request.args['address']
    session.pop(user, None)
    setUser(None)
    flash('Successfully logged out!')
    return redirect(curr_page)

@app.route('/local')
def local():
    '''
    Returns Near Me page, displaying cinemas fetched from api.
    '''
    ip= api.getIP()
    zip= api.getZip(ip)
    lat= api.getLat(ip)
    lon= api.getLon(ip)
    try:
        theaterDict = api.send_request()
        theaters= theatherDict['cinemas']
    except:
        #for if there are no theaters near you!
        theaters=[]

    if user in session:
        return render_template("nearby.html", logged_in = True, sidebar= genres,ip=ip,zip=zip,lat=lat,lon=lon,theaters = theaters, count = len(theaters))
    return render_template("nearby.html", logged_in = False, sidebar= genres,ip=ip,zip=zip,lat=lat,lon=lon,theaters = theaters ,count = len(theaters))

@app.route('/profile')
def profile():
    '''
    Generates User profile
    '''
    # instantiates DB_Manager with path to DB_FILE
    data = arms.DB_Manager(DB_FILE)
    movWithComment= data.getMoviesCommentedOn(user)
    movWithVotes= data.getMoviesVotedOn(user)
    movComments= {} #key is movie and value is associated comment
    votedUp=[]
    votedDown=[]

    if len(movWithComment)!=0:
        for movie in movWithComment:
            comments= data.getUserComments(user,movie)
            movComments[movie]= comments

    if len(movWithVotes)!=0:
        for movie in movWithVotes:
            rating = data.getMovieVote(user, movie)
            if rating == 1:
                votedUp.append(movie)
            if rating == -1:
                votedDown.append(movie)
    data.save()
    if user in session:
        name= user
        return render_template("profile.html",name=user,logged_in = True, sidebar= genres,commentDict= movComments, movWithComment=movWithComment, votedUp=votedUp, votedDown=votedDown)
    return redirect(url_for('index'))


@app.route('/page', methods=['GET'])
def page():
    '''
    Route necessary for pagination. Returns the resulting movies given the current page/genre.
    '''
    global pageDict
    interval = request.args['interval']
    genre = request.args['genre']
    intPage = int(request.args['page'])
    page = str(intPage)
    newInterval = getInterval(intPage)
    if intPage - int(interval) > 5:
        return redirect("/categories?interval={0}&page={1}&Submit={2}".format(str(intPage - 1), page, genre))
    elif intPage == 6:
        return redirect("/categories?interval={0}&page={1}&Submit={2}".format(str(intPage - 1), page, genre))
    return redirect("/categories?interval={0}&page={1}&Submit={2}".format(interval, page, genre))



@app.route('/categories',methods=['GET'])
def categories():
    '''
    Retrieves interval for the page and returns category results given some specified genre.
    Note: this route uses the 'GET' method so links can easily be shared amongst users for the different categories
    while still maintaining the robustness of using one template to render a page dedicated to one
    specific category of movies
    '''
    interval = request.args['interval']
    getInterval(int(interval)) # creates interval for this page
    genre = request.args["Submit"]
    page = str(request.args['page'])
    movieDict = api.getMovies(genre, int(page))
    return render_template('category.html',  sidebar=genres, genre=genre, movieDict=movieDict, logged_in = user in session, movieQ=True, curr_page=page, pages=pageDict[interval], notIndex=True)

@app.route('/movie', methods=['POST','GET'])
def movie():
    '''
    Upon access, creates table specific to movie
    Renders movie page from API info
    '''
    movID = request.args["Submit"]
    movDict = api.getMovieDict(movID)
    movieTitle= api.getMovieName(movID)
    movieTrailer = api.getTrailer(movID)
    reviews = api.getReviews(movID)
    simMovie = api.getSimilar(movID)
    data = arms.DB_Manager(DB_FILE)
    data.createMovie(movieTitle)
    movComments= data.getComments(movieTitle)
    voted = data.checkVote(movieTitle, user)
    numVotes = data.getNumVotes(movieTitle)

    if user in session:
        return render_template('movie.html', dict = movDict, sidebar = genres, logged_in= True, comments=movComments, trailer = movieTrailer, review = reviews, mov_id = movID, voted=voted, votes=numVotes,simMovie=simMovie)
    return render_template('movie.html', dict = movDict, sidebar = genres, logged_in= False, comments=movComments, trailer = movieTrailer, review = reviews, mov_id = movID, voted=voted, votes=numVotes, simMovie=simMovie)

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    '''
    Form action to submit a comment. Flashes user on successful comment submission.
    '''
    if user in session:
        data = arms.DB_Manager(DB_FILE)
        comment = request.args['entry']
        id = request.args['Submit']
        title = api.getMovieName(id)
        data.addComment(title, user, comment)
        data.save()
        movComments= data.getComments(title)
        flash('Successfully left a comment!')
        movDict = api.getMovieDict(id)
        movieTrailer = api.getTrailer(id)
        reviews = api.getReviews(id)
        return redirect("/movie?Submit={0}".format(str(id)))
    return redirect(url_for('index'))

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    '''
    Allows user to either downvote or upvote on a movie page.
    '''
    data = arms.DB_Manager(DB_FILE)
    if user in session:
        #creates table of votes if does not already exist
        data.createVoteTable()
        vote=0
        try:
            id = request.args['Submit1']
            vote= 1

        except:
            id = request.args['Submit2']
            vote = -1

        title = api.getMovieName(id)
        data.addVote(title, user, vote)
        data.save()
        movComments= data.getComments(title)
        flash('Successfully left a vote!')
        return redirect("/movie?Submit={0}".format(str(id)))
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    '''
    Search route allows or either Mood results, Im Feeling Lucky result, or a general search query provided in the search bar.
    '''
    if request.args["Submit"] == "Search1":
        entry = request.args['entry'].lower().strip()
        if len(entry.strip()) != 0:
            movieDict = api.searchMovie(entry)
            if len(movieDict) == 0:
                flash("There were no movies with '{0}'!".format(entry))
                return redirect(url_for('index'))
            if user in session:
                return render_template('searchResults.html', entry= entry, logged_in=True, sidebar=genres, movieDict=movieDict, pages=pageDict['1'])
            else:
                return render_template('searchResults.html', entry= entry, logged_in=False, sidebar=genres, movieDict=movieDict, pages=pageDict['1'])
        flash("Please input a movie name!")
        return redirect(url_for('index'))
    #pressing the mood button
    elif request.args["Submit"] == "Search2":
            if user in session:
                return render_template('mood.html', logged_in=True, sidebar=genres)
            else:
                return render_template('mood.html', logged_in=False, sidebar=genres)
    #pressing the I'm feeling lucky button
    elif request.args["Submit"] == "Search3":

        movDict = api.getRandom()
        id = movDict['id']
        if user in session:
            return redirect('/movie?Submit={0}'.format(str(id)))
        else:
            return redirect('/movie?Submit={0}'.format(str(id)))
@app.route('/mood',methods=['POST'])
def mood():
    '''
    Given a certain mood, displays movies only of certain genres.
    '''
    if request.form["submit"] == "Happy":
        family = api.getMovies("Family")
        romantic = api.getMovies("Romance")
        history = api.getMovies("History")
        return render_template('mood.html',mood = "Happy", sidebar=genres, disp = [family,romantic,history])
    if request.form["submit"] == "Sad":
        comedy = api.getMovies("Comedy")
        fantasy = api.getMovies("Fantasy")
        return render_template('mood.html', mood = "Sad", sidebar=genres, disp = [comedy,fantasy])
    if request.form["submit"] == "Stressed":
        animation = api.getMovies("Animation")
        music = api.getMovies("Music")
        action = api.getMovies("Action")
        return render_template('mood.html', mood = "Stressed", sidebar=genres, disp = [animation,music,action])
    if request.form["submit"] == "Bored":
        drama = api.getMovies("Drama")
        crime = api.getMovies("Crime")
        adventure = api.getMovies("Adventure")
        comedy = api.getMovies("Comedy")
        return render_template('mood.html', mood = "Bored",sidebar=genres, disp = [drama,crime,adventure,comedy])

if __name__ == '__main__':
    app.debug = True
    app.run()
