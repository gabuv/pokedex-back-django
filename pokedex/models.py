import json
from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    image_src = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Pokemon(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    discover_date = models.DateTimeField("datetime of the discovery", auto_now_add=True)
    types = models.ManyToManyField(Type)
    image_src = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name
    
    def toJSON(self):
        return json.dumps(
        self,
        # default=lambda o: o.__dict__, 
        sort_keys=True,
        indent=4)

