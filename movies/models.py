from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Star(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Certification(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=250)
    year = models.IntegerField()
    time = models.IntegerField()
    imdb = models.FloatField()
    votes = models.IntegerField()
    meta_score = models.FloatField(null=True, blank=True)
    gross = models.FloatField(null=True, blank=True)
    certification = models.ForeignKey(Certification, on_delete=models.PROTECT, related_name='movies')
    description = models.TextField()

    class Meta:
        ordering = ('name', 'year', 'time')
        indexes = (
            models.Index(fields=('name', 'year', 'time')),
        )

    def __str__(self):
        return f'{self.name} ({self.year})'


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genre_movies')

    class Meta:
        unique_together = ('movie', 'genre')

    def __str__(self):
        return f'{self.movie} - {self.genre}'


class MovieDirector(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_directors')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='director_movies')

    class Meta:
        unique_together = ('movie', 'director')

    def __str__(self):
        return f'{self.movie} - {self.director}'


class MovieStar(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_stars')
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name='star_movies')

    class Meta:
        unique_together = ('movie', 'star')

    def __str__(self):
        return f'{self.movie} - {self.star}'

