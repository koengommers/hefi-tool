# Healthcare Financials Tool (HeFi-tool)

A tool for retrieving and analysing Dutch healthcare financial data.

## Requirements

- Python 3.7
- pip
- [chromedriver](http://chromedriver.chromium.org/)

## Installation

    pip install https://github.com/koengommers/hefi-tool/archive/master.zip

## Database migrations

Alembic is used for database migrations. To set up a new database (tables, columns, etc.), run:

    alembic -c path/to/hefi-tool/hefi_tool/alembic.ini upgrade head

## Documentation

Explanations, examples and reference of the code are available. [View documentation](docs/index.md)
