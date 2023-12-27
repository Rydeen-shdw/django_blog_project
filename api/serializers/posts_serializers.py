from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from blog import models

User = get_user_model()


class PostListDetailReadSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    updated = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    publish = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = ('id', 'title', 'slug', 'author', 'body', 'publish',
                  'created', 'updated', 'image_url', 'status', 'category', 'tags')

    def get_author(self, instance):
        return [{'id': instance.author.id,
                 'first_name': instance.author.first_name,
                 'last_name': instance.author.last_name }]

    def get_category(self, instance):
        return [{'id': instance.category.id,
                 'slug': instance.category.slug,
                 'name': instance.category.name}]


class PostCreateUpdateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author_id = serializers.CharField(write_only=True)
    category_id = serializers.CharField(write_only=True)

    class Meta:
        model = models.Post
        fields = ('id', 'title', 'slug', 'author_id', 'body', 'publish',
                  'created', 'updated', 'image_url', 'status', 'category_id', 'tags')

    def create(self, validated_data):
        author_id = validated_data.pop('author_id')
        category_id = validated_data.pop('category_id')
        tags_data = validated_data.pop('tags', [])

        with transaction.atomic():
            try:
                category = models.Category.objects.get(pk=category_id)
            except models.Post.DoesNotExist:
                raise ValidationError({'certification_id': [f'Category with id {category_id} not found.']})

            try:
                author = models.User.objects.get(pk=author_id)
            except models.Post.DoesNotExist:
                raise ValidationError({'certification_id': [f'Author with id {author_id} not found.']})

            post = models.Post.objects.create(category=category, author=author, **validated_data)
            post.tags.set(tags_data)
        return post