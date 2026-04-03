import requests
from django.conf import settings


class TMDbService:
    """Service layer for interacting with The Movie Database API."""

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    # --- Search ---
    def search_movies(self, query, page=1, year=None):
        params = {'query': query, 'page': page}
        if year:
            params['year'] = year
        return self._get('/search/movie', params)

    def search_tv(self, query, page=1):
        params = {'query': query, 'page': page}
        return self._get('/search/tv', params)

    def search_multi(self, query, page=1):
        params = {'query': query, 'page': page}
        return self._get('/search/multi', params)

    # --- Details ---
    def get_movie_details(self, movie_id):
        return self._get(f'/movie/{movie_id}', {'append_to_response': 'credits,videos,similar'})

    def get_tv_details(self, tv_id):
        return self._get(f'/tv/{tv_id}', {'append_to_response': 'credits,videos,similar'})

    # --- Trending ---
    def get_trending(self, media_type='movie', time_window='week'):
        return self._get(f'/trending/{media_type}/{time_window}')

    # --- Discover (filtered browsing) ---
    def discover_movies(self, page=1, sort_by='popularity.desc', genre_id=None, year=None):
        params = {'page': page, 'sort_by': sort_by}
        if genre_id:
            params['with_genres'] = genre_id
        if year:
            params['primary_release_year'] = year
        return self._get('/discover/movie', params)

    def discover_tv(self, page=1, sort_by='popularity.desc', genre_id=None):
        params = {'page': page, 'sort_by': sort_by}
        if genre_id:
            params['with_genres'] = genre_id
        return self._get('/discover/tv', params)

    # --- Genres ---
    def get_movie_genres(self):
        return self._get('/genre/movie/list')

    def get_tv_genres(self):
        return self._get('/genre/tv/list')

    # --- Popular / Top Rated / Upcoming ---
    def get_popular_movies(self, page=1):
        return self._get('/movie/popular', {'page': page})

    def get_top_rated_movies(self, page=1):
        return self._get('/movie/top_rated', {'page': page})

    def get_upcoming_movies(self, page=1):
        return self._get('/movie/upcoming', {'page': page})

    def get_now_playing(self, page=1):
        return self._get('/movie/now_playing', {'page': page})


tmdb = TMDbService()
