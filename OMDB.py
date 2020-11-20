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
def get_movie_data(mov_str):
    baseUrl = "http://www.omdbapi.com/"
    param_dict = {"t" : mov_str, "r" : "json"}
    omdb_obj = requests_with_caching.get(baseUrl, params = param_dict)
    print(omdb_obj.url)
    return omdb_obj.json()

def get_movie_rating(movie_dict):
    rotten_tomato_rating = 0
    temp = dict()
    for temp in movie_dict["Ratings"]:
        if "Rotten Tomatoes" in temp["Source"]:
            rotten_tomato_rating = int(temp["Value"].strip("%"))
    return rotten_tomato_rating

def get_sorted_recommendations(movie_lst):
    movie_dict = dict()
    movie_final = list()
    m_lst = list()
    m_lst = get_related_titles(movie_lst)
    for m in m_lst:
        rt = get_movie_rating(get_movie_data(m))
        movie_dict[m] = rt
    #Ratings should be in decreasing order, movies should be in reverse alphabetical order
    temp_dict = sorted(movie_dict.items(), key = lambda x: (x[1],x[0]), reverse= True)
    for i in temp_dict:
        movie_final.append(i[0])
    return movie_final
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages

get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

