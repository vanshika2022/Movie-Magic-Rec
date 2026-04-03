from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Review, Favorite, Watchlist
from .serializers import ReviewSerializer, FavoriteSerializer, WatchlistSerializer
from .tmdb_service import tmdb


# ──────────────────────────────────────
# TMDb proxy endpoints (public)
# ──────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def search_movies(request):
    query = request.query_params.get('query', '')
    page = request.query_params.get('page', 1)
    year = request.query_params.get('year')
    if not query:
        return Response({'error': 'query parameter is required'}, status=400)
    data = tmdb.search_movies(query, page=page, year=year)
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_tv(request):
    query = request.query_params.get('query', '')
    page = request.query_params.get('page', 1)
    if not query:
        return Response({'error': 'query parameter is required'}, status=400)
    data = tmdb.search_tv(query, page=page)
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_multi(request):
    query = request.query_params.get('query', '')
    page = request.query_params.get('page', 1)
    if not query:
        return Response({'error': 'query parameter is required'}, status=400)
    data = tmdb.search_multi(query, page=page)
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, movie_id):
    data = tmdb.get_movie_details(movie_id)
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def tv_detail(request, tv_id):
    data = tmdb.get_tv_details(tv_id)
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def trending(request):
    media_type = request.query_params.get('media_type', 'movie')
    time_window = request.query_params.get('time_window', 'week')
    data = tmdb.get_trending(media_type, time_window)
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def discover_movies(request):
    page = request.query_params.get('page', 1)
    sort_by = request.query_params.get('sort_by', 'popularity.desc')
    genre_id = request.query_params.get('genre')
    year = request.query_params.get('year')
    data = tmdb.discover_movies(page=page, sort_by=sort_by, genre_id=genre_id, year=year)
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def genres(request):
    movie_genres = tmdb.get_movie_genres()
    tv_genres = tmdb.get_tv_genres()
    return Response({'movie': movie_genres['genres'], 'tv': tv_genres['genres']})


@api_view(['GET'])
@permission_classes([AllowAny])
def popular_movies(request):
    page = request.query_params.get('page', 1)
    return Response(tmdb.get_popular_movies(page=page))


@api_view(['GET'])
@permission_classes([AllowAny])
def upcoming_movies(request):
    page = request.query_params.get('page', 1)
    return Response(tmdb.get_upcoming_movies(page=page))


# ──────────────────────────────────────
# Reviews (authenticated)
# ──────────────────────────────────────

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Review.objects.all()
        tmdb_id = self.request.query_params.get('tmdb_id')
        media_type = self.request.query_params.get('media_type')
        if tmdb_id:
            queryset = queryset.filter(tmdb_id=tmdb_id)
        if media_type:
            queryset = queryset.filter(media_type=media_type)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


# ──────────────────────────────────────
# Favorites (authenticated)
# ──────────────────────────────────────

class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, tmdb_id):
    media_type = request.query_params.get('media_type', 'movie')
    deleted, _ = Favorite.objects.filter(
        user=request.user, tmdb_id=tmdb_id, media_type=media_type
    ).delete()
    if deleted:
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Not found'}, status=404)


# ──────────────────────────────────────
# Watchlist (authenticated)
# ──────────────────────────────────────

class WatchlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_watchlist(request, tmdb_id):
    media_type = request.query_params.get('media_type', 'movie')
    deleted, _ = Watchlist.objects.filter(
        user=request.user, tmdb_id=tmdb_id, media_type=media_type
    ).delete()
    if deleted:
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Not found'}, status=404)
