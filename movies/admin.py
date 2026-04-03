from django.contrib import admin
from .models import Review, Favorite, Watchlist

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'media_type', 'rating', 'created_at']
    list_filter = ['media_type', 'rating']
    search_fields = ['title', 'user__username']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'media_type', 'added_at']
    list_filter = ['media_type']

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'media_type', 'added_at']
    list_filter = ['media_type']
