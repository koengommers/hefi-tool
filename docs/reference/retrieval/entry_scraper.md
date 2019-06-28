# hefi_tool.retrieval.entry_scraper
Contains EntryScraper class.
## EntryScraper
Scrapes overview page for entries.

Scrapes the listings page of a year for the institution information on it.
It also indexes the non-standardized documents on the page. For every
institution it saves the business id (KvK nummer), the name and the
location of the institution and the year.
```python
EntryScraper(page)
```
Init the class.

**Args:**
- page (OverviewPage): The page to scrape.

### scrape_entries
```python
EntryScraper.scrape_entries(self)
```
Start scraping the page for entries.
### scrape_entry
```python
EntryScraper.scrape_entry(self, elem)
```
Get data from an element containing an entry.

**Args:**
- elem: BeautifulSoup element that contains the entry.


### scrape_documents
```python
EntryScraper.scrape_documents(self, entry, entry_elem)
```
Scrape non-standardized documents belonging to an entry.

**Args:**
- entry (Entry): The entry to scrape the documents for.
- entry_elem: The BeautifulSoup element that contains the data.


### save_results
```python
EntryScraper.save_results(self)
```
Save the scraping results.

**Returns:**
    (tuple) Number of entries and number of documents scraped.


