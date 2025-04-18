from django.db import models

# Create your models here.
class Pokemon(models.Model):
    pokemon_id = models.IntegerField(unique=True)
    name = models.CharField(max_length = 50)
    image_url = models.URLField(blank=True, null=True)
    types = models.CharField(max_length=100)
