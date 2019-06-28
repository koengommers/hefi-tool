# hefi_tool.retrieval.document_scraper
Contains DocumentScraper class.
## DocumentScraper
Scrapes standardized documents pages.

Indexes standardized documents on the standardized documents page
of an entry. For every document it stores what entry it belongs to
and the label of the document.
```python
DocumentScraper(page)
```
Init DocumentScraper object.

**Args:**
- page (DocumentsPage): The page to scrape the documents from.

### scrape_documents
```python
DocumentScraper.scrape_documents(self)
```
Start scraping for the documents.
### save_results
```python
DocumentScraper.save_results(self)
```
Save the scraping results.

**Returns:**
    (int) Number of documents found and indexed.


