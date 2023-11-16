from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from blog import models
from blog import forms


def post_list_view(request):
    posts = models.Post.published.all()
    return render(request, 'blog/post/post_list.html', {'posts': posts})


def post_detail_view(request, slug):
    post = get_object_or_404(models.Post, slug=slug)
    comments = post.comments.filter(active=True)
    form = forms.CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments,

    }
    return render(request, 'blog/post/post_detail.html', context)


@login_required
@require_http_methods(["POST",])
def post_comment(request, slug):
    post = get_object_or_404(models.Post,
                             slug=slug,
                             status='published')
    comment = None
    user = request.user
    form = forms.CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = user
        comment.save()
    return redirect('blog:post_detail', slug=slug)
