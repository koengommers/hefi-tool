# Using the data

## Load into dataframe

A year and datapoints can be chosen to load into a dataframe. See [Pipeline.year_to_dataframe()](../reference/pipeline.md#year_to_dataframe) for more details.

```python
from hefi_tool import Pipeline

data_points = ['totaal bedrijfsopbrengsten', 'totaal personeelskosten', 'totaal personeel']
Pipeline.year_to_dataframe(2018, business_id='KvK nummer', name='instelling', data_points=data_points)
```

## Export to CSV

A year and datapoints can be exported to CSV. See [Pipeline.year_to_csv()](../reference/pipeline.md#year_to_csv) for more details.

```python
from hefi_tool import Pipeline

data_points = ['totaal bedrijfsopbrengsten', 'totaal personeelskosten', 'totaal personeel']
Pipeline.year_to_csv(2018, business_id='KvK nummer', name='instelling', data_points=data_points)
```

## Querying the database

If one of the supplied functions doesn't suit the needs, the database can be queried directly. For exact details on forming queries, read the [SQLAlchemy querying documentation](https://docs.sqlalchemy.org/en/13/orm/query.html).

Example of querying all indexed documents:

```python
from hefi_tool.database import db
from hefi_tool.models import Document

documents = db.session.query(Document).all()
```
