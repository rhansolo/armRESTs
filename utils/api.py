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
    key = "95e69e7f8882e106d7cf82de25f6a422"
    return fetchInfo(url.format(str(id), key))

def getMovieName(id):
    dict= getMovieDict(id)
    return dict['title']

def getPopular():
    ''' Getting trending movies '''
    movURL=" https://api.themoviedb.org/3/movie/popular?api_key="
    movKey= "95e69e7f8882e106d7cf82de25f6a422"
    movLang="&language=en-US&page=1"
    movInfo= fetchInfo(movURL+movKey+movLang)
    return movInfo['results'];

def getGenres():
    ''' Getting all possible genres '''
    genURL="https://api.themoviedb.org/3/genre/movie/list?api_key=95e69e7f8882e106d7cf82de25f6a422&language=en-US"
    genInfo= fetchInfo(genURL)
    return genInfo['genres']

GENRES = getGenres()

def getMovies(genre):
    ''' Getting all movies given genre '''
    search_for_genre = [x for x in GENRES if x['name'] == genre][0]
    genre_id = search_for_genre['id']
    genURL = "https://api.themoviedb.org/3/discover/movie?api_key=95e69e7f8882e106d7cf82de25f6a422&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={0}".format(genre_id)
    genInfo = fetchInfo(genURL)
    return genInfo['results']

def searchMovie(keyword, page = '1'):
    '''Getting all movies given keyword'''
    word = keyword
    # fix space issue in keyword
    keywordURL = "https://api.themoviedb.org/3/search/movie?api_key=95e69e7f8882e106d7cf82de25f6a422&language=en-US&query={0}&page={1}&include_adult=false".format(word.replace(" ", "%20"), page)
    return fetchInfo(keywordURL)['results']

def getRandom():
    year = random.randint(2000,2018)
    num = random.randint(0,19)
    movURL = "https://api.themoviedb.org/3/discover/movie?api_key=95e69e7f8882e106d7cf82de25f6a422&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=true&page=1&year=" + str(year)
    page = random.randint(1,8)
    newMovUrl = "https://api.themoviedb.org/3/discover/movie?api_key=95e69e7f8882e106d7cf82de25f6a422&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=true&page=" + str(page) + "&year=" + str(year)
    id = fetchInfo(newMovUrl)['results'][num]['id']
    return getMovieDict(str(id))

def getTrailer(id):
    movURL = "https://api.themoviedb.org/3/movie/"
    movRest ="/videos?api_key=95e69e7f8882e106d7cf82de25f6a422&language=en-US"
    genInfo = fetchInfo(movURL + str(id) + movRest)
    key = genInfo['results'][0]['key']
    link =  "https://www.youtube.com/embed/" + str(key)
    return link
def getReviews(id):
    movURL =  "https://api.themoviedb.org/3/movie/"
    movRest = "/reviews?api_key=95e69e7f8882e106d7cf82de25f6a422&language=en-US&page=1"
    genInfo = fetchInfo(movURL + str(id) + movRest)
    return genInfo['results']
'''
International Showtimes API
Aleksandra's API key:  h54sMq1Q8UinW1K91Ts3fxPJ34CYMQAC
documentation: https://api.internationalshowtimes.com/documentation/v4/#Authentication
'''
def send_request():
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/",
            params={
                #"countries": "US",
                "location": "40.72,-73.85",
                "distance": "30",
            },
            headers={
                "X-API-Key": "h54sMq1Q8UinW1K91Ts3fxPJ34CYMQAC",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
        print("it works")
    except:
        print('HTTP Request failed')
