from django.shortcuts import render

from blog import models


def post_list_view(request):
    posts = models.Post.objects.all()
    return render(request, 'blog/post/post_list.html', {'posts': posts})
