# Generated by Django 4.2.7 on 2023-12-05 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200)),
                ('code', models.CharField(max_length=3)),
                ('population', models.IntegerField()),
                ('description', models.TimeField()),
                ('flag', models.URLField()),
                ('capital', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200)),
                ('description', models.TimeField()),
                ('image', models.URLField()),
                ('lat', models.FloatField(verbose_name='latitude')),
                ('lon', models.FloatField(verbose_name='longitude')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cities', to='weather.country')),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'ordering': ('name',),
                'unique_together': {('lon', 'lat')},
            },
        ),
        migrations.CreateModel(
            name='UserCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='weather.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User cities',
                'unique_together': {('user', 'city')},
            },
        ),
    ]
