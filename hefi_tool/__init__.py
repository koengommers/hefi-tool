"""Import pipeline and create needed directories.

Pipeline is imported, so it can be imported by `from hefi_tool import pipeline`.
Some directories are needed for storing data, these are created if they don't exist yet.

"""

import os

from .pipeline import Pipeline

directories = ['data', 'data/temp', 'data/pdf', 'data/html', 'data/exports']
for directory in directories:
    os.makedirs(directory, exist_ok=True)
