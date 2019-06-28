# hefi_tool.retrieval.overview_page
Contains OverviewPage class.
## OverviewPage
Represents the overview page of a year.
```python
OverviewPage(year, reload=False, driver=None)
```
Init the class.

**Args:**
- year (int): The year to get the overview page for.
- reload (bool): Whether to reload the page if it is already downloaded.
- driver (selenium.webdriver.Chrome): The web driver to be used.
    - If none is given than a new webdriver will be started.

### html_file
```python
OverviewPage.html_file(self)
```
Get HTML file path for saving the document.

**Returns:**
    (str) Path for the HTML file.


### init_driver
```python
OverviewPage.init_driver(self)
```
Start a new webdriver.
### navigate_to_page
```python
OverviewPage.navigate_to_page(self)
```
Let the webdriver navigate to the page.
### download_document
```python
OverviewPage.download_document(self, document)
```
Download a document that is on the page.

**Args:**
- document (Document): The document to download.


### download
```python
OverviewPage.download(self)
```
Get the HTML content from the URL.
### save
```python
OverviewPage.save(self)
```
Save the HTML for caching purposes.

The HTML file is saved because the website sometimes has
outages, in that case the saved file can be used.


### get_html
```python
OverviewPage.get_html(self)
```
Get HTML for the page.

Downloads the HTML if it doesn't have it yet.

**Returns:**
    (str) HTML content.


