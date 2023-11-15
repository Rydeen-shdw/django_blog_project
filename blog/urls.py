from django.urls import path

from blog import views

app_name = 'blog'


urlpatterns = [
    path('', views.post_list_view, name='post_list'),
]
