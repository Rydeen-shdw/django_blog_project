from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError


def send_activation_api_email(user, token, sender_email):
    activation_url = f'{settings.EMAIL_DOMAIN}/api/v1.0/accounts/activate/{token.token}/'
    try:
        send_mail(
            'Activate your account',
            f'Please click on the following link to activate your account: {activation_url}',
            sender_email,
            [user.email],
            fail_silently=False
        )
    except ValidationError as e:
        return {'success': False, 'message': 'Validation error', 'details': str(e)}
    except Exception as e:
        return {'success': False, 'message': 'Error sending activation email', 'details': str(e)}