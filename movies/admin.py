from django.contrib import admin
from django.utils.safestring import mark_safe

from movies import models


class MovieGenreInline(admin.TabularInline):
    model = models.MovieGenre
    extra = 1


class MovieDirectorInline(admin.TabularInline):
    model = models.MovieDirector
    extra = 1
    raw_id_fields = ('director',)


class MovieStarInline(admin.TabularInline):
    model = models.MovieStar
    extra = 1
    raw_id_fields = ('star',)


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [MovieGenreInline, MovieDirectorInline, MovieStarInline]
    list_display_links = ('pk', 'name')
    list_display = ('pk', 'name', 'year', 'time', 'imdb', 'votes', 'meta_score', 'gross', 'certification', 'get_genres')
    search_fields = ('name', 'description')
    list_filter = ('year', 'certification')
    ordering = ('-pk',)
    list_per_page = 10
    fieldsets = (
        ('Movie', {
            'fields': ('name', 'year', 'time', 'imdb', 'votes', 'meta_score', 'gross', 'description')
        }),
        ('Certification', {
            'fields': ('certification',)
        })
    )

    def get_genres(self, obj):
        genres_html = ", ".join(f"<b>{movie_genre.genre.name}</b>" for movie_genre in obj.movie_genres.all())
        return mark_safe(genres_html)

    get_genres.short_description = 'Genres'
