from django.core.management.base import BaseCommand
from app.helpers import CsfdScraper, FilmDataProcessor


class Command(BaseCommand):
    help = "Scrapes films and their actors from CSFD and saves the data to the database."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Scrapping and processing ..."))
        processor = FilmDataProcessor()
        scraper = CsfdScraper(processor)
        scraper.scrape_and_process_top_films_with_actors()
        self.stdout.write(self.style.SUCCESS("Films processed"))
