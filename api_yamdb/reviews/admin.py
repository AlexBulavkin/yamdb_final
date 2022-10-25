from django.contrib import admin

from .models import Category, Genre, Title, GenreTitle, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    """Отражение модели Category в админке."""
    list_display = ('id', 'name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    """Отражение модели Genre в админке."""
    list_display = ('id', 'name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    """Отражение модели Title в админке."""
    list_display = ('id', 'name', 'year', 'description',
                    'rating', 'category')


class GenreTitleAdmin(admin.ModelAdmin):
    """Отражение модели GenreTitle в админке."""
    list_display = ('id', 'genre', 'title')


class ReviewAdmin(admin.ModelAdmin):
    """Отражение модели Review в админке."""
    list_display = ('id', 'title', 'text', 'author',
                    'score', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    """Отражение модели Comment в админке."""
    list_display = ('id', 'review', 'text', 'author',
                    'pub_date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
