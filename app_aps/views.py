from django.shortcuts import render
from .models import GeoLocalizacao
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect

def home(request):
    geolocalizacoes = {
        'geolocalizacao': GeoLocalizacao.objects.all()
    }
    return render(request, 'home/home.html', geolocalizacoes)

@csrf_protect
def create(request):
    if request.method == 'POST':
        print('aquuuuuuuuuuui')
        # form = GeoLocalizacao(request.POST)
        # new_geolocalizacao = GeoLocalizacao()
        # new_geolocalizacao.image_name = request.POST.get('image_name')
        # new_geolocalizacao.latitude = request.POST.get('latitude')
        # new_geolocalizacao.longitude = request.POST.get('longitude')
        # new_geolocalizacao.altitude = request.POST.get('altitude')
        # new_geolocalizacao.save()
        # geolocalizacoes = {
        #     'geolocalizacao': GeoLocalizacao.objects.all()
        # }
        # return HttpResponseRedirect('/home')
    else:
        form = GeoLocalizacao()
    return render(request, 'home/create.html', {'form': form})

