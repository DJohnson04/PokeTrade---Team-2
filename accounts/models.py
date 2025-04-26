from django.db import models
from django.contrib.auth.models import User
from collection.models import Pokemon

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.user.username
class UserPokemon(models.Model):
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='pokemons')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=100, unique=True)  # Optional: to uniquely identify each instance
    is_selling = models.BooleanField(default=False)  # if True, dont display on collections
    def __str__(self):
        return f"{self.pokemon.name} owned by {self.owner.user.username}"
class Listing(models.Model):
    seller = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='listings')
    user_pokemon = models.OneToOneField(UserPokemon, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
