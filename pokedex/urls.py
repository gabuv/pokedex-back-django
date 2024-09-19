from django.urls import path

from . import views
from .views import latest_pokemon, all_names, found_pokemon, update_pokedex

app_name = "pokedex"
urlpatterns = [
    path("/", views.IndexView.as_view(), name="index"),
    path("index/", latest_pokemon),
    path("allNames/", all_names),
    path("pokemon/<name>/", found_pokemon),
    path("updatePokedex/", update_pokedex)
]