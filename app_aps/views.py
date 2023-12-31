from django.shortcuts import render, get_object_or_404, redirect
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
from .forms import GeoLocalizacaoForm
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template import loader
import asyncio
from django.http import HttpResponse
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from asgiref.sync import sync_to_async
import tempfile

image_width = 640
image_height = 480

fake = Faker()

def format(num):
    formatted_number = "{:,.3f}".format(num / 1000)
    return formatted_number

def home(request):
    geolocalizacoes = GeoLocalizacao.objects.all().order_by('image_name')
    
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

    return render(request, 'home/home.html', {
        'geolocalizacoes' : pagina_atual, 
        'pagina_atual' : pagina_atual, 
        'amout' : geolocalizacoes.count(),
    })

@csrf_protect
def create(request):
    if request.method == 'POST':
        form = GeoLocalizacaoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')

        return render(request, 'home/home.html')
    return render(request, 'home/create.html')

@csrf_protect
def update(request, id):
    location = get_object_or_404(GeoLocalizacao, id=id)

    if request.method == 'POST':
        form = GeoLocalizacaoForm(request.POST, request.FILES, instance=location)  # Pass the instance to update
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GeoLocalizacaoForm(instance=location)

    return render(request, 'home/update.html', {'location': location})

def delete(request, id):
    location = get_object_or_404(GeoLocalizacao, id=id)
    location.delete()
    return redirect('home')

def generate_fake_image_data(width, height, format):
    image = Image.new('RGB', (width, height))

    image_data = BytesIO()
    image.save(image_data, format=format)

    image_binary = image_data.getvalue()
    return image_binary

def fill_database_with_fake_data(request):
    image_dir = 'media/media/images'
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
    return redirect('home')
    
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
        'amount' : format(elementos.count()),
    })

def arvore_res():
    tempo_inicial = time.time()
    elementos = GeoLocalizacao.objects.all()

    root = None

    for elemento in elementos:
        root = insert(root, elemento)

    elementos_ordenados = list(in_order_traversal(root))

    tempo_final = time.time()
    tempo_decorrido = tempo_final - tempo_inicial
    tempo_decorrido_formatted = f'{tempo_decorrido:.2f}'

    return (tempo_decorrido_formatted)

# QUICKSORT
def quicksort(request):
    geolocalizacoes = GeoLocalizacao.objects.all().order_by('image_name')

    start_time = time.time()

    def quick_sort_algorithm(arr):
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x.image_name < pivot.image_name]
        middle = [x for x in arr if x.image_name == pivot.image_name]
        right = [x for x in arr if x.image_name > pivot.image_name]

        return quick_sort_algorithm(left) + middle + quick_sort_algorithm(right)

    sorted_geolocalizacoes = quick_sort_algorithm(list(geolocalizacoes))

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    items_per_page = 10
    paginator = Paginator(sorted_geolocalizacoes, items_per_page)
    page = request.GET.get('page')

    try:
        sorted_geolocalizacoes = paginator.page(page)
    except PageNotAnInteger:
        sorted_geolocalizacoes = paginator.page(1)
    except EmptyPage:
        sorted_geolocalizacoes = paginator.page(paginator.num_pages)


    return render(request, 'quick_sort/quick_sort.html', {
        'elementos_ordenados': sorted_geolocalizacoes,
        'tempo_decorrido': elapsed_time,
        'amount' : format(geolocalizacoes.count()),
    })
    
def quicksort_res():
    geolocalizacoes = GeoLocalizacao.objects.all()

    start_time = time.time()

    def quick_sort_algorithm(arr):
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x.image_name < pivot.image_name]
        middle = [x for x in arr if x.image_name == pivot.image_name]
        right = [x for x in arr if x.image_name > pivot.image_name]

        return quick_sort_algorithm(left) + middle + quick_sort_algorithm(right)

    sorted_geolocalizacoes = quick_sort_algorithm(list(geolocalizacoes))

    end_time = time.time()
    elapsed_time = end_time - start_time

    return (elapsed_time)

# BUBBLESORT
def bubblesort(request):
    geolocalizacoes = list(GeoLocalizacao.objects.all().order_by('image_name'))
    amount = len(geolocalizacoes)

    start_time = time.time()

    def sorted_bubble_sort(geolocalizacoes):
        loc_s = list(geolocalizacoes)
        n = len(loc_s)
        steps = [] 

        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if loc_s[j].image_name > loc_s[j + 1].image_name:
                    loc_s[j], loc_s[j + 1] = loc_s[j + 1], loc_s[j]
                    steps.append(list(loc_s))
        return steps

    ordenacao_bubble = sorted_bubble_sort(geolocalizacoes)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    items_per_page = 10
    paginator = Paginator(geolocalizacoes, items_per_page)
    page = request.GET.get('page')

    try:
        geolocalizacoes = paginator.page(page)
    except PageNotAnInteger:
        geolocalizacoes = paginator.page(1)
    except EmptyPage:
        geolocalizacoes = paginator.page(paginator.num_pages)
        
    data = {
        'elementos_ordenados': geolocalizacoes,
        'tempo_decorrido': elapsed_time,
        'amount' : amount,
    }
    
    return render(request, 'bubble_sort/bubble_sort.html', data)

def bubblesort_res():
    geolocalizacoes = list(GeoLocalizacao.objects.all().order_by('altitude'))
    start_time = time.time()

    def sorted_bubble_sort(geolocalizacoes):
        loc_s = list(geolocalizacoes)
        n = len(loc_s)
        steps = [] 

        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if loc_s[j].altitude > loc_s[j + 1].altitude:
                    loc_s[j], loc_s[j + 1] = loc_s[j + 1], loc_s[j]
                    steps.append(list(loc_s))
        return steps

    ordenacao_bubble = sorted_bubble_sort(geolocalizacoes)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return (elapsed_time)

def relatorio(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

    p = canvas.Canvas(response)
    
    elapsed_time = bubblesort_res()
    bubblesort_res_time_str = "{:.2f}".format(elapsed_time)
    
    elapsed_time2 = quicksort_res()
    quicksort_res_time_str2 = "{:.2f}".format(elapsed_time2)

    p.drawString(100, 750, "Tempo estimado para Ordenação tipo Árvore: " + arvore_res())
    p.drawString(100, 720, "Tempo estimado para Ordenação tipo BubbleSort: " + bubblesort_res_time_str)
    p.drawString(100, 690, "Tempo estimado para Ordenação tipo BubbleSort: " + quicksort_res_time_str2)
    p.showPage()
    p.save()
    
    return response