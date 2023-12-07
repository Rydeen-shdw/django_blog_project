from django import forms


class CityWeatherForm(forms.Form):
    city = forms.CharField(max_length=100)

