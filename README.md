# armRESTs

Robin Han  
Aleksandra Koroza  
Johnny Wong  
pd 8

---------------------  
### Groovy Movie  
Hello and welcome to our project! Our site allows the user to browse through various trending
movies, to leave comments on said movies, and to downvote/upvote as they see fit. The user can also search for specific movies, get recommended movies based on their mood, and get a random movie assigned to them. The user can also see what movies and theaters are available in their locality.

### Instructions for setup:

#### Virtual environment:
- It is important to use a venv because it creates an isolated python environment to run code.  It allows you to
have your dependencies installed exclusively on it, not globally. (you don't need root access!)  This is especially useful if you need to use 2 different versions of a package with 2 pieces of code.

Steps to create a venv:
1. In a terminal, go to the folder in which you want to keep your venv
2. Run `python3 -m venv EXVENV`
   1. We are using EXVENV as the name of the virtual environment; you can use any name you would like
3. Activate your virtual environment by running `source EXVENV/bin/activate`
   1. Your computer's name will now be preceded by (EXVENV).  You are now inside of the virtual environment.
4. Install dependencies (see below)
5. To exit the venv, run `deactivate`
6. You can now activate your virtual environment from any cwd by running `source ~/ROUTE/TO/ENV/EXVENV/bin/activate`

### How to Run:
  Once you have activated your virtual environment:
  1. Install all plugins necessary with: `(venv)$pip install -r <path-to-file>requirements.txt`
  2. Run `python app.py`
  3. Open your localhost and enjoy!

## API information
  There are 4 API's in use to complete this project:

### MovieDB
  - Keys available at this [link] (https://www.themoviedb.org/documentation/api)
  - Used to return trending movies and all of the categories displayed in this project.
  - Movie images, reviews, trailers, and other cool features accessed from this API.

### International Showtimes API
  - Keys available by following steps on this [link](https://www.internationalshowtimes.com/signup.html).(takes a few minutes to process)
  - Used to access movie theaters in the user's area given their location.

### ipStack API
  - A key can be procured by following the steps on this [link](https://ipstack.com/). (sign up for the free plan)
  - API used to return the user's location given their IP.
  - More specifically, we use longitude, latitude, and zipcode.

### ipify API
  - This API does not require a key.
  - Returns the user's IP address.
  - [Here](https://www.ipify.org/) it be.
