from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile

User = get_user_model()


class DateInputCustom(forms.DateInput):
    input_type = 'date'


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'date_of_birth', 'avatar', 'bio', 'info']

        labels = {
            'date_of_birth': 'Date of your Birth',
            'avatar': 'Avatar URL'
        }

        placeholders = {
            'avatar': 'Left empty to use gravatar',
            'bio': 'Write a short biography',
            'info': 'Enter some additional information'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': self.Meta.placeholders.get(field_name, '')
            })
        self.fields['date_of_birth'].widget = DateInputCustom()
