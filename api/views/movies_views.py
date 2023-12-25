from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.orderings import MovieOrdering
from api.serializers.movies_serializers import MovieListReadSerializer, MovieCreateUpdateSerializer
from movies.models import Movie


class MovieListAPIView(APIView):
    def get(self, request: Request) -> Response:
        orderings = MovieOrdering.get_ordering_fields(request)
        movies = Movie.objects.all().order_by(*orderings)

        per_page = int(request.query_params.get('limit', 10))

        paginator = PageNumberPagination()
        paginator.page_size = per_page
        movies_page = paginator.paginate_queryset(movies, request)

        serializer = MovieListReadSerializer(movies_page, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        create_serializer = MovieCreateUpdateSerializer(data=request.data)
        if create_serializer.is_valid():
            movie = create_serializer.save()
            read_serializer = MovieListReadSerializer(movie)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
