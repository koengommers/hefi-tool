# hefi_tool.retrieval.document_downloader
Contains DocumentDownloader class.
## DocumentDownloader
Downloads documents efficiently.

It will split the documents into non-standardized and standardized documents, because they have to be downloaded differently. Afterwards documents that are on the same page will be grouped, to avoiding having to load pages double. Documents are downloaded using a WebDriver. As the status of downloads cannot be read, it will download the documents to a temporarily directory, when a file is detected in that directory it will be renamed and moved.
```python
DocumentDownloader(documents, download_dir='data/temp', document_dir='data/pdf')
```
Init downloader object.

It will split the documents into non-standardized and standardized documents, because they have to be downloaded differently.

**Args:**
- documents (list): List of document objects to download.
- download_dir (str): Path to directory that temporarily stores downloads.
- document_dir (str): Path to directory that stores the documents.

### split_documents
```python
DocumentDownloader.split_documents(self)
```
Split documents in non-standardized and standardized.
### init_driver
```python
DocumentDownloader.init_driver(self)
```
Start the WebDriver.
### download
```python
DocumentDownloader.download(self)
```
Start downloading the documents.
### check_directory
```python
DocumentDownloader.check_directory(self)
```
Check if temporary download directory is empty.
### download_standardized
```python
DocumentDownloader.download_standardized(self)
```
Download the standardized documents.

Groups documents by entry (year and institution) because their links
are on the same page.


### download_non_standardized
```python
DocumentDownloader.download_non_standardized(self)
```
Download the non-standardized documents.

Groups documents by year because their links are on the same pages.


