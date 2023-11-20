from django.urls import path

from accounts import views

app_name = 'accounts'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('activate/<str:username>/<str:token>/', views.activate_account_view, name='activate'),
    path('<str:username>/', views.profile_view, name='profile'),
    path('edit/<str:username>/', views.profile_edit_view, name='profile_edit'),
]
