from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput()
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }


class ProfileEditForm(forms.ModelForm):
    model = Profile
    fields = ['user__first_name', 'user__last-name', 'gender', 'date_of_birth', 'info']
    widgets = {
        'user__first_name': forms.TextInput(),
        'user__last-name':  forms.TextInput(),
        'gender': forms.ChoiceField(),
        'date_of_birth': forms.DateField(),
        'info': forms.TextInput()
    }
