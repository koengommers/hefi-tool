# Tweedejaarsproject Volkskrant

Provides insights to healthcare financials

## Group (Chicken)
- Soufiane Ben Haddou
- Koen Gommers
- Dennis Swart
- Jeroen Taal

## Setup

### Requirements

- Python 3.7
- pipenv
- chromedriver

### Instructions

Install dependencies and create necessary directories

    pipenv install
    mkdir data
    mkdir data/html

Activate virtualenv (Don't forget to do this every time after opening a new terminal)

    pipenv shell

If you need to run database migrations, make sure that your Python path is in your environment variables.

    export PYTHONPATH=.

To upgrade to newest database scheme, run:

    alembic upgrade head

Now you're all set to run the Python files. Example:

    python run.py
