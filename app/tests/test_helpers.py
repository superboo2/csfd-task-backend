import json
import logging

from django.test import TestCase
from app.helpers import FilmDataProcessor, CsfdScraper
from app.models import Film, Actor

logging.disable(logging.INFO)


class FilmDataProcessorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.film_records = [
            {
                "name": "Vykoupení z věznice Shawshank",
                "film_number": 2294,
                "rating": 1,
                "url": "abc",
                "year": 1994,
                "actors": [
                    {"name": "Tim Robbins", "url": "abc", "actor_number": 103},
                    {
                        "name": "Morgan Freeman",
                        "url": "abc",
                        "actor_number": 92,
                    },
                ],
            },
            {
                "name": "Forrest Gump",
                "film_number": 10135,
                "rating": 2,
                "url": "abc",
                "year": 1994,
                "actors": [
                    {"name": "Tom Hanks", "url": "abc", "actor_number": 330},
                    {
                        "name": "Robin Wright",
                        "url": "abc",
                        "actor_number": 604,
                    },
                ],
            },
        ]

    def test_process_and_save_film_data(self):
        self.assertEqual(Film.objects.count(), 0)
        self.assertEqual(Actor.objects.count(), 0)

        processor = FilmDataProcessor()
        processor.process_and_save_film_data(self.film_records[0])

        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Actor.objects.count(), 2)

    def test_process_and_save_film_data_duplicity_film_number(self):
        # Only the film with unique film_number will be created.
        self.assertEqual(Film.objects.count(), 0)

        self.film_records[1]["film_number"] = self.film_records[0]["film_number"]

        processor = FilmDataProcessor()
        processor.process_and_save_film_data(self.film_records[0])
        processor.process_and_save_film_data(self.film_records[1])

        self.assertEqual(Film.objects.count(), 1)

    def test_process_and_save_film_data_film_without_actors(self):
        # Film can be without actors.
        self.assertEqual(Film.objects.count(), 0)
        self.assertEqual(Actor.objects.count(), 0)

        self.film_records[0]["actors"] = []

        processor = FilmDataProcessor()
        processor.process_and_save_film_data(self.film_records[0])

        self.assertEqual(list(Film.objects.first().actors.all()), [])
        self.assertEqual(Actor.objects.count(), 0)

    def test_process_and_save_film_data_duplicity_actor_number(self):
        # Only the actor with unique actor_number will be created.
        self.assertEqual(Film.objects.count(), 0)
        self.assertEqual(Actor.objects.count(), 0)

        self.film_records[1]["actors"][1]["actor_number"] = self.film_records[0]["actors"][0]["actor_number"]

        processor = FilmDataProcessor()
        processor.process_and_save_film_data(self.film_records[0])
        processor.process_and_save_film_data(self.film_records[1])

        self.assertEqual(Film.objects.count(), 2)
        self.assertEqual(Actor.objects.count(), 3)
