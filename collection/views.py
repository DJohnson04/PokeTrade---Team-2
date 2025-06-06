from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import UserAccount, UserPokemon
import random
from collection.models import Pokemon
import requests

# Create your views here.

#if logged in, display cards gathered from database(currently the html is blank)
@login_required()
def index(request):
    user_profile, created = UserAccount.objects.get_or_create(user=request.user)

    owned_pokemon = user_profile.pokemons.select_related('pokemon').all()

    if not owned_pokemon.exists():
        all_pokemon = list(Pokemon.objects.all())
        for _ in range(9):
            random_pokemon = random.choice(all_pokemon)
            UserPokemon.objects.create(
                owner=user_profile,
                pokemon=random_pokemon,
                unique_id=f"{request.user.id}-{random_pokemon.id}-{random.randint(1000, 9999)}"
            )
    owned_pokemon = user_profile.pokemons.select_related('pokemon').filter(is_selling=False)
    for user_pokemon in owned_pokemon:
        user_pokemon.is_sold = False
    stats = []

    for user_pokemon in owned_pokemon:
        pokemon_name = user_pokemon.pokemon.name.lower()
        api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
        try:
            resp = requests.get(api_url, timeout=5)
            resp.raise_for_status()
            stats = resp.json().get("stats", [])
        except Exception:
            stats = []
    return render(request, 'collection/index.html', {
        'owned_pokemon': owned_pokemon,
        'stats': stats,
    })