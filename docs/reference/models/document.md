# hefi_tool.models.document
Contains Database class.
## Document
Represents a document.

This class is a SQLAlchemy model for the database.
```python
Document(entry, label, standardized, name=None, published_on=None, url=None)
```
Create a new document.

**Args:**
- entry (Entry): The entry to which the document belongs.
- label (str): The label the document has.
- standardized (bool): Whether the document is a standardized format.
- name (str): The optional name of the document.
- published_on (datetime.date): Date on which it was published.
- url (str): Optional url to the document.
    - The URL isn't really used, because it is generated and not reliable because it changes.


### filename
```python
Document.filename(self, ext=True)
```
Get the filename for storing the document.

**Args:**
- ext (bool): Whether to include the extension (.pdf)

**Returns:**
    (str) The filename.


### get_path
```python
Document.get_path(self, download=True)
```
Get path of the document file.

**Args:**
- download (bool): Whether to download document if it isn't yet.

**Returns:**
    (str) The absolute path to the file.


### set_downloaded
```python
Document.set_downloaded(self)
```
Mark the document as downloaded and save path.
### remove_download
```python
Document.remove_download(self)
```
Unmark the document as downloaded.
### download
```python
Document.download(self)
```
Download this document.
### set_processed
```python
Document.set_processed(self)
```
Mark the document as processed.
