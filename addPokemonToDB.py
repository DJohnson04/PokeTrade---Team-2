import os
import sys
import django
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poketrade.settings')
django.setup()

from collection.models import Pokemon

def load_pokemon():
    for i in range(1, 1200):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch Pokémon #{i}")
            continue

        data = response.json()
        name = data["name"]
        image_url = data["sprites"]["other"]["official-artwork"]["front_default"]
        types = ", ".join([t['type']['name'] for t in data["types"]])

        pokemon, created = Pokemon.objects.get_or_create(
            pokemon_id=i,
            defaults={
                'name': name,
                'image_url': image_url,
                'types': types,
            }
        )

        if created:
            print(f"Added {name}")
        else:
            print(f"{name} already exists")


if __name__ == "__main__":
    load_pokemon()
