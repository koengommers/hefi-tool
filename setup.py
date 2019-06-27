import setuptools

setuptools.setup(
    name="hefi_tool",
    version="0.0.1",
    packages=['hefi_tool'],
    install_requires=[
        'sqlalchemy',
        'alembic',
        'selenium',
        'bs4',
        'requests',
        'pdfquery',
        'jellyfish',
        'pandas'
    ]
)
