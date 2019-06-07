from core.command_handler import CommandHandler
from pipeline.scrapers.overview_scraper import OverviewScraper


class ScrapeCommand(CommandHandler):
    name = 'scrape'

    def run(self):
        scraper = OverviewScraper(self.command[0], load=False)
        scraper.scrape()
        n_results = scraper.save_results()
        print('{} results added to database'.format(n_results))
