from django.shortcuts import get_object_or_404
import requests
from django.core.management.base import BaseCommand
from pokedex.models import Type, Pokemon
import progressbar
import time

class Command(BaseCommand):
    help = 'Fetch data from the external API and populate the database'

    def handle(self, *args, **kwargs):
        ### TYPES ###
        # On sait qu'il n'y a que 19 types de Pokemon sur l'API
        typesCountPokeapi = 19
        pbar = progressbar.ProgressBar(maxval=typesCountPokeapi)
        pbar.start()
        for i in range(1, typesCountPokeapi + 1):
            response = requests.get('https://pokeapi.co/api/v2/type/' + str(i))
            if response.status_code == 200:
                type_data = response.json()
                Type.objects.update_or_create(
                    name = type_data['name'],
                    image_src = type_data['sprites']['generation-ix']['scarlet-violet']['name_icon']
                )
                time.sleep(0.05)
                pbar.update(i)
            else:
                self.stdout.write(self.style.ERROR('Failed to fetch data from the API for index ' + str(i)))
        pbar.finish()
        self.stdout.write(self.style.SUCCESS('Tous les Types de Pokemon ont bien été initialisé.'))

        ### POKEMON STARTERS ###
        starters = ['bulbasaur', 'charmander', 'squirtle']
        for starter in starters :
            response = requests.get('https://pokeapi.co/api/v2/pokemon/' + starter)
            if response.status_code == 200:
                pokemon_data = response.json()
                starter_pk, created = Pokemon.objects.update_or_create(
                    name = pokemon_data['name'].lower(),
                    height = pokemon_data['height'],
                    weight = pokemon_data['weight'],
                    image_src = pokemon_data['sprites']['other']['official-artwork']['front_default']
                )
                starter_pk.types.set(list(map(lambda p: get_object_or_404(Type, pk=p['type']['name']), pokemon_data['types'])))
            else : 
                self.stdout.write(self.style.ERROR("L'ajout du starter a échoué pour le Pokemon suivant : " + starter))

        self.stdout.write(self.style.SUCCESS("L'initialisation du Pokedex est terminée."))

        return True
