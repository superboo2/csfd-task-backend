import time
from requests import Session
from bs4 import BeautifulSoup
from app.models import Film, Actor
from csfd_task.settings import logger


class CsfdScraper:
    """
    A class to scrape data from CSFD and pass it to a processor.
    """

    BASE_URL = "https://www.csfd.cz"

    def __init__(self, processor):
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        }
        self.processor = processor

    def scrape_and_process_top_films_with_actors(self, limit: int = 300):
        """
        Scrapes the top films and their respective actors from CSFD and processes the data.
        """
        film_records = self._scrape_top_films(limit)
        for film_record in film_records:
            logger.info(f"film: {film_record['name']}, rating:{film_record['rating']}")
            film_record["actors"] = self._scrape_film_actors(film_record["url"])
            logger.info("-scraped")
            self.processor.process_and_save_film_data(film_record)
            time.sleep(1)

    def _scrape_top_films(self, limit: int):
        """
        Scrapes the top films from multiple pages on CSFD based on the provided limit.
        """
        url_params = ["", "?from=100", "?from=200", "?from=300"]
        film_records = []

        for url_param in url_params:
            page_url = f"{self.BASE_URL}/zebricky/filmy/nejlepsi/{url_param}"
            film_records.extend(self._scrape_films_from_page(page_url))
            time.sleep(1)

        return film_records[:limit]

    def _scrape_films_from_page(self, url: str) -> list:
        """
        Scrapes films from a single page.
        """
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        film_elements = soup.find_all("h3", {"class": "film-title-norating"})
        films = []

        for film_element in film_elements:
            film_rating_text = film_element.find_next("span", {"class": "film-title-user"}).text.strip()
            film_rating = int(film_rating_text[:-1])  # Remove dot character

            url = film_element.find_next("a")["href"]

            film_url_text = url.split("/")[2]  # 2294-vykoupeni-z-veznice-shawshank/
            film_number = int(film_url_text.split("-")[0])  # 2294

            span_element = film_element.find_next("span", {"class": "film-title-info"})
            film_year = int(span_element.text.strip()[1:-1])  # remove brackets

            data = film_element.find_next("a", {"class": "film-title-name"})

            film = {
                "name": data["title"],
                "film_number": film_number,
                "rating": film_rating,
                "url": f"{self.BASE_URL}{url}",
                "year": film_year,
                "actors": [],
            }

            films.append(film)

        return films

    def _scrape_film_actors(self, film_url: str) -> list:
        """
        Scrapes the list of actors for a given film.
        """
        response = self.session.get(film_url)
        soup = BeautifulSoup(response.text, "html.parser")
        actors = []

        actor_title_element = soup.find("h4", string="Hrají:")
        if actor_title_element:
            actors_container = actor_title_element.find_parent("div")
            actor_elements = actors_container.find_all("a", class_=lambda x: x != "more")

            for actor_element in actor_elements:
                actor_name = actor_element.text.strip()
                url = actor_element["href"]  # /tvurce/103-tim-robbins/
                csfd_url = f"{self.BASE_URL}{url}"  # https://www.csfd.cz/tvurce/103-tim-robbins/
                actor_url_text = url.split("/")[2]  # 103-tim-robbins
                actor_number = int(actor_url_text.split("-")[0])  # 103

                actor = {"name": actor_name, "url": csfd_url, "actor_number": actor_number}

                actors.append(actor)

        return actors


class FilmDataProcessor:
    """
    A class to process and save film data to the database.
    """

    def process_and_save_film_data(self, film_record: dict):
        """
        Saves a single film record with its actors to the database.
        """
        actors = self._get_or_create_actors(film_record["actors"])
        film, is_created = Film.objects.get_or_create(
            film_number=film_record["film_number"],  # unique
            defaults={
                "name": film_record["name"],
                "film_number": film_record["film_number"],
                "rating": film_record["rating"],
                "url": film_record["url"],
                "year": film_record["year"],
            },
        )

        if is_created:
            film.actors.set(actors)
            film.save()

        logger.info("-processed")

    def _get_or_create_actors(self, actor_records: list) -> list:
        actors = []
        for actor_record in actor_records:
            actor, _ = Actor.objects.get_or_create(
                actor_number=actor_record["actor_number"],  # unique
                defaults={
                    "name": actor_record["name"],
                    "actor_number": actor_record["actor_number"],
                    "url": actor_record["url"],
                },
            )

            actors.append(actor)

        return actors
