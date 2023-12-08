from django import forms


class CityWeatherForm(forms.Form):
    city = forms.CharField(max_length=100)


class UserCityCreateForm(forms.Form):
    city = forms.CharField(widget=forms.HiddenInput())
    country_code = forms.CharField(widget=forms.HiddenInput())
    lat = forms.FloatField(widget=forms.HiddenInput())
    lon = forms.FloatField(widget=forms.HiddenInput())
