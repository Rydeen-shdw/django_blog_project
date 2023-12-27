from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post

from api.serializers.posts_serializers import PostListDetailReadSerializer, PostCreateUpdateSerializer


class PostsListAPIView(APIView):
    def get(self, request: Request) -> Response:
        posts = Post.objects.all()

        per_page = int(request.query_params.get('limit', 10))

        paginator = PageNumberPagination()
        paginator.page_size = per_page
        posts_page = paginator.paginate_queryset(posts, request)

        serializer = PostListDetailReadSerializer(posts_page, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        create_serializer = PostCreateUpdateSerializer(data=request.data)
        if create_serializer.is_valid():
            post = create_serializer.save()
            read_serializer = PostListDetailReadSerializer(post)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostAPIView(APIView):
    def get(self, request: Request, slug: str) -> Response:
        try:
            post = Post.objects.get(slug=slug)
            serializer = PostListDetailReadSerializer(post)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Post.DoesNotExist:
            return Response(
                {"status": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )