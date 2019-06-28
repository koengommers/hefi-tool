# hefi_tool.models.entry
Contains Entry class.
## Entry
Represents an entry of an institution.

An entry is a unique combination of institution and year.
This class is a SQLAlchemy model for the database.
```python
Entry(business_id, year, name, location)
```
Store a new entry.

**Args:**
- business_id (str): The business id of the institution (KvK nummer).
- year (int): The year of the entry.
- name (str): Name of the institution.
- location (str): Geographical location of the institution.


### add_data_point
```python
Entry.add_data_point(self, key, value)
```
Add data point to this entry.

**Args:**
- key (str): Key/name of the data point.
- value: Value of the data point.


### get_data_point
```python
Entry.get_data_point(self, key)
```
Get a data point by key.

**Args:**
- key (str): Key of the data point.

**Returns:**
    value of the data point.


### get_financial_document
```python
Entry.get_financial_document(self)
```
Get the financial document of this entry.

**Returns:**
    (Document) The financial document.


### get_employee_document
```python
Entry.get_employee_document(self)
```
Get the employee document of this entry.

**Returns:**
    (Document) The employee document.


### get_entity_document
```python
Entry.get_entity_document(self)
```
Get the entity document of this entry.

**Returns:**
    (Document) The entity document.


### get_necessary_documents
```python
Entry.get_necessary_documents(self)
```
Get all documents needed for data extraction.

**Returns:**
    (list) List of documents.


### to_list
```python
Entry.to_list(self, business_id=True, name=True, data_points=[])
```
Convert this entry in a list containing data points.

Is used for putting data in a DataFrame.

**Args:**
- business_id (bool): Whether the business id needs to be included.
- name (bool): Whether the institution name needs to be included.
- data_points (list): List of data point keys that need to be included.

**Returns:**
    (list) List of entry properties and data points.


