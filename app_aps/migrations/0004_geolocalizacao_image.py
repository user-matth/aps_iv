# Generated by Django 4.1.5 on 2023-10-23 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_aps', '0003_geolocalizacao_image_blob'),
    ]

    operations = [
        migrations.AddField(
            model_name='geolocalizacao',
            name='image',
            field=models.ImageField(blank=True, default='default_image.jpg', null=True, upload_to='images/'),
        ),
    ]
