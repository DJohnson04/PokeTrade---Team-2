from django.db import models
from django.contrib.auth.models import User
from collection.models import Pokemon

class OwnedPokeMon(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owned_pokemon = models.ManyToManyField(Pokemon, related_name="owners")
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.user.username