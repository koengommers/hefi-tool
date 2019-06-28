# Using the data

## Load into dataframe

A year and a datapoints can be chosen to load into a dataframe. See [Pipeline.year_to_dataframe()](../reference/pipeline.md#year_to_dataframe) for more details.

```python
from hefi_tool import Pipeline

data_points = ['totaal bedrijfsopbrengsten', 'totaal personeelskosten', 'totaal personeel']
Pipeline.year_to_dataframe(2018, business_id='KvK nummer', name='instelling', data_points=data_points)
```
