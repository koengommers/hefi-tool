# hefi_tool.processing.entity_data_extractor
Contains EntityDataExtractor class.
## EntityDataExtractor
Extracts data about the institution entity.

It extracts the legal form, whether the institution is registered
at the Chamber of Commerce and the type of care they provide.
```python
EntityDataExtractor(document)
```
Begin a new data extraction.

**Args:**
- document (Document): An entity document.


### is_registered
```python
EntityDataExtractor.is_registered(self)
```
Check whether the institution is registered at the Chamber of Commerce.

**Returns:**
    (bool|None) A boolean if the result can be found, else None.


### list_institution_types
```python
EntityDataExtractor.list_institution_types(self, result)
```
Get a list of all the institution types on the document.

**Args:**
- result: Element that contains the institution types.

**Returns:**
    (list) List of institution types


### option_is_checked
```python
EntityDataExtractor.option_is_checked(elem)
```
Check whether an option on the form is checked.

**Args:**
- elem: The element to check.

**Returns:**
    (bool) True if it is checked.


### bbox_to_string
```python
EntityDataExtractor.bbox_to_string(bbox)
```
Format a list of bounding box coordinates to a string.

**Args:**
- bbox (list): List of coordinates.

**Returns:**
    (str) String in format [x1, y1, x2, y2].


### bbox_to_list
```python
EntityDataExtractor.bbox_to_list(bbox)
```
Convert a bounding box string to a list of coordinates.

**Args:**
- bbox (str): Bounding box in format [x1, y1, x2, y2].

**Returns:**
    (str) List of coordinates.


### find_institution_type
```python
EntityDataExtractor.find_institution_type(self)
```
Find institution type.

**Returns:**
    (list) List of institution types belonging to the institution.


### find_legal_form
```python
EntityDataExtractor.find_legal_form(self)
```
Find the checked legal form.

**Returns:**
    (str) The legal form.


### run
```python
EntityDataExtractor.run(self)
```
Run the extraction.
### save_results
```python
EntityDataExtractor.save_results(self)
```
Save the result.
