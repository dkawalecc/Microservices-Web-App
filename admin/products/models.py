from django.db import models
from django.apps import AppConfig
# import os
# from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
# settings.configure(default_settings="admin.settings", DEBUG=True)

# Create your models here.


class Product(models.Model):
    # id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)


class User(models.Model):
    # id = models.BigAutoField(primary_key=True)
    pass
