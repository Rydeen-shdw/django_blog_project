from datetime import date

from django import template
from django.contrib import messages

from blog.models import Follow

register = template.Library()


@register.filter
def is_following(user, user_to_follow):
    return Follow.objects.filter(follower=user, followed=user_to_follow).exists()


@register.filter
def calculate_age(profile):
    today = date.today()
    age = today.year - profile.year - ((today.month, today.day) < (profile.month, profile.day))
    return age