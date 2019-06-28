# Processing a year

For exact use of the functions and their arguments, see [Pipeline](../reference/pipeline.md).

## Creating financial index file
If there are documents in the database but no financial index file yet, it can be created this way.

```python
from hefi_tool import Pipeline

Pipeline.create_index_file('data/indexes.txt')
```

## Running all tasks for a year
With the use of `Pipeline.process_year()` all tasks for a certain year can be ran. Running this will take an extremely long time (estimated 30 hours for a year) because processing the PDF documents is computationally expensive.

```python
from hefi_tool import Pipeline

Pipeline.process_year(2018, 'data/indexes.txt')
```

## Running tasks individually
Tasks can also be run separately, for example in case when there are no documents yet for creating the index file.

### Scraping entries and indexing documents
```python
from hefi_tool import Pipeline

Pipeline.scrape_entries(2018)
entries = Pipeline.get_entries(2018)
Pipeline.index_standardized_documents(entries)
```

### Downloading necessary documents
```python
from hefi_tool import Pipeline

entries = Pipeline.get_entries(2018)
Pipeline.download_documents(entries)
```
### Extracting data
```python
from hefi_tool import Pipeline

entries = Pipeline.get_entries(2018)
Pipeline.extract_data(entries, 'data/indexes.txt')
```
