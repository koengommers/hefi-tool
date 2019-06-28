import setuptools

setuptools.setup(
    name="hefi_tool",
    version="1.0.0",
    packages=[
        'hefi_tool',
        'hefi_tool.models',
        'hefi_tool.processing',
        'hefi_tool.retrieval'
    ],
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
