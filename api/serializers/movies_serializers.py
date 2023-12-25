from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movies import models


class MovieListReadSerializer(serializers.ModelSerializer):
    certification = serializers.CharField(source='certification.name')
    genres = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = ['id', 'year', 'name', 'imdb', 'certification', 'genres', 'directors']

    def get_genres(self, obj: models.Movie):
        return [{'id': movie_genre.genre.pk, 'name': movie_genre.genre.name}
                for movie_genre in obj.movie_genres.all()]

    def get_directors(self, obj: models.Movie):
        return [{'id': movie_director.director.pk, 'name': movie_director.director.name}
                for movie_director in obj.movie_directors.all()]


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    certification_id = serializers.IntegerField(write_only=True)
    genre_ids = serializers.ListSerializer(child=serializers.IntegerField())
    director_ids = serializers.ListSerializer(child=serializers.IntegerField())
    star_ids = serializers.ListSerializer(child=serializers.IntegerField())

    class Meta:
        model = models.Movie
        fields = ['name', 'year', 'time', 'imdb', 'votes', 'meta_score', 'gross', 'description',
                  'certification_id', 'genre_ids', 'director_ids', 'star_ids']

    def create(self, validated_data):
        certification_id = validated_data.pop('certification_id')
        genre_ids = set(validated_data.pop('genre_ids'))
        director_ids = set(validated_data.pop('director_ids'))
        star_ids = set(validated_data.pop('star_ids'))

        with transaction.atomic():
            try:
                certification = models.Certification.objects.get(pk=certification_id)
            except models.Certification.DoesNotExist:
                raise ValidationError({'certification_id': [f'Certification with id {certification_id} not found.']})

            movie = models.Movie.objects.create(certification=certification, **validated_data)

            for genre_id in genre_ids:
                try:
                    genre = models.Genre.objects.get(pk=genre_id)
                except models.Genre.DoesNotExist:
                    raise ValidationError({'genre_ids': [f'Genre with id {genre_id} not found.']})
                models.MovieGenre.objects.create(movie=movie, genre=genre)

            for director_id in director_ids:
                try:
                    director = models.Director.objects.get(pk=director_id)
                except models.Director.DoesNotExist:
                    raise ValidationError({'director_ids': [f'Director with id {director_id} not found.']})
                models.MovieDirector.objects.create(movie=movie, director=director)

            for star_id in star_ids:
                try:
                    star = models.Star.objects.get(pk=star_id)
                except models.Star.DoesNotExist:
                    raise ValidationError({'star_ids': [f'Star with id {star_id} not found.']})
                models.MovieStar.objects.create(movie=movie, star=star)

            return movie


