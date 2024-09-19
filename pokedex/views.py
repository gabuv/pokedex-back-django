from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from rest_framework import serializers
import requests

from pokedex.management.commands import fetch_init_data
from pokedex.models import Pokemon, Type

class IndexView(generic.ListView):

    def get_queryset(self):
        try:
            """Return last Pokemon discovered."""
            return Pokemon.objects.latest("discover_date")
        except (Pokemon.DoesNotExist):
            return None
          
def latest_pokemon(request): 
    try:
        """Return last Pokemon discovered."""
        latest_pokemon_discovered = Pokemon.objects.latest("discover_date")
        serializer = PokemonSerializer(latest_pokemon_discovered)
        return JsonResponse(serializer.data, safe=False)
    except (Pokemon.DoesNotExist):
        return JsonResponse({"result" : []}, status=204) 

def all_names(request):
    allPokemon = Pokemon.objects.all().order_by('name')
    return JsonResponse([p.name for p in allPokemon], safe=False)

def found_pokemon(request, name):
    try:
        object_found = Pokemon.objects.get(pk=name.lower())
        serializer = PokemonSerializer(object_found, context={'new_created_pokemon': False})
        return JsonResponse(serializer.data, safe=False)
    except (Pokemon.DoesNotExist):
        # Call PokeAPI
        pokeapi_new_pokemon = pokeapi_pokemon_endpoint(name)
        if (pokeapi_new_pokemon != None):
            serializer =  PokemonSerializer(pokeapi_new_pokemon, context={'new_created_pokemon': True})
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({"result" : []}, status=204)
        

def pokeapi_pokemon_endpoint(name):
    response = requests.get('https://pokeapi.co/api/v2/pokemon/' + name.lower())
    if response.status_code == 200:
        pokemon_data = response.json()
        new_pokemon_pk, created = Pokemon.objects.update_or_create(
            name = pokemon_data['name'].lower(),
            height = pokemon_data['height'],
            weight = pokemon_data['weight'],
            image_src = pokemon_data['sprites']['other']['official-artwork']['front_default']
        )
        new_pokemon_pk.types.set(list(map(lambda p: get_object_or_404(Type, pk=p['type']['name']), pokemon_data['types'])))
        return new_pokemon_pk
    else:
        return
    
def update_pokedex(request):
    count_types = Type.objects.count()
    # Si le nombre de Types de la BDD est 0 alors la BDD n'a pas été initialisée
    if (count_types == 0) :
        # On lance le script fetch_init_data
        command = fetch_init_data.Command()
        ret = command.handle()
        return JsonResponse({"result" : "La base de données est maintenant initialisée"}, status=200)
    else :
        return JsonResponse({"result" : "La base de données est déjà initialisée"}, status=204)



class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['name', 'image_src']


class PokemonSerializer(serializers.ModelSerializer):

    types = TypeSerializer(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = ['name', 'height', 'weight', 'discover_date', 'types', 'image_src']
