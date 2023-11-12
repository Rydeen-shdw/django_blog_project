from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

from config import settings


def send_email(request, subject, user, to_email, template_name):
    from_email = 'admin@3dexzilla.com'
    template_url = 'accounts/' + template_name + '.html'
    message = {
        'user': user,
        'domain': settings.EMAIL_DOMAIN,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)}
    html_message = render_to_string(template_url, message)
    email = EmailMultiAlternatives(
        subject, html_message, from_email, to=[to_email])
    email.mixed_subtype = 'related'
    email.attach_alternative(html_message, 'text/html')
    return email
