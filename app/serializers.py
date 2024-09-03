from rest_framework import serializers
from app.models import Film, Actor


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name"]


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ["id", "name"]


class FilmDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)

    class Meta:
        model = Film
        fields = ["name", "actors", "film_number", "rating", "url", "year"]


class ActorDetailSerializer(serializers.ModelSerializer):
    films = FilmSerializer(many=True)

    class Meta:
        model = Actor
        fields = ["name", "url", "actor_number", "films"]
