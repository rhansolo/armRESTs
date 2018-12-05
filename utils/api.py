# armRESTs - Robin Han, Aleksandra Koroza, Johnny Wong
# SoftDev1 pd8
# P01: ArRESTed Development

# Used for API access and methods
import json
import random
import requests
import urllib.request as request

from urllib.request import Request

'''
LIST OF KEYS
'''
key0 = open('utils/key0.txt', 'r')
key1 = open('utils/key1.txt', 'r')
key2 = open('utils/key2.txt', 'r')
movieDB_key = key0.readline().strip()
showtimes_key = key1.readline().strip()
ipStack_key = key2.readline().strip()
key0.close()
key1.close()
key2.close()


'''
API HELPERS
'''

def fetchInfo(url):
    ''' Returns loaded response '''
    response = request.urlopen(url)
    response = response.read()
    info = json.loads(response)
    return info


'''
MovieDB
Aleksandra's API key (v3 auth)= 95e69e7f8882e106d7cf82de25f6a422
(v4 auth)= eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5NWU2OWU3Zjg4ODJlMTA2ZDdjZjgyZGUyNWY2YTQyMiIsInN1YiI6IjViZmNiYmNmYzNhMzY4NWMzNzAxZWJjYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.QlJW54t6fGCvuAQNjp4_1H8kRod3DDWBBtv93Sa5VsU
remember that it's 40 requests per 10 sec
examples: https://www.themoviedb.org/documentation/api/discover
/discover/movie?sort_by=popularity.desc for popular movies ?
'''


def getMovieDict(id):
    ''' Getting entire associated movie dictionary '''
    url = "https://api.themoviedb.org/3/movie/{0}?api_key={1}"
    return fetchInfo(url.format(str(id), movieDB_key))

def getMovieName(id):
    dict= getMovieDict(id)
    return dict['title']

def getPopular():
    ''' Getting trending movies '''
    movURL=" https://api.themoviedb.org/3/movie/popular?api_key={0}&language=en-US&page=1"
    movInfo= fetchInfo(movURL.format(movieDB_key))
    return movInfo['results'];

def getGenres():
    ''' Getting all possible genres '''
    genURL="https://api.themoviedb.org/3/genre/movie/list?api_key={0}&language=en-US"
    genInfo= fetchInfo(genURL.format(movieDB_key))
    return genInfo['genres']

GENRES = getGenres()

def getMovies(genre):
    ''' Getting all movies given genre '''
    search_for_genre = [x for x in GENRES if x['name'] == genre][0]
    genre_id = search_for_genre['id']
    genURL = "https://api.themoviedb.org/3/discover/movie?api_key={0}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={1}".format(movieDB_key,genre_id)
    genInfo = fetchInfo(genURL)
    return genInfo['results']

def searchMovie(keyword, page = '1'):
    '''Getting all movies given keyword'''
    word = keyword
    # fix space issue in keyword
    keywordURL = "https://api.themoviedb.org/3/search/movie?api_key={0}&language=en-US&query={1}&page={2}&include_adult=false".format(movieDB_key, word.replace(" ", "%20"), page)
    return fetchInfo(keywordURL)['results']

def getRandom():
    year = random.randint(2000,2018)
    num = random.randint(0,19)
    movURL = "https://api.themoviedb.org/3/discover/movie?api_key={0}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=true&page=1&year={1}".format(movieDB_key, str(year))
    page = random.randint(1,8)
    newMovUrl = "https://api.themoviedb.org/3/discover/movie?api_key={0}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=true&page=".format(movieDB_key) + str(page) + "&year=" + str(year)
    id = fetchInfo(newMovUrl)['results'][num]['id']
    return getMovieDict(str(id))

def getTrailer(id):
    movURL = "https://api.themoviedb.org/3/movie/"
    movRest ="/videos?api_key={0}&language=en-US".format(movieDB_key)
    genInfo = fetchInfo(movURL + str(id) + movRest)
    key = genInfo['results'][0]['key']
    link =  "https://www.youtube.com/embed/" + str(key)
    return link
def getReviews(id):
    movURL =  "https://api.themoviedb.org/3/movie/"
    movRest = "/reviews?api_key={0}&language=en-US&page=1".format(movieDB_key)
    genInfo = fetchInfo(movURL + str(id) + movRest)
    return genInfo['results']

'''
International Showtimes API
Aleksandra's API key:  h54sMq1Q8UinW1K91Ts3fxPJ34CYMQAC
documentation: https://api.internationalshowtimes.com/documentation/v4/#Authentication
'''

#this API required some header shenanigans
def send_request():
    #try:
        IP = getIP()
        longitude = getLon(IP)
        latitude = getLat(IP)
        loc = str(latitude) + "," + str(longitude)
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/",
            params={
                #"countries": "US",
                #"location": "40.72,-73.86",
                "location": loc,
                # distance is measured in kilometers
                "distance": "20",

            },
            headers={
                "X-API-Key": "{0}".format(showtimes_key),
            },
        )

        #print('Response HTTP Status Code: {status_code}'.format(
        #    status_code=response.status_code))
        #print('Response HTTP Response Body: {content}'.format(
        #    content=response.content))
        content= response.json()
        #print(content)
        #print(response.url)
        #print("it works")
    #except:
        #print('HTTP Request failed')
        return content
def getTheater():
    pass

'''
ipStack API
Aleksandra's API key:  5eccde7ed4a5f5de86b6c688b239d7c2
documentation: https://ipstack.com/quickstart
https://ipstack.com/documentation
'''
ipStackURL= "http://api.ipstack.com/"

def getZip(IP):
    try:
        locInfo= fetchInfo(ipStackURL+IP+"?access_key="+ipStack_key)
        return locInfo["zip"]
    except:
        print("no zip")

def getLat(IP):
    try:
        locInfo= fetchInfo(ipStackURL+IP+"?access_key="+ipStack_key)
        return locInfo["latitude"]
    except:
        print("no lat")

def getLon(IP):
    try:
        locInfo= fetchInfo(ipStackURL+IP+"?access_key="+ipStack_key)
        return locInfo["longitude"]
    except:
        print("no lon")

'''
ipify API
Does not require API key; very nice and simple
info: https://www.ipify.org/
'''

def getIP():
    try:
        IPURL= "https://api.ipify.org?format=json"
        ipInfo= fetchInfo(IPURL)
        return ipInfo['ip']
    except:
        print("no ip")
