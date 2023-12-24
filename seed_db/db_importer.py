from django.conf import settings
from django.db import transaction
from django.db.models import Q

from seed_db import init_django_orm
from seed_db.csv_mapper import MovieCSVParser
from seed_db.dto import MoviesDTO
from movies import models
from movies.models import Movie


class MovieDataImporter:
    def __init__(self, movies_dto: MoviesDTO):
        self._movies_dto = movies_dto

    def _get_certification_or_create(self, certification_name: str) -> models.Certification:
        certification, _ = models.Certification.objects.get_or_create(name=certification_name)
        return certification

    def _get_genre_or_create(self, genre_name: str) -> models.Genre:
        genre, _ = models.Genre.objects.get_or_create(name=genre_name)
        return genre

    def _get_star_or_create(self, star_name: str) -> models.Star:
        star, _ = models.Star.objects.get_or_create(name=star_name)
        return star

    def _get_director_or_create(self, director_name: str) -> models.Director:
        director, _ = models.Director.objects.get_or_create(name=director_name)
        return director

    @transaction.atomic
    def import_data(self) -> None:
        for movie_dto in self._movies_dto.movies:
            certification = self._get_certification_or_create(movie_dto.certification)
            movie = models.Movie.objects.create(
                name=movie_dto.name,
                year=movie_dto.year,
                time=movie_dto.time,
                imdb=movie_dto.imdb,
                votes=movie_dto.votes,
                meta_score=movie_dto.meta_score,
                gross=movie_dto.gross,
                certification=certification,
                description=movie_dto.description
            )

            for genre_name in movie_dto.genres:
                genre = self._get_genre_or_create(genre_name)
                models.MovieGenre.objects.create(movie=movie, genre=genre)

            for star_name in movie_dto.stars:
                star = self._get_star_or_create(star_name)
                models.MovieStar.objects.create(movie=movie, star=star)

            for director_name in movie_dto.directors:
                director = self._get_director_or_create(director_name)
                models.MovieDirector.objects.create(movie=movie, director=director)


if __name__ == '__main__':
    path_to_movies_file = settings.BASE_DIR / 'seed_db' / 'movies.csv'
    parser = MovieCSVParser(path_to_movies_file)
    movies_dto = parser.read_csv_and_map_to_dto()

    importer = MovieDataImporter(movies_dto)
    importer.import_data()

