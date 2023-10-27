from django.urls import path
from app_aps import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.create, name='create'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('arvore', views.arvore, name='arvore'),
    path('quicksort', views.quicksort, name='quicksort'),
    path('bubblesort', views.bubblesort, name='bubblesort'),
    path('fill_database/', views.fill_database_with_fake_data, name='fill_database'),
    path('relatorio/', views.relatorio, name='relatorio'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)