# armRESTs - Robin Han, Aleksandra Koroza, Johnny Wong
# SoftDev1 pd8
# P01: ArRESTed Development

# Used for API access and methods
import json
import urllib.request as request

'''
API HELPERS
'''
#returns loaded response
def fetchInfo(url):
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
movURL="https://api.themoviedb.org/3/trending/all/day?api_key="
movKey= "95e69e7f8882e106d7cf82de25f6a422"

#get currently popular movies
def getPopular():
    movInfo= fetchInfo(movURL+movKey)
    return movInfo['results'];
    #pops= movInfo['results'][0]['original_title']
    #return pops
