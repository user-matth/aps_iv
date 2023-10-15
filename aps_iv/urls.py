from django.urls import path
from app_aps import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
]
