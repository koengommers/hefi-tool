# hefi_tool.retrieval.documents_page
Contains DocumentsPage class.
## DocumentsPage
Represents a listings page of non-standardized documents.
```python
DocumentsPage(entry, reload=False)
```
Init the class.

**Args:**
- entry (Entry): The entry to get the listings page from.
- reload (bool): Whether to reload the page if it is already downloaded.

### html_file
```python
DocumentsPage.html_file(self)
```
Get HTML file path for saving the document.

**Returns:**
    (str) Path for the HTML file.


### download
```python
DocumentsPage.download(self)
```
Get the HTML content from the URL.
### save
```python
DocumentsPage.save(self)
```
Save the HTML for caching purposes.

The HTML file is saved because the website sometimes has
outages, in that case the saved file can be used.


### get_html
```python
DocumentsPage.get_html(self)
```
Get HTML for the page.

Downloads the HTML if it doesn't have it yet.

**Returns:**
    (str) HTML content.


