from django import forms
from .models import GeoLocalizacao

class GeoLocalizacaoForm(forms.ModelForm):
    class Meta:
        model = GeoLocalizacao
        fields = ['image', 'image_name', 'latitude', 'longitude', 'altitude']
