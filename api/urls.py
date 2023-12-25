from django.urls import path

from api.views import movies_views, accounts_views

app_name = 'api'


urlpatterns = [
    # movies
    path('movies/movies/', movies_views.MovieListAPIView.as_view(), name='movies_list'),
    path('accounts/create/', accounts_views.UserCreatePIView.as_view(), name='register'),
    path('accounts/activate/<str:token>/', accounts_views.ActivateUserAPIView.as_view(), name='activate')
]
