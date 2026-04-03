from rest_framework import serializers
from .models import Review, Favorite, Watchlist


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'tmdb_id', 'media_type', 'title',
                  'rating', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']


class FavoriteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'username', 'tmdb_id', 'media_type', 'title',
                  'poster_path', 'added_at']
        read_only_fields = ['id', 'username', 'added_at']


class WatchlistSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'username', 'tmdb_id', 'media_type', 'title',
                  'poster_path', 'added_at']
        read_only_fields = ['id', 'username', 'added_at']
