# hefi_tool.models.data_point
Contains DataPoint class.
## DataPoint
Represents a data point.

This class is a SQLAlchemy model for the database.
A data point is stored with a key/name, a value type and value.
```python
DataPoint(entry, key)
```
Create a new data point.

**Args:**
- entry (Entry): The entry to which the data point belongs.
- key (str): The key/name for the data point.


### list_to_csv
```python
DataPoint.list_to_csv(value)
```
Convert a list to a comma separated string.

**Args:**
- value (list): The list to convert.


### set_value
```python
DataPoint.set_value(self, value)
```
Set the value of the data point.

The value type is inferred from the value variable type.

**Args:**
- value: The value to set.


### get_value
```python
DataPoint.get_value(self)
```
Get the value from the data point.

The value is converted to fit its value type.


