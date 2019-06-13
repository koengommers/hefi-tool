from core.command_handler import CommandHandler
from pipeline.retrieval.overview_page import OverviewPage
from pipeline.retrieval.entry_scraper import EntryScraper


class ScrapeCommand(CommandHandler):
    name = 'scrape'

    def run(self):
        try:
            page = OverviewPage(int(self.command[0]))
            scraper = EntryScraper(page)
            scraper.scrape_entries()
            n_results = scraper.save_results()
            print('{} entries and {} documents added to database'.format(*n_results))
        except RuntimeError:
            print('Something went wrong. Try again.')
