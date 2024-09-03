import json
import logging

from rest_framework import status
from django.test import TestCase
from app.helpers import FilmDataProcessor
from app.models import Film

logging.disable(logging.INFO)


class FilmViewTests(TestCase):
    film_url = "/film"

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

    def test_get_film_list_successfully(self):
        self.assertEqual(Film.objects.count(), 1)
        with self.assertNumQueries(2):
            response = self.client.get(self.film_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            results = response.json()["results"]

            self.assertEqual(len(results), 1)
            self.assertEqual(len(results[0]), 2)
            self.assertEqual(results[0]["name"], "Vykoupení z věznice Shawshank")
            self.assertEqual(results[0]["id"], 1)

    def test_get_film_detail_successfully(self):
        self.assertEqual(Film.objects.count(), 1)
        with self.assertNumQueries(2):
            response = self.client.get(f"{self.film_url}/1")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            result = response.json()
            self.assertEqual(len(result), 6)
            self.assertEqual(result["name"], self.film_record["name"])
            self.assertEqual(result["film_number"], self.film_record["film_number"])
            self.assertEqual(result["url"], self.film_record["url"])
            self.assertEqual(result["year"], self.film_record["year"])

            # actors
            self.assertEqual(len(result["actors"]), 2)
            self.assertEqual(len(result["actors"][0]), 2)
            self.assertEqual(result["actors"][0]["id"], 1)
            self.assertEqual(result["actors"][0]["name"], "Tim Robbins")

    def test_update_film_detail_unsuccessfully(self):
        response = self.client.patch(f"{self.film_url}/1", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_film_detail_unsuccessfully(self):
        response = self.client.delete(f"{self.film_url}/1", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_film_detail_unsuccessfully(self):
        response = self.client.post(f"{self.film_url}/1", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
