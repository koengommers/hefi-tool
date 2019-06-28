# hefi_tool.processing.finance_data_extractor
Contains the FinanceDataExtractor class.
## FinanceDataExtractor
Extracts financial details data.

It extracts financial details and tries to match them to indexes from an index file.
It works by searching for the headers, afterwards it searches for the monetary values
by searching for 'euro'. The value names are always on the left of those values.
```python
FinanceDataExtractor(document, index_file=None)
```
Begin a new data extraction.

**Args:**
- document (Document): An entity document.
- index_file (str): Path to the index file to use.

### normalize_index
```python
FinanceDataExtractor.normalize_index(index)
```
Normalize an index.

**Args:**
- index (str): The index to normalize

**Returns:**
    (str) Normalized index.


### create_index_file
```python
FinanceDataExtractor.create_index_file(documents, return_file)
```
Create index file from a list of documents.

**Args:**
- documents (list): List of financial documents.
- return_file (str): Path of file destination.


### bbox_to_string
```python
FinanceDataExtractor.bbox_to_string(bbox)
```
Format a list of bounding box coordinates to a string.

**Args:**
- bbox (list): List of coordinates.

**Returns:**
    (str) String in format [x1, y1, x2, y2].


### bbox_to_list
```python
FinanceDataExtractor.bbox_to_list(bbox)
```
Convert a bounding box string to a list of coordinates.

**Args:**
- bbox (str): Bounding box in format [x1, y1, x2, y2].

**Returns:**
    (str) List of coordinates.


### is_in_right_column
```python
FinanceDataExtractor.is_in_right_column(self, obj, max_edge_distance=10)
```
Check whether an object is in the right column.

**Args:**
- obj: The object to check

**Returns:**
    (bool) True if in right column.


### get_columns
```python
FinanceDataExtractor.get_columns(self)
```
Find the coordinates of the middle and right column.
### get_value_locations
```python
FinanceDataExtractor.get_value_locations(self)
```
Get locations of values in all three columns.

This function takes the objects in the right column,
makes list with bounding boxes of values in all columns.

**Returns:**
    (list) Bounding boxes of values in all columns.


### build_query
```python
FinanceDataExtractor.build_query(self)
```
Build a query using the bounding boxes.
### match_index
```python
FinanceDataExtractor.match_index(self, index)
```
Match an index to indexes from the index file.

**Args:**
- index (str): The index to match.

**Returns:**
    (str): The matched index.


### get_numerical
```python
FinanceDataExtractor.get_numerical(value)
```
Get a numerical value out of a string.

**Args:**
- value (str): The string containing a possible numeric value.

**Returns:**
    (int) The found numeric value.


### to_dict
```python
FinanceDataExtractor.to_dict(self, results)
```
Put results in a dictionary.

Matches the index and extracts the numerical values from the results.

**Args:**
- results: The results to process.

**Returns:**
    (tuple) A dictionary for current year and for last year.


### run
```python
FinanceDataExtractor.run(self)
```
Run the extraction.

**Returns:**
    (dict) The results.


### save_results
```python
FinanceDataExtractor.save_results(self)
```
Save the result.
