# Generated by Django 4.1.5 on 2023-10-18 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_aps', '0002_remove_geolocalizacao_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='geolocalizacao',
            name='image_blob',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
