from django.urls import path
from app_aps import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.create, name='create'),
    path('update/<int:id>/', views.update, name='update'),
    path('patch/', views.patch, name='patch'),
    path('delete/<int:id>/delete/', views.delete, name='delete'),
    path('store', views.store, name='store'),
    path('fila', views.fila, name='fila'),
    path('pilha', views.pilha, name='pilha'),
    path('lista', views.lista, name='lista'),
    path('arvore', views.arvore, name='arvore'),
    path('fill_database/', views.fill_database_with_fake_data, name='fill_database'),
]
