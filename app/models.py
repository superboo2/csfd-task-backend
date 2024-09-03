from unidecode import unidecode
from django.db import models


class Actor(models.Model):
    actor_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    name_normalized = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.name_normalized = unidecode(self.name).lower()
        super().save(*args, **kwargs)


class Film(models.Model):
    film_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    name_normalized = models.CharField(max_length=255)

    url = models.CharField(max_length=255)
    year = models.IntegerField()
    rating = models.IntegerField()

    actors = models.ManyToManyField(Actor, related_name="films")

    def save(self, *args, **kwargs):
        self.name_normalized = unidecode(self.name).lower()
        super().save(*args, **kwargs)
