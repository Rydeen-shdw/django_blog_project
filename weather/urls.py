from django.urls import path

from weather import views

app_name = 'weather'


urlpatterns = [
    path('today/', views.WeatherCityView.as_view(), name='today'),
    path('user-city/create/', views.UserCityCreateView.as_view(), name='user_city_create'),
    path('user-city/list/', views.UserCityListView.as_view(), name='user_city_list'),
    path('user-city/<slug:slug>/detail/', views.UserCityDetailView.as_view(), name='user_city_detail')
]
