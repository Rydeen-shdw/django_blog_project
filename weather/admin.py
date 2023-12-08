from django.contrib import admin

from weather.models import City, Country, UserCity


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'image', 'lat', 'lon')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('country',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'capital', 'flag')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserCity)
class UserCityAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')
    search_fields = ('city__name', 'user__username')


