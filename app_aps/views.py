from django.shortcuts import render
from .models import GeoLocalizacao, TreeNode
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from queue import LifoQueue
from operator import attrgetter

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

# FILA

def fila(request):
    tempo_inicial = time.time()
    fila = Queue()

    geolocalizacoes = GeoLocalizacao.objects.all()

    for loc in geolocalizacoes:
        fila.put(GeoLocation(loc.image_name, loc.latitude, loc.longitude, loc.altitude))


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
    tempo_inicial = time.time()
    geolocalizacoes = GeoLocalizacao.objects.all()

    pilha = LifoQueue()
    for loc in geolocalizacoes:
        pilha.put(loc)


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

# LISTA

def lista(request):
    tempo_inicial = time.time()
    elementos = GeoLocalizacao.objects.all()

    elementos_ordenados = sorted(elementos, key=attrgetter('image_name'))

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
        
    tempo_final = time.time()
    tempo_decorrido = tempo_final - tempo_inicial

    return render(request, 'lista/lista.html', {
        'elementos_ordenados': pagina_atual,
        'tempo_decorrido': tempo_decorrido,
        'amount': elementos.count(),
        'pagina_atual': pagina_atual,
    })
    
# ARVORE BINARIA

class Node:
    def __init__(self, elemento):
        self.elemento = elemento
        self.left = None
        self.right = None

def insert(root, elemento):
    if root is None:
        return Node(elemento)
    if elemento.altitude < root.elemento.altitude:
        root.left = insert(root.left, elemento)
    else:
        root.right = insert(root.right, elemento)
    return root

def in_order_traversal(root):
    if root:
        yield from in_order_traversal(root.left)
        yield root.elemento
        yield from in_order_traversal(root.right)
        
def arvore(request):
    tempo_inicial = time.time()
    elementos = GeoLocalizacao.objects.all()

    root = None

    for elemento in elementos:
        root = insert(root, elemento)

    elementos_ordenados = list(in_order_traversal(root))

    items_per_page = 10

    paginator = Paginator(elementos_ordenados, items_per_page)

    page = request.GET.get('page')

    try:
        elementos_ordenados = paginator.page(page)
    except PageNotAnInteger:
        elementos_ordenados = paginator.page(1)
    except EmptyPage:
        elementos_ordenados = paginator.page(paginator.num_pages)

    tempo_final = time.time()
    tempo_decorrido = tempo_final - tempo_inicial

    return render(request, 'arvore/arvore.html', {
        'elementos_ordenados': elementos_ordenados,
        'tempo_decorrido': tempo_decorrido,
    })