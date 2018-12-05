# armRESTs - Robin Han, Aleksandra Koroza, Johnny Wong
# SoftDev1 pd8
# P01: ArRESTed Development

import sqlite3   # enable control of an sqlite database

class DB_Manager:
    '''
    HOW TO USE:
    Every method openDB by connecting to the inputted path of
    a database file. After performing all operations on the
    database, the instance of the DB_Manager must save using
    the save method.
    The operations/methods can be found below. DB_Manager
    has been custom fit to work with
    P01: ArRESTed Development
    '''
    def __init__(self, dbfile):
        '''
        SET UP TO READ/WRITE TO DB FILES
        '''
        self.DB_FILE = dbfile
        self.db = None
    #========================HELPER FXNS=======================
    def openDB(self):
        '''
        OPENS DB_FILE AND RETURNS A CURSOR FOR IT
        '''
        self.db = sqlite3.connect(self.DB_FILE) # open if file exists, otherwise create
        return self.db.cursor()

    def tableCreator(self, tableName, col0, col1, col2):
        '''
        CREATES A 3 COLUMN TABLE IF tableName NOT TAKEN
        ALL PARAMS ARE STRINGS
        '''
        c = self.openDB()
        if not self.isInDB(tableName):
            command = 'CREATE TABLE "{0}"({1}, {2}, {3});'.format(tableName, col0, col1, col2)
            c.execute(command)


    def insertRow(self, tableName, data):
       '''
         APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
         @tableName is the name the table being written to
         @data is a tuple containing data to be entered
       '''
       c = self.openDB()
       command = 'INSERT INTO "{0}" VALUES(?, ?, ?)'
       c.execute(command.format(tableName), data)


    def isInDB(self, tableName):
        '''
        RETURNS True IF THE tableName IS IN THE DATABASE
        RETURNS False OTHERWISE
        '''
        c = self.openDB()
        command = 'SELECT * FROM sqlite_master WHERE type = "table"'
        c.execute(command)
        selectedVal = c.fetchall()
        # list comprehensions -- fetch all tableNames and store in a set
        tableNames = set([x[1] for x in selectedVal])

        return tableName in tableNames

    def table(self, tableName):
        '''
        PRINTS OUT ALL ROWS OF INPUT tableName
        '''
        c = self.openDB()
        command = 'SELECT * FROM "{0}"'.format(tableName)
        c.execute(command)
        print(c.fetchall())


    def save(self):
        '''
        COMMITS CHANGES TO DATABASE AND CLOSES THE FILE
        '''
        self.db.commit()
        self.db.close()
    #========================HELPER FXNS=======================

    #======================== DB FXNS =========================
    def getUsers(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT users AND CORRESPONDING PASSWORDS
        '''
        c = self.openDB()
        command = 'SELECT user_name, passwords FROM users'
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def get_user_ids(self, storyTitle):
        '''
        RETURNS SET OF user_ids CONTRIBUTED TO storyTitle
        '''
        c = self.openDB()
        command = 'SELECT user_id FROM "{0}"'.format(storyTitle)
        c.execute(command)
        ids = set(x[0] for x in c.fetchall())
        return ids

    def registerUser(self, userName, password):
        '''
        ADDS user TO DATABASE
        '''
        c = self.openDB()
        command = 'SELECT user_id FROM users WHERE user_id = (SELECT max(user_id) FROM users)'
        c.execute(command)
        selectedVal = c.fetchone()
        max_id = 0
        if selectedVal != None:
            max_id = selectedVal[0]
        else:
            max_id = 0
            # userName is already in database -- do not continue to add
        if self.findUser(userName):
            return False
        # userName not in database -- continue to add
        else:
            row = (userName, password, max_id + 1)
            self.insertRow('users', row)
            return True

    def findUser(self, userName):
        '''
        CHECKS IF userName IS UNIQUE
        '''
        return userName in self.getUsers()

    def verifyUser(self, userName, password):
        '''
        CHECKS IF userName AND password MATCH THOSE FOUND IN DATABASE
        '''
        c = self.openDB()
        command = 'SELECT user_name, passwords FROM users WHERE user_name = "{0}"'.format(userName)
        c.execute(command)
        selectedVal = c.fetchone()
        if selectedVal == None:
            return False
        if userName == selectedVal[0] and password == selectedVal[1]:
            return True
        return False

    def getID_fromUser(self, userName):
        '''
        RETURNS user_id OF userName
        '''
        c = self.openDB()
        command = 'SELECT user_id FROM users WHERE user_name == "{0}"'.format(userName)
        c.execute(command)
        id = c.fetchone()[0]
        return id
    '''
    Look at story stuff for reference...
    use it for movies instead
    '''
    #==========================Start of movie fxns==========================
    def createMovie(self, movieTitle):
        '''
         cREATES TABLE OF movieTitle IF movieTitle IS UNIQUE(NOT FOUND IN DATABASE)
         Each movie table used to store comments
        '''
        if not self.findMovie(movieTitle):
            self.tableCreator(movieTitle, 'movie_title text', 'user text', 'comment text')
            return True
        return False

    def addComment(self, movieTitle, user, comment):
        '''
        ADD comment TO movieTitle's TABLE TO DATABASE
        user can comment more than once
        movietitle field redundant, (can be replaced with time of comment)
        '''
        row=(movieTitle,user,comment)
        self.insertRow(movieTitle, row)
        return True

    def findMovie(self, movieTitle):
        '''
        Checks if movieTitle is unique
        '''
        movieTitles = self.getMovies()
        return movieTitle in movieTitles

    def getMovies(self):
        '''
        RETURNS A SET CONTAINING ALL CURRENT movieTitles
        '''
        c = self.openDB()
        command = 'SELECT * FROM sqlite_master WHERE type = "table"'
        c.execute(command)
        selectedVal = c.fetchall()
        # list comprehensions -- fetch all movieTitles and store in a set
        movieTitles = set([x[1] for x in selectedVal if x[3] > 2 and x[1] != 'votes'])
        return movieTitles

    def getComments(self, movieTitle):
        '''
        RETURNS A SET CONTAINING ALL CURRENT movieComments for a specific movie
        '''
        c = self.openDB()
        command = 'SELECT comment, user FROM "{0}"'.format(movieTitle)
        c.execute(command)
        selectedVal = c.fetchall()
        movieComments = set(selectedVal)
        return movieComments

    def getMoviesCommentedOn(self, user):
        '''
        Returns a set containg all current movieTitles user has commented on
        '''
        c = self.openDB()
        movieSet = set()
        for movie in self.getMovies():
            command = 'SELECT movie_title FROM "{0}" WHERE user = "{1}";'.format(movie, user)
            c.execute(command)
            selectedVal = c.fetchone()
            if selectedVal != None:
                movieSet.add(movie)
        return movieSet

    def getUserComments(self, user, movie):
        '''
        Returns a set of comments left by a particular user on a particular movie
        '''
        c = self.openDB()
        commentSet = set()
        command = 'SELECT comment FROM "{0}" WHERE user = "{1}";'.format(movie, user)
        c.execute(command)
        selectedVal = c.fetchall()
        for comment in selectedVal:
            commentSet.add(comment[0])
        return commentSet

    def getMoviesVotedOn(self,user):
        '''
        Returns a set containing all current movieTitles user has voted on
        '''
        c = self.openDB()
        movieSet = set()
        for movie in self.getMovies():
            command = 'SELECT movie_title FROM votes WHERE user = "{0}";'.format(user)
            c.execute(command)
            selectedVal = c.fetchone()
            if selectedVal != None:
                movieSet.add(movie)
        return movieSet

    def getMovieVote(self, user, movie):
        '''
        Returns 1 if the user upvoted the movie
        Returns -1 if the user downvoted the movie
        Returns 0 if the user has not voted on the movie
        '''
        c = self.openDB()
        command = 'SELECT rate FROM votes WHERE user = "{0}" and movie_title = "{1}";'.format(user,movie)
        c.execute(command)
        selectedVal = c.fetchall()
        if len(selectedVal) > 0:
            return selectedVal[0][0]
        return 0



    #==========================End of movie fxns==========================
    #==========================Start of vote fxns==========================

    def createVoteTable(self):
        '''
        #cREATES TABLE OF votes IF votes IS UNIQUE(NOT FOUND IN DATABASE)
        #Used to store upvote/downvote information for each movie
        '''
        self.tableCreator('votes', 'movie_title text', 'user text', 'rate integer')
        return True

    def addVote(self, movieTitle, user, vote):
        '''
        ADD vote TO movieTitle's TABLE TO DATABASE
        users can upvote or downvote
        '''
        row=(movieTitle,user,vote)
        self.insertRow('votes', row)
        return True

    def getNumVotes(self, movieTitle):
        '''
        RETURNS NUMBER OF VOTES FOR INPUT movieTitle
        '''
        c = self.openDB()
        command = 'SELECT rate FROM votes WHERE movie_title == "{0}"'.format(movieTitle)
        c.execute(command)
        selectedVal = c.fetchall()
        print('selected val: ' + str(selectedVal))
        sum = 0
        for i in selectedVal:
            sum += i[0]
        return sum


    def checkVote(self, movieTitle, user):
        '''
        Checks whether user has voted on a particular movie
        '''
        c = self.openDB()
        command = 'SELECT user, movie_title FROM votes WHERE user == "{0}" and movie_title == "{1}"'.format(user, movieTitle)
        c.execute(command)
        selectedVal = c.fetchone()
        print(selectedVal)
        return selectedVal != None

    def getRating(self,movieTitle):
        pass


    #======================== DB FXNS =========================
#======================== END OF CLASS DB_Manager =========================
