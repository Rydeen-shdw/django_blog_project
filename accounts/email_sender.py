from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts import tokens


def send_activation_mail(request, user, to_email):
    from_email = 'admin@admin.com'
    subject = "Activation account"
    message = render_to_string('accounts/email_confirmation.html', {
        'user': user,
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': tokens.account_activation_token.make_token(user)
    })
    email = EmailMessage(subject, message, from_email, to=[to_email])
    if email.send():
        messages.success(request, f'{user}, activation link send in your E-mail')
    else:
        messages.error(request, 'E-mail not send')




