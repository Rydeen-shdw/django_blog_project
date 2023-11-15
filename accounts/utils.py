from django.core.mail import send_mail
from django.http import HttpRequest
from django.urls import reverse


def send_activation_email(user, user_token, from_email, request: HttpRequest):
    activation_url = f'{request.scheme}://{request.get_host()}' \
                     f'{reverse("accounts:activate", args=[user.username, user_token.token])}'
    send_mail(
        'Activate your account',
        f'Please click on the following link to activate your account: {activation_url}',
        from_email,
        [user.email],
        fail_silently=False
    )
