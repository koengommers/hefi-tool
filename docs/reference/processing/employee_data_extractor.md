# hefi_tool.processing.employee_data_extractor
Contains EmployeeDataExtractor class.
## EmployeeDataExtractor
Extracts data about amount of employees.

Employee documents differ from year to year. The used method assumes a document from
2018 is used. It extracts the total amount of employees at the end of the year.

```python
EmployeeDataExtractor(document)
```
Begin a new data extraction.

**Args**:
- document (Document): An employee document.

### get_bbox
```python
EmployeeDataExtractor.get_bbox(elem)
```
Get list of coordinates of the bounding box from an element.

**Args:**
- elem: The element to get the bbox for.

**Returns:**
    (list) Coordinates of the bounding box.


### locate_column
```python
EmployeeDataExtractor.locate_column(self)
```
Locate the column containing number employees end of year.
### get_numerical
```python
EmployeeDataExtractor.get_numerical(value)
```
Get a numerical value out of a string.

**Args:**
- value (str): The string containing a possible numeric value.

**Returns:**
    (int) The found numeric value.


### get_employees
```python
EmployeeDataExtractor.get_employees(self)
```
Extract number of total employees at end of the year.

**Returns:**
    (dict) Dictionary of results.


### run
```python
EmployeeDataExtractor.run(self)
```
Run the extraction.
### save_result
```python
EmployeeDataExtractor.save_result(self)
```
Save the result.
