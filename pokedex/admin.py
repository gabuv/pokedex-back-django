from django.contrib import admin

from .models import Type, Pokemon

admin.site.register(Pokemon)
admin.site.register(Type)
