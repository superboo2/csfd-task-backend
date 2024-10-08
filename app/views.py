from rest_framework import viewsets, filters
from app.models import Film, Actor
from app.serializers import FilmSerializer, ActorSerializer, FilmDetailSerializer, ActorDetailSerializer


class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "name_normalized",
    ]

    queryset = Film.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FilmDetailSerializer
        return FilmSerializer


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "name_normalized",
    ]
    queryset = Actor.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActorDetailSerializer
        return ActorSerializer
