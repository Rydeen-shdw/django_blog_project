from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.conf import settings

from accounts import forms
from accounts import models
from blog.models import Post, Follow
from accounts.utils import send_activation_email

User = get_user_model()


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already register.')
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user_token = models.ActivateToken.objects.create(user=user)
            send_activation_email(user, user_token, settings.EMAIL_HOST_USER, request)
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})

    form = forms.RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["GET"])
def activate_account_view(request, username, token):
    user = get_object_or_404(User, username=username)
    token = get_object_or_404(models.ActivateToken, token=token, user=user)

    if user.is_active:
        messages.error(request, 'User is already activated.')
        return redirect('blog:post_list')

    if token.verify_token():
        user.is_active = True
        token.delete()
        user.save()

        messages.success(request, 'Activation complete.')
        return redirect('accounts:login')

    messages.error(request, 'Token expired')
    return redirect('accounts:test')


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(request, email=email, password=password)

            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 7)

            if user:
                login(request, user)
                next_url = request.GET.get('next', 'blog:post_list')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid form data')
            return render(request, 'accounts/login.html', {'form': form})

    form = forms.LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["GET"])
@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@require_http_methods(["GET", "POST"])
@login_required
def change_password_view(request, username):
    user = get_object_or_404(User, username=username)

    if request.user != user:
        messages.error(request, f'You don\'t have permission to change password for user {username}')
        return redirect('accounts:profile_detail', username=username)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Your password was successfully updated.')
            return redirect('accounts:profile_detail', username=username)
        else:
            return render(request, 'accounts/change_password.html', {'form': form})

    form = PasswordChangeForm(user)
    return render(request, 'accounts/change_password.html', {'form': form})


@require_http_methods(["GET", "POST"])
@login_required
def profile_create_view(request):
    if hasattr(request.user, 'profile'):
        messages.info(request, 'You already have profile')
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            return redirect('blog:post_list')
        else:
            return render(request, 'accounts/profile/profile_create.html', {'form': form})

    form = forms.ProfileForm()
    return render(request, 'accounts/profile/profile_create.html', {'form': form})


@require_http_methods(["GET"])
def profile_detail_view(request, username):
    profile = get_object_or_404(models.Profile, user__username=username)
    posts = Post.published.filter(author=profile.user)[:4]
    context = {
        'profile': profile,
        'posts': posts
    }
    return render(request, 'accounts/profile/profile_detail.html', context)


@require_http_methods(["GET", "POST"])
@login_required
def profile_update_view(request, username):
    profile = get_object_or_404(models.Profile, user__username=username)

    if request.user != profile.user:
        messages.error(request, 'You don\'t have permission to edit this profile.')
        return redirect('accounts:profile_detail', username=username)

    if request.method == 'POST':
        form = forms.ProfileForm(instance=profile, data=request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Profile updated')
            return redirect('accounts:profile_detail', username=username)
        else:
            return render(request, 'accounts/profile/profile_update.html', {'form': form})

    form = forms.ProfileForm(instance=profile)
    return render(request, 'accounts/profile/profile_update.html', {'form': form})


@login_required
def user_follow_view(request, username):
    user = get_object_or_404(User, username=username)
    follow = Follow(follower=request.user, followed=user)
    follow.save()
    messages.success(request, f'For now you follow {user.get_full_name()}')
    return redirect('accounts:profile_detail', username=username)


@login_required
def user_unfollow_view(request, username):
    user = get_object_or_404(User, username=username)
    existing_follow = Follow.objects.filter(follower=request.user, followed=user).first()
    if existing_follow:
        existing_follow.delete()
        messages.success(request, f'You have unfollowed {user.get_full_name()}')
    else:
        messages.warning(request, f'You are not following {user.get_full_name()}')
    return redirect('accounts:profile_detail', username=username)


def user_followers_view(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers.filter(followed=user.id)
    return render(request, 'accounts/profile/followers.html', {'user': user,
                                                               'followers': followers})


def user_following_view(request, username):
    user = get_object_or_404(User, username=username)
    followings = user.following.filter(follower=user.id)
    return render(request, 'accounts/profile/followed.html', {'user': user,
                                                              'followings': followings})


