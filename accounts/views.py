from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.conf import settings

from accounts import forms
from accounts import models
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
        return render(request, 'accounts/registration.html', {'form': form})

    form = forms.RegisterForm()
    return render(request, 'accounts/registration.html', {'form': form})


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
        return redirect('blog:post_list')

    messages.error(request, 'Token expired')
    return redirect('blog:post_list')


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
                return redirect('blog:post_list')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid form data')
            return render(request, 'accounts/login.html', {'form': form})

    form = forms.LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def test_view(request):
    return render(request, 'home.html')
