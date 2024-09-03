import django_filters
from unidecode import unidecode
from .models import Film, Actor


class DiacriticInsensitiveCharFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value:
            normalized_value = unidecode(value).lower()
            return qs.filter(name_normalized__contains=normalized_value)
        return qs


class FilmFilter(django_filters.FilterSet):
    name = DiacriticInsensitiveCharFilter(field_name="name_normalized")

    class Meta:
        model = Film
        fields = ["name"]


class ActorFilter(django_filters.FilterSet):
    name = DiacriticInsensitiveCharFilter(field_name="name_normalized")

    class Meta:
        model = Actor
        fields = ["name"]
