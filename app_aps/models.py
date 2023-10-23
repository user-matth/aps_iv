from django.db import models
from django.utils import timezone

class GeoLocalizacao(models.Model):
    id = models.AutoField(primary_key=True)
    image_blob = models.BinaryField(null=True, blank=True)
    image = models.ImageField(upload_to='media/images/', default='default_image.jpg', null=True, blank=True)
    image_name = models.TextField(max_length=100)
    latitude = models.TextField(max_length=100)
    longitude = models.TextField(max_length=100)
    altitude = models.TextField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.created_at:
            self.created_at = timezone.now()
        return super(GeoLocalizacao, self).save(*args, **kwargs)

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
