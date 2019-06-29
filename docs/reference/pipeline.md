# hefi_tool.pipeline
Contains Pipeline class.

The pipeline class is the entrypoint for running most processes for data retrieval, data processing and also for data exporting.


## Pipeline
Entry point for running data related tasks.

It can:
- process all entries from a given year
- create financial details index file
- export data points from a year to a DataFrame

### process_year
```python
Pipeline.process_year(year, index_file)
```
Process a year.

**Args:**
- year (int): The year to process.
- index_file (str): Path to a financial details index file.


### get_entries
```python
Pipeline.get_entries(year)
```
Get entries from a given year.

**Args:**
- year (int): The year to get entries from.

**Returns:**
    list: List of Entry objects.


### year_to_dataframe
```python
Pipeline.year_to_dataframe(year, business_id=None, name=None, data_points=[])
```
Put data points from a year in a DataFrame.

**Args:**
- year (int): The year to select data points from.
- business_id (str): The name of the business id column if it needs to be included.
- name (str): The name of the business name column if it needs to be included.
- data_points (list): List of data point keys that need to be included.

**Returns:**
    The DataFrame.


### entries_to_dataframe
```python
Pipeline.entries_to_dataframe(entries, business_id=None, name=None, data_points=[])
```
Put data points from certain entries in a DataFrame.

**Args:**
- entries (list): List of Entry objects of which the data points get selected.
- business_id (str): The name of the business id column if it needs to be included.
- name (str): The name of the business name column if it needs to be included.
- data_points (list): List of data point keys that need to be included.

**Returns:**
    The DataFrame.

### year_to_csv
```python
Pipeline.year_to_csv(year, business_id=None, name=None, data_points=[], export_path=None)
```
Export data points from a year to a csv.

**Args:**
- year (int): The year to select data points from.
- business_id (str): The name of the business id column if it needs to be included.
- name (str): The name of the business name column if it needs to be included.
- data_points (list): List of data point keys that need to be included.
- export_path (str): The destination of the csv file.
    - If none is given than it will default to `exports/{year}.csv`

### scrape_entries
```python
Pipeline.scrape_entries(year)
```
Scrape entries from a given year.

It will scrape the entries from the institutions on a given year.
It will also index the non-standardized documents belonging to the entries.

**Args:**
- year (int): The year to scrape


### index_standardized_documents
```python
Pipeline.index_standardized_documents(entries)
```
Index standardized documents belonging to the given entries.

**Args:**
- entries (list): List of Entry objects.


### download_documents
```python
Pipeline.download_documents(entries)
```
Download documents needed for data extracting belonging to certain entries.

The method for downloading documents can be found in the DocumentDownloader class.

**Args:**
- entries (list): List of Entry objects.


### extract_data
```python
Pipeline.extract_data(entries, index_file)
```
Extract data from the documents belonging to the entries.

It assumes the documents have been downloaded or they will be skipped.

**Args:**
- entries (list): List of Entry objects.
- index_file (str): Path of the financial index file.
    - The index file is needed to match the item names of the financial details to the given indexes.


### create_index_file
```python
Pipeline.create_index_file(index_file, limit=10)
```
Create an index file for the financial details item names.

It is created by selecting random financial documents and
extracting the item names used in those files.

**Args:**
- index_file (str): Path of the desired location for the index file.
- limit (int): The limit of the random number of documents chosen.


### extract_financial_data
```python
Pipeline.extract_financial_data(entries, index_file)
```
Extract data from the financial documents belonging to the entries.

The method for extracting financial data can be found in the FinanceDataExtractor class.

**Args:**
- entries (list): List of Entry objects.
- index_file (str): Path of the financial index file.
    - The index file is needed to match the item names of the financial details to the given indexes.


### extract_entity_data
```python
Pipeline.extract_entity_data(entries)
```
Extract data from the entity documents belonging to the entries.

The method for extracting financial data can be found in the EntityDataExtractor class.

**Args:**
- entries (list): List of Entry objects.


### extract_employee_data
```python
Pipeline.extract_employee_data(entries)
```
Extract data from the employee documents belonging to the entries.

The method for extracting financial data can be found in the EmployeeDataExtractor class.
Currently only works reliably for employee documents from 2018.

**Args:**
- entries (list): List of Entry objects.


