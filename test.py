import requests
from pprint import pprint
import urllib.parse


#MB_endpoint_TWO = "https://api.themoviedb.org/3/search/movie?api_key=9149b2f73b90782e603b46258102edd0&language=en-US&query=https%3A%2F%2Fapi.themoviedb.org%2F3%2Fmovie%2FAnt-Man%3F&page=1&include_adult=false"


class MoviesApiDb():

    def __init__(self):

        #Key
        self.MB_API_KEY = "9149b2f73b90782e603b46258102edd0"

    def get_movie_info(self, movie_name):

        self.movie_name = movie_name

        MB_endpoint_ONE = "https://api.themoviedb.org/3/search/movie?"
        parameters = {

            'api_key': self.MB_API_KEY,
            'language': 'en_US',
            'query': self.movie_name,
            'page': 1,

        }

        response = requests.get(MB_endpoint_ONE, params=parameters)
        response.raise_for_status()
        data = response.json()

        return data

    def get_movie_details(self, movie_id):

        self.movie_id = movie_id

        MB_endpoint_TWO = f"https://api.themoviedb.org/3/movie/{self.movie_id}?"
        parameters = {

            'api_key': self.MB_API_KEY,
            #'movie_id': self.movie_id,
            #'language': 'en-US'

        }

        response = requests.get(MB_endpoint_TWO, params=parameters)
        response.raise_for_status()
        data = response.json()

        return data







#634649


#start = MoviesApiDb()
#mid = start.get_movie_info('the matrix')['results'][0]['id']
#pprint(mid)

#result = start.get_movie_details(mid)
#print(result['original_title'])







#print(f"{result['original_title']}\n{result['poster_path']}\n{result['release_date']}\n{result['overview']}")

#for index, item in enumerate(result):
#    print(item)
#    #print(f"{item['original_title']}\n{item['release_date']}\n{item['overview']}\n{item['vote_average']}\n{item['popularity']}\n{item['poster_path']}")