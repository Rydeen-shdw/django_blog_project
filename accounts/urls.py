from django.urls import path

from accounts import views

app_name = 'accounts'


urlpatterns = [
    # user account
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('activate/<str:username>/<str:token>/', views.activate_account_view, name='activate'),
    path('password_change/<str:username>/', views.change_password_view, name='password_change'),
    # user profile
    path('profile/create/', views.profile_create_view, name='profile_create'),
    path('profile/<str:username>/detail/', views.profile_detail_view, name='profile_detail'),
    path('profile/<str:username>/update/', views.profile_update_view, name='profile_update'),
    # user follow system
    path('profile/follow/<str:username>/', views.user_follow_view, name='follow_user'),
    path('profile/unfollow/<str:username>/', views.user_unfollow_view, name='unfollow_user'),
    path('profile/<str:username>/followers/', views.user_followers_view, name='followers'),
    path('profile/<str:username>/following/', views.user_following_view, name='following')
]
