from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from blog import models
from blog import forms


def post_list_view(request: HttpRequest) -> HttpResponse:
    posts = models.Post.published.all()
    return render(request, 'blog/post/post_list.html', {'posts': posts})


def post_detail_view(request: HttpRequest, post_slug: str) -> HttpResponse:
    post = get_object_or_404(models.Post, slug=post_slug)
    form = forms.CommentForm()
    contex = {
        'post': post,
        'form': form
    }
    return render(request, 'blog/post/post_detail.html', contex)


@login_required
def post_like_view(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(models.Post, pk=post_id)

    if post.is_liked_by(request.user):
        like = post.likes.get(user=request.user)
        like.delete()
    else:
        models.PostLike.objects.create(post=post, user=request.user)
        if post.is_disliked_by(request.user):
            dislike = post.dislikes.get(user=request.user)
            dislike.delete()
    return HttpResponseRedirect(f'{post.get_absolute_url()}#postFooter')


@login_required
def post_dislike_view(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(models.Post, pk=post_id)

    if post.is_disliked_by(request.user):
        dislike = post.dislikes.get(user=request.user)
        dislike.delete()
    else:
        models.PostDislike.objects.create(post=post, user=request.user)
        if post.is_liked_by(request.user):
            like = post.likes.get(user=request.user)
            like.delete()

    return HttpResponseRedirect(f'{post.get_absolute_url()}#postFooter')


@login_required
def comment_like_view(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(models.Comment, pk=comment_id)

    if comment.is_liked_by(request.user):
        like = comment.likes.get(user=request.user)
        like.delete()
    else:
        models.CommentLike.objects.create(comment=comment, user=request.user)
        if comment.is_disliked_by(request.user):
            dislike = comment.dislikes.get(user=request.user)
            dislike.delete()

    return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#commentLike{comment.pk}')


@login_required
def comment_dislike_view(request: HttpRequest, comment_id: int) -> HttpResponse:
    comment = get_object_or_404(models.Comment, pk=comment_id)

    if comment.is_disliked_by(request.user):
        dislike = comment.dislikes.get(user=request.user)
        dislike.delete()
    else:
        models.CommentDislike.objects.create(comment=comment, user=request.user)
        if comment.is_liked_by(request.user):
            like = comment.likes.get(user=request.user)
            like.delete()

    return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#commentLike{comment.pk}')
