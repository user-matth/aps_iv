from django.urls import path
from app_aps import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.create, name='create'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/delete/', views.delete, name='delete'),
    path('arvore', views.arvore, name='arvore'),
    path('quicksort', views.quicksort, name='quicksort'),
    path('fill_database/', views.fill_database_with_fake_data, name='fill_database'),
]
