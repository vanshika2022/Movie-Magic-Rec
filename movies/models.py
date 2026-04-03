from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    tmdb_id = models.IntegerField(help_text="TMDb movie or TV show ID")
    media_type = models.CharField(
        max_length=10,
        choices=[('movie', 'Movie'), ('tv', 'TV Show')],
        default='movie',
    )
    title = models.CharField(max_length=255, help_text="Movie/show title for display")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating from 1 to 10",
    )
    content = models.TextField(help_text="Review text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tmdb_id', 'media_type')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.rating}/10)"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tmdb_id = models.IntegerField()
    media_type = models.CharField(
        max_length=10,
        choices=[('movie', 'Movie'), ('tv', 'TV Show')],
        default='movie',
    )
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tmdb_id', 'media_type')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    tmdb_id = models.IntegerField()
    media_type = models.CharField(
        max_length=10,
        choices=[('movie', 'Movie'), ('tv', 'TV Show')],
        default='movie',
    )
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tmdb_id', 'media_type')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.title} (watchlist)"
