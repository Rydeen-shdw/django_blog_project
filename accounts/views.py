from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from accounts import forms, tokens

User = get_user_model()


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('accounts:test')

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
                return redirect('accounts:test')
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


@require_http_methods(["GET", "POST"])
def registration_view(request):

    if request.user.is_authenticated:
        messages.info(request, 'You are already register.')
        return redirect('accounts:test')

    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data['password'])
            user.is_active = False
            email = form.cleaned_data['email']
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = tokens.account_activation_token.make_token(user)
            send_mail("Confirm Your Email Address",
                      f'http://{current_site}/activate/{uid}/{token}',
                      'from@example.com',
                      [email])
            user.save()
            return redirect('accounts:test')
    else:
        form = forms.UserRegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})


def test_view(request):
    return render(request, 'home.html')


def activate(request, uidb64, token):
    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return redirect("home")
    if user is not None and tokens.account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:test')
    else:
        error_message = 'Activation link is invalid!'
        return HttpResponse(error_message)
