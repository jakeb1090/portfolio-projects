import requests
from flask import request
from urllib.parse import urlencode
import urllib.parse


# api_version = '3'
# api_base_url = f"https://api.themoviedb.org/{api_version}"
# endpoint_path = f"/movie/{movie_id}"
# endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}"
# print(endpoint)

api_key = '117fc9f739845d5f616af35ae5ab3a47'
api_version = 3
base_url = f"https://api.themoviedb.org/{api_version}"
resource_path = '/tv/airing_today'
endpoint = f"{base_url}{resource_path}?api_key={api_key}&page=1"

class MovieAPI:
    def __init__(self,):
        self.api_key = api_key
        self.api_version = api_version
        self.base_url = base_url
        self.resource_path = resource_path
        self.endpoint = endpoint
        
    def name_to_id(self,name='person'):
        r_path = '/search/person'
        params = {
            'api_key': api_key,
            'language': 'en_US',
            'include_adult': 'true'
        }
        params_encoded = urllib.parse.urlencode(params)
        query = urllib.parse.quote(f"{name}")
        url = f"{base_url}{r_path}?{params_encoded}&query={query}"
        r = requests.get(url)
        _id = r.json()['results'][0]['id']
        return _id
        
    def lookup_id(self, person_id):
        r_path = f"/person/{person_id}"
        url = f"{self.base_url}{r_path}?api_key={self.api_key}"
        r = requests.get(url)
        data = r.json()
        return data
    
    def movie_credits_id(self, person_id):
        r_path = f'/person/{person_id}/movie_credits'
        url = f'{self.base_url}{r_path}?api_key={self.api_key}'
        movies = requests.get(url).json()
        return movies
    
    def person_profile(self, name='person'):
        characters = []
        _id = self.name_to_id(name)
        movies = self.movie_credits_id(_id)
        roles =  movies['cast']
        for r in roles:
            roles = {
                'character': r['character'],
#                 'film': r['title'],
#                 'popularity': r['popularity']
            }
            characters.append(roles)
        df = pd.DataFrame(characters)
#         return df.sort_values(by=['popularity'], ascending=False).head(0)
        return _id
            
    def show_to_id_kor(self, show='name'):
        r_path = '/search/tv'
        params = {
            'api_key': self.api_key,
            'language': 'ko'
        }
        params_encoded = urlencode(params)
        query = urllib.parse.quote(f"{show}")
        url = f"{self.base_url}{r_path}?{params_encoded}&query={query}"
        r = requests.get(url)
        data = r.json()
        items = data['results']
        for item in items:
            if item['original_language'] == 'ko':
                return item['poster_path']
            
            
    def show_to_id(self, show='name'):
        r_path = '/search/tv'
        params = {
            'api_key': self.api_key,
            'language': 'en'
        }
        params_encoded = urlencode(params)
        query = urllib.parse.quote(f"{show}")
        url = f"{self.base_url}{r_path}?{params_encoded}&query={query}"
        r = requests.get(url)
        data = r.json()
        items = data['results']
        for item in items:
            return item['poster_path']
            
    def build_imgurl(self, show):
        imgpath = self.show_to_id(show)
        endpoint = 'https://image.tmdb.org/t/p/w500'
        url = f"{endpoint}{imgpath}"
        return(url)
        print(url)
    
    def build_imgurl_kor(self, show):
        imgpath = self.show_to_id_kor(show)
        endpoint = 'https://image.tmdb.org/t/p/w500'
        url = f"{endpoint}{imgpath}"
        return(url)
        print(url)
        
def number_word(num):
        word = num_word.convert_to_words(urllib.parse.quote(f"{num}"))
        return word
    

        
    

    
    
    
    
