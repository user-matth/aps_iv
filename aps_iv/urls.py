from django.urls import path
from app_aps import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.new, name='create')
]
