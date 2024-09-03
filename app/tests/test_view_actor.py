import json
import logging

from rest_framework import status

from django.test import TestCase
from app.helpers import FilmDataProcessor
from app.models import Actor

logging.disable(logging.INFO)


class ActorViewTests(TestCase):
    actor_url = "/actor"

    @classmethod
    def setUpTestData(cls):
        cls.film_record = {
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
        }

        processor = FilmDataProcessor()
        processor.process_and_save_film_data(cls.film_record)

    def test_get_actor_list_successfully(self):
        self.assertEqual(Actor.objects.count(), 2)
        with self.assertNumQueries(2):
            response = self.client.get(self.actor_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            results = response.json()["results"]

            self.assertEqual(len(results), 2)
            self.assertEqual(len(results[0]), 2)
            self.assertEqual(results[0]["name"], "Tim Robbins")
            self.assertEqual(results[0]["id"], 1)

    def test_get_actor_detail_successfully(self):
        self.assertEqual(Actor.objects.count(), 2)
        with self.assertNumQueries(2):
            response = self.client.get(f"{self.actor_url}/2")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            result = response.json()
            self.assertEqual(len(result), 4)

            first_actor = self.film_record["actors"][0]

            for key in ["name", "url", "actor_number", "films"]:
                self.assertIn(key, result)

            # 2 films
            self.assertEqual(len(result["films"]), 1)
            self.assertEqual(len(result["films"][0]), 2)
            self.assertEqual(result["films"][0]["id"], 1)
            self.assertEqual(result["films"][0]["name"], self.film_record["name"])

    def test_update_film_detail_unsuccessfully(self):
        response = self.client.patch(f"{self.actor_url}/1", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_film_detail_unsuccessfully(self):
        response = self.client.delete(f"{self.actor_url}/1", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_film_detail_unsuccessfully(self):
        response = self.client.post(f"{self.actor_url}/1", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
