from django.urls import path

from api.views import movies_views, accounts_views, posts_views

app_name = 'api'


urlpatterns = [
    # movies
    path('movies/movies/', movies_views.MovieListAPIView.as_view(), name='movies_list'),
    path('accounts/create/', accounts_views.UserCreateAPIView.as_view(), name='register'),
    path('accounts/activate/', accounts_views.ActivateUserAPIView.as_view(),name='activate'),
    path('posts/posts/', posts_views.PostsListAPIView.as_view(), name='posts_list'),
    path('posts/posts/<str:slug>/', posts_views.PostAPIView.as_view(), name='posts')
]
