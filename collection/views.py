from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import OwnedPokeMon
import random
from collection.models import Pokemon


# Create your views here.

#if logged in, display cards gathered from database(currently the html is blank)
@login_required()
def index(request):
    try:
        user_profile = OwnedPokeMon.objects.get(user=request.user)
    except OwnedPokeMon.DoesNotExist:
        user_profile = OwnedPokeMon.objects.create(user=request.user)
        print("created owned_pokemon field")
    owned_pokemon = user_profile.owned_pokemon.all()
    if not owned_pokemon:
        for i in range (1, 10):
            user_profile.owned_pokemon.add(random.choice(Pokemon.objects.all()))
        owned_pokemon = user_profile.owned_pokemon.all()

    return render(request, 'collection/index.html', {
                    'owned_pokemon': owned_pokemon})