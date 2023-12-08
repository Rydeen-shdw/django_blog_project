from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Country(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200)
    code = models.CharField(max_length=3)
    population = models.IntegerField()
    description = models.TextField()
    flag = models.URLField()
    capital = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Countries'


class City(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    image = models.URLField()
    lat = models.FloatField(verbose_name='latitude')
    lon = models.FloatField(verbose_name='longitude')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='cities')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Cities'
        unique_together = ('lon', 'lat')


class UserCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cities')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='users')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.city}'

    class Meta:
        unique_together = ('user', 'city')
        verbose_name_plural = 'User cities'
