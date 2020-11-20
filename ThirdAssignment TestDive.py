import json
import requests_with_caching
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
def get_movies_from_tastedive(movie_str):
    baseUrl = "https://tastedive.com/api/similar"
    params_dict = {"q": movie_str, "type": "movies", "limit": 5}
    tastedive_resp = requests_with_caching.get(baseUrl,params = params_dict)
    print(tastedive_resp.url)
    return tastedive_resp.json()
def extract_movie_titles(diction):
    a = dict()
    ls = list()
    a = diction["Similar"]["Results"]
    di = {}
    for di in a:
        ls.append(di["Name"])
    return ls
def get_related_titles(lst):
    master_lst = list()
    a = dict()
    for l in lst:
        a = get_movies_from_tastedive(l)
        temp1 = extract_movie_titles(a) 
        [master_lst.append(x) for x in temp1 if x not in master_lst]
    return master_lst
get_related_titles(["Black Panther", "Captain Marvel"])
get_related_titles([])

