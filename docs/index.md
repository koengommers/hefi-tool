# General description

The tool is able to extract and store data given a year. The following steps are taken to achieve this:
* Scrape entries
* Index documents
* Download documents
* Extract data

The documents are published on a [government website](https://www.desan.nl/net/DoSearch/Search.aspx), this website uses JavaScript to handle a lot of things, which makes navigating and scraping the site automatically a bit harder. A webdriver (using [Selenium](https://selenium-python.readthedocs.io/installation.html#introduction) and [chromedriver](http://chromedriver.chromium.org/)) is used to automate a browser, so the JavaScript is ran.

Data is stored in a [SQLite](https://www.sqlite.org/index.html) database and [SQLAlchemy](https://www.sqlalchemy.org/) is used for easy use of interacting with the database.

## Scrape entries
To scrape the entries from the website the year is entered in the search form. Each entry belongs to an institution in a certain year. These entries are scraped and stored in the database. See [EntryScraper](reference/retrieval/entry_scraper.md) for more details.

## Index documents
For every entry the corresponding documents are indexed to see what is available. See [DocumentScraper](reference/retrieval/document_scraper.md) for more details.

## Download documents
After the documents are indexed, the needed documents are selected and downloaded. See [Pipeline](reference/pipeline.md) for details on selecting documents [DocumentDownloader](reference/retrieval/document_downloader.md) for details on downloading documents.

## Extract data
Every document that is downloaded is afterwards processed to extract data. The exact method differs for each document type, however all methods make use of [PDFQuery](https://github.com/jcushman/pdfquery), a library for extracting data from PDF documents. See [EmployeeDataExtractor](reference/processing/employee_data_extractor.md), [EntityDataExtractor](reference/processing/entity_data_extractor.md), [FinancialDataExtractor](reference/processing/financial_data_extractor.md) for more details.

The data stored in the database can be put into a [Pandas](https://pandas.pydata.org/) DataFrame or exported to csv. See examples in '[Using the data](examples/using_the_data.md)'.

# Examples of usage

- [Processing a year](examples/processing_a_year.md)
- [Using the data](examples/using_the_data.md)

# Reference

- **migrations**: *Contains [alembic](https://alembic.sqlalchemy.org/en/latest/) migration files.*
- **models**: *Contains database models*
    - [data_point](reference/models/data_point.md)
    - [document](reference/models/document.md)
    - [entry](reference/models/entry.md)
    - [year](reference/models/year.md)
- **processing**: *Extracting data from documents*
    - [employee_data_extractor](reference/processing/employee_data_extractor.md)
    - [entity_data_extractor](reference/processing/entity_data_extractor.md)
    - [finance_data_extractor](reference/processing/finance_data_extractor.md)
- **retrieval**: *Retrieving documents*
    - [document_downloader](reference/retrieval/document_downloader.md)
    - [document_scraper](reference/retrieval/document_scraper.md)
    - [documents_page](reference/retrieval/document_scraper.md)
    - [entry_scraper](reference/retrieval/entry_scraper.md)
    - [overview_page](reference/retrieval/overview_page.md)
- [database](reference/database.md): *Wrapper for SQLAlchemy for interacting with the database*
- [pipeline](reference/pipeline.md): *Entry point for running processes*
