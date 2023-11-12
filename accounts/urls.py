from django.urls import path

from accounts import views

app_name = 'accounts'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.test_view, name='test'),
]
