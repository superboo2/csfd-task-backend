from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from app.filters import FilmFilter, ActorFilter
from app.models import Film, Actor
from app.serializers import FilmSerializer, ActorSerializer, FilmDetailSerializer, ActorDetailSerializer


class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilmFilter
    queryset = Film.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FilmDetailSerializer
        return FilmSerializer


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ActorFilter
    queryset = Actor.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActorDetailSerializer
        return ActorSerializer
