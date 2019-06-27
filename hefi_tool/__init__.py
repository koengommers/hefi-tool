import os

from .pipeline import Pipeline

directories = ['data', 'data/temp', 'data/pdf', 'data/html']
for directory in directories:
    os.makedirs(directory, exist_ok=True)
