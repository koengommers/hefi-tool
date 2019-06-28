# hefi_tool.database
Contains Database class and starts database session.

## Database
Wrapper class for access to the database.
```python
Database(url)
```
Start a new session.

**Args:**
- url (str): URL for database connection.

### create_all
```python
Database.create_all(self)
```
Create all tables and columns.
