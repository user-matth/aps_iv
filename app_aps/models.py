from django.db import models

class GeoLocalizacao(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='images/')
    image_name = models.TextField(max_length=100)
    latitude = models.TextField(max_length=100)
    longitude = models.TextField(max_length=100)
    altitude = models.TextField(max_length=100)
