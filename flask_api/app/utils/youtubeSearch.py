import json
from youtube_search import YoutubeSearch

'''
    Searching through the YouTube via a given keyword

    :param: (str) key - the given keyword
    :param: (number) max_results - maximum number of desired results
'''
def searchByKey(key, max_results = 10):

    results = YoutubeSearch(key, max_results = max_results).to_json()
    return json.loads(results)
