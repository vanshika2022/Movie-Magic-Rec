from django.urls import path
from . import views

urlpatterns = [
    # TMDb search & browse
    path('search/movies/', views.search_movies, name='search-movies'),
    path('search/tv/', views.search_tv, name='search-tv'),
    path('search/multi/', views.search_multi, name='search-multi'),

    # TMDb details
    path('movies/<int:movie_id>/', views.movie_detail, name='movie-detail'),
    path('tv/<int:tv_id>/', views.tv_detail, name='tv-detail'),

    # TMDb lists
    path('trending/', views.trending, name='trending'),
    path('discover/', views.discover_movies, name='discover'),
    path('genres/', views.genres, name='genres'),
    path('popular/', views.popular_movies, name='popular'),
    path('upcoming/', views.upcoming_movies, name='upcoming'),

    # Reviews
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),

    # Favorites
    path('favorites/', views.FavoriteListCreateView.as_view(), name='favorite-list'),
    path('favorites/<int:tmdb_id>/', views.remove_favorite, name='remove-favorite'),

    # Watchlist
    path('watchlist/', views.WatchlistListCreateView.as_view(), name='watchlist-list'),
    path('watchlist/<int:tmdb_id>/', views.remove_from_watchlist, name='remove-watchlist'),
]
