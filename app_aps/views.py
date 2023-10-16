from django.shortcuts import render
from .models import GeoLocalizacao

def home(request):
    geolocalizacoes = {
        'geolocalizacao': GeoLocalizacao.objects.all()
    }
    return render(request, 'home/home.html', geolocalizacoes)

def create(request):
    new_geolocalizacao = GeoLocalizacao()
    new_geolocalizacao.image_name = request.POST.get('image_name')
    new_geolocalizacao.latitude = request.POST.get('latitude')
    new_geolocalizacao.longitude = request.POST.get('longitude')
    new_geolocalizacao.altitude = request.POST.get('altitude')
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    # new_geolocalizacao.save()
    # geolocalizacoes = {
    #     'geolocalizacao': GeoLocalizacao.objects.all()
    # }
    # return render(request, 'home/home.html')

def new(request):
    return render(request, 'home/create.html')