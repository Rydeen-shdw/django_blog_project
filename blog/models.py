from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager
from django.db import models
from django.utils import timezone

from blog.managers import PublishedManager

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    body = models.TextField(verbose_name='Content')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=250, null=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='posts')
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-created', '-updated')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.slug])

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def is_disliked_by(self, user):
        return self.dislikes.filter(user=user).exists()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} on post {self.post.title}'


class PostDislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_dislikes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} on post {self.post.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.author} - {self.body}'

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def is_disliked_by(self, user):
        return self.dislikes.filter(user=user).exists()


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f'{self.user} like on comment {self.comment.body}'


class CommentDislike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_dislikes')

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f'{self.user} dislike on comment {self.comment.body}'


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"

