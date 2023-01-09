import tmdbsimple as tmdb
from django.conf import settings

tmdb.API_KEY = settings.TMDB_API_KEY

def search_movie(query: str, page=int):
    search = tmdb.Search()
    response = search.movie(query=query, language="fr", page=page)
    return response

def movie_details(movie_id: int):
    movie = tmdb.Movies(movie_id)
    response = movie.info(language="fr")
    return response