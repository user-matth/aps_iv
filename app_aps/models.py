from django.db import models

class GeoLocalizacao(models.Model):
    id = models.AutoField(primary_key=True)
    image_blob = models.BinaryField(null=True, blank=True)
    image_name = models.TextField(max_length=100)
    latitude = models.TextField(max_length=100)
    longitude = models.TextField(max_length=100)
    altitude = models.TextField(max_length=100)

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
