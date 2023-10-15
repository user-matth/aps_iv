from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')

def create(request):
    return render(request, 'home/create.html')