from django.urls import path

from blog import views

app_name = 'blog'


urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/comment/', views.post_comment, name='post_comment')
]
