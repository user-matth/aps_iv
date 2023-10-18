from django.shortcuts import render
from .models import GeoLocalizacao
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from faker import Faker
import os
import requests
from io import BytesIO
from django.core.files import File
import random
from PIL import Image
from django.http import JsonResponse
import base64
from queue import Queue
import time
from django.core.paginator import Paginator, EmptyPage
from queue import LifoQueue

image_width = 640
image_height = 480

fake = Faker()

def home(request):
    geolocalizacoes = GeoLocalizacao.objects.all()
    items_por_pagina = 10  
    paginator = Paginator(geolocalizacoes, items_por_pagina)

    try:
        numero_pagina = int(request.GET.get('page', 1))
        if numero_pagina < 1:
            raise ValueError
    except ValueError:
        numero_pagina = 1 

    try:
        pagina_atual = paginator.page(numero_pagina)
    except EmptyPage:
        pagina_atual = paginator.page(paginator.num_pages)

    encoded_images = []
    for geolocalizacao in pagina_atual:
        if geolocalizacao.image_blob is not None:
            encoded_image = base64.b64encode(geolocalizacao.image_blob).decode('utf-8')
            encoded_images.append(encoded_image)
        else:
            encoded_images.append(None)

    return render(request, 'home/home.html', {'geolocalizacoes': pagina_atual, 'encoded_images': encoded_images, 'pagina_atual': pagina_atual})

@csrf_protect
def create(request):
    print(request)
    if request.method == 'POST':
        print('aquuuuuuuuuuui')
    else:
        form = GeoLocalizacao()
    return render(request, 'home/create.html', {'form': form})

def store(request):
    if request.method == 'POST':
        # image = request.FILES['image_blob']
        # image_data = image.read()
        image_name = request.POST['image_name']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        altitude = request.POST['altitude']

        location = GeoLocalizacao(
            # image_blob=image_data,
            image_name=image_name,
            latitude=latitude,
            longitude=longitude,
            altitude=altitude
        )

        location.save()
    return render(request, 'home/store.html')


def generate_fake_image_data(width, height, format):
    image = Image.new('RGB', (width, height))

    image_data = BytesIO()
    image.save(image_data, format=format)

    image_binary = image_data.getvalue()
    return image_binary

def fill_database_with_fake_data(request):
    for _ in range(10000): 
        png_image_data = generate_fake_image_data(image_width, image_height, 'PNG')
        location = GeoLocalizacao(
            image_blob=png_image_data,
            image_name=fake.word(),
            latitude=fake.latitude(),
            longitude=fake.longitude(),
            altitude=fake.random_int(min=0, max=1000)
        )
        location.save()
    return render(request, 'home/home.html')

class GeoLocation:
    def __init__(self, image_name, latitude, longitude, altitude):
        self.image_name = image_name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

# def fila(request):
#     fila = Queue()

#     geolocalizacoes = GeoLocalizacao.objects.all()

#     for loc in geolocalizacoes:
#         fila.put(GeoLocation(loc.image_name, loc.latitude, loc.longitude, loc.altitude))

#     tempo_inicial = time.time()

#     elementos_ordenados = []
#     while not fila.empty():
#         elementos_ordenados.append(fila.get())
#     elementos_ordenados = sorted(elementos_ordenados, key=lambda loc: loc.altitude)

#     tempo_final = time.time()

#     tempo_decorrido = tempo_final - tempo_inicial

#     return render(request, 'fila/fila.html', {'elementos_ordenados': elementos_ordenados, 'tempo_decorrido': tempo_decorrido, 'amount': geolocalizacoes.count()})

def fila(request):
    fila = Queue()

    geolocalizacoes = GeoLocalizacao.objects.all()

    for loc in geolocalizacoes:
        fila.put(GeoLocation(loc.image_name, loc.latitude, loc.longitude, loc.altitude))

    tempo_inicial = time.time()

    elementos_ordenados = []
    while not fila.empty():
        elementos_ordenados.append(fila.get())
    elementos_ordenados = sorted(elementos_ordenados, key=lambda loc: loc.altitude)

    tempo_final = time.time()

    tempo_decorrido = tempo_final - tempo_inicial

    items_por_pagina = 10
    paginator = Paginator(elementos_ordenados, items_por_pagina)

    try:
        numero_pagina = int(request.GET.get('page', 1))
        if numero_pagina < 1:
            raise ValueError
    except ValueError:
        numero_pagina = 1

    try:
        pagina_atual = paginator.page(numero_pagina)
    except EmptyPage:
        pagina_atual = paginator.page(paginator.num_pages)

    return render(request, 'fila/fila.html', {'elementos_ordenados': pagina_atual, 'tempo_decorrido': tempo_decorrido, 'amount': geolocalizacoes.count(), 'pagina_atual': pagina_atual})

def pilha(request):
    geolocalizacoes = GeoLocalizacao.objects.all()

    pilha = LifoQueue()
    for loc in geolocalizacoes:
        pilha.put(loc)

    tempo_inicial = time.time()

    elementos_ordenados = []
    while not pilha.empty():
        elementos_ordenados.append(pilha.get())

    elementos_ordenados = sorted(elementos_ordenados, key=lambda loc: loc.altitude)

    tempo_final = time.time()

    tempo_decorrido = tempo_final - tempo_inicial

    items_por_pagina = 10
    paginator = Paginator(elementos_ordenados, items_por_pagina)

    try:
        numero_pagina = int(request.GET.get('page', 1))
        if numero_pagina < 1:
            raise ValueError
    except ValueError:
        numero_pagina = 1

    try:
        pagina_atual = paginator.page(numero_pagina)
    except EmptyPage:
        pagina_atual = paginator.page(paginator.num_pages)

    return render(request, 'pilha/pilha.html', {'elementos_ordenados': pagina_atual, 'tempo_decorrido': tempo_decorrido, 'amount': geolocalizacoes.count(), 'pagina_atual': pagina_atual})